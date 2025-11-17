"""
CrewAI-inspired Crew implementation

团队协作模式，支持顺序和层级流程
"""

import time
from typing import List, Dict, Any, Optional, Callable
from ..cognitive.types import Task
from .types import ProcessType, AgentOutput, CrewOutput
from .agent import Agent


class Crew:
    """
    CrewAI 风格的智能体团队

    支持两种流程模式：
    1. SEQUENTIAL: 按顺序执行任务
    2. HIERARCHICAL: 自动选出管理员，进行任务分配和协调
    """

    def __init__(
        self,
        name: str,
        agents: List[Agent],
        tasks: List[Task],
        process: ProcessType = ProcessType.SEQUENTIAL,
        verbose: bool = False,
        skill_executor: Optional[Callable] = None
    ):
        """
        初始化团队

        Args:
            name: 团队名称
            agents: 智能体列表
            tasks: 任务列表
            process: 流程类型
            verbose: 是否输出详细日志
            skill_executor: 技能执行器
        """
        self.name = name
        self.agents = agents
        self.tasks = tasks
        self.process = process
        self.verbose = verbose
        self.skill_executor = skill_executor

        # 运行时状态
        self.execution_history: List[CrewOutput] = []
        self.manager: Optional[Agent] = None

        # 如果是层级模式，选出管理员
        if self.process == ProcessType.HIERARCHICAL:
            self._elect_manager()

    def _elect_manager(self):
        """选举管理员（层级模式）"""
        # 简化实现：选择技能最多的智能体作为管理员
        if self.agents:
            self.manager = max(self.agents, key=lambda a: len(a.skills))
            if self.verbose:
                print(f"[Crew '{self.name}'] 选举 '{self.manager.role}' 为管理员")

    def kickoff(self, inputs: Dict[str, Any]) -> CrewOutput:
        """
        启动团队协作

        Args:
            inputs: 输入数据

        Returns:
            CrewOutput: 团队执行结果
        """
        start_time = time.time()

        if self.verbose:
            print(f"\n{'=' * 60}")
            print(f"Crew '{self.name}' 启动")
            print(f"流程模式: {self.process.value}")
            print(f"智能体数量: {len(self.agents)}")
            print(f"任务数量: {len(self.tasks)}")
            print(f"{'=' * 60}\n")

        try:
            if self.process == ProcessType.SEQUENTIAL:
                agent_outputs = self._execute_sequential(inputs)
            elif self.process == ProcessType.HIERARCHICAL:
                agent_outputs = self._execute_hierarchical(inputs)
            elif self.process == ProcessType.PARALLEL:
                agent_outputs = self._execute_parallel(inputs)
            else:
                raise ValueError(f"不支持的流程类型: {self.process}")

            execution_time_ms = int((time.time() - start_time) * 1000)

            # 汇总最终结果
            final_result = self._aggregate_results(agent_outputs)

            # 判断整体是否成功
            success = all(output.success for output in agent_outputs)

            crew_output = CrewOutput(
                crew_name=self.name,
                agent_outputs=agent_outputs,
                final_result=final_result,
                total_execution_time_ms=execution_time_ms,
                success=success,
                metadata={
                    "process_type": self.process.value,
                    "total_agents": len(self.agents),
                    "total_tasks": len(self.tasks)
                }
            )

            self.execution_history.append(crew_output)

            if self.verbose:
                print(f"\n{'=' * 60}")
                print(f"Crew '{self.name}' 完成")
                print(f"总耗时: {execution_time_ms}ms")
                print(f"状态: {'成功' if success else '失败'}")
                print(f"{'=' * 60}\n")

            return crew_output

        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)

            if self.verbose:
                print(f"\n[Crew '{self.name}'] 执行失败: {str(e)}\n")

            return CrewOutput(
                crew_name=self.name,
                agent_outputs=[],
                final_result={"error": str(e)},
                total_execution_time_ms=execution_time_ms,
                success=False,
                metadata={"error": str(e)}
            )

    def _execute_sequential(self, inputs: Dict[str, Any]) -> List[AgentOutput]:
        """顺序执行模式"""
        agent_outputs = []
        context = inputs.copy()

        for i, task in enumerate(self.tasks):
            # 选择合适的智能体
            agent = self._select_agent_for_task(task)

            if not agent:
                if self.verbose:
                    print(f"警告: 没有智能体能处理任务 '{task.description}'")
                continue

            # 执行任务
            output = agent.execute_task(task, context, self.skill_executor)
            agent_outputs.append(output)

            # 更新上下文（串联任务）
            if output.success:
                context[f"task_{i}_result"] = output.result

        return agent_outputs

    def _execute_hierarchical(self, inputs: Dict[str, Any]) -> List[AgentOutput]:
        """层级执行模式（管理员协调）"""
        if not self.manager:
            raise ValueError("层级模式需要管理员，但未选举成功")

        agent_outputs = []
        context = inputs.copy()

        # 管理员制定计划
        if self.verbose:
            print(f"[Manager '{self.manager.role}'] 制定执行计划...")

        # 简化实现：按任务优先级排序
        sorted_tasks = sorted(self.tasks, key=lambda t: t.priority, reverse=True)

        for task in sorted_tasks:
            # 管理员分配任务给最合适的智能体
            agent = self._manager_assign_task(task)

            if not agent:
                # 管理员亲自执行
                agent = self.manager

            # 执行任务
            output = agent.execute_task(task, context, self.skill_executor)
            agent_outputs.append(output)

            # 管理员验证结果
            if self.verbose:
                status = "✓" if output.success else "✗"
                print(f"[Manager] 任务 '{task.description}' {status}")

            # 更新上下文
            if output.success:
                context[f"task_{task.id}_result"] = output.result

        return agent_outputs

    def _execute_parallel(self, inputs: Dict[str, Any]) -> List[AgentOutput]:
        """并行执行模式（简化实现，实际应使用多线程/异步）"""
        # 注意：这是简化的实现，真正的并行需要多线程或异步
        agent_outputs = []

        # 为每个任务分配智能体并"并行"执行
        for task in self.tasks:
            agent = self._select_agent_for_task(task)
            if agent:
                output = agent.execute_task(task, inputs, self.skill_executor)
                agent_outputs.append(output)

        return agent_outputs

    def _select_agent_for_task(self, task: Task) -> Optional[Agent]:
        """为任务选择最合适的智能体"""
        # 找出能处理该任务的智能体
        capable_agents = [a for a in self.agents if a.can_handle_task(task)]

        if not capable_agents:
            return None

        # 选择技能匹配度最高的
        best_agent = max(
            capable_agents,
            key=lambda a: len(set(a.skills) & set(task.required_skills))
        )

        return best_agent

    def _manager_assign_task(self, task: Task) -> Optional[Agent]:
        """管理员分配任务"""
        # 排除管理员自己
        workers = [a for a in self.agents if a != self.manager]

        capable_workers = [a for a in workers if a.can_handle_task(task)]

        if not capable_workers:
            return None

        # 选择负载最低的智能体
        best_worker = min(
            capable_workers,
            key=lambda a: len(a.task_history)
        )

        return best_worker

    def _aggregate_results(self, agent_outputs: List[AgentOutput]) -> Any:
        """汇总所有智能体的输出"""
        if not agent_outputs:
            return None

        # 简化实现：返回所有结果的列表
        return {
            "summary": f"完成 {len(agent_outputs)} 个任务",
            "results": [
                {
                    "agent": output.agent_role,
                    "task": output.task_description,
                    "success": output.success,
                    "output": output.result
                }
                for output in agent_outputs
            ],
            "overall_success": all(o.success for o in agent_outputs)
        }

    def get_crew_stats(self) -> Dict[str, Any]:
        """获取团队统计信息"""
        if not self.execution_history:
            return {
                "total_executions": 0,
                "success_rate": 0.0,
                "avg_execution_time_ms": 0
            }

        total = len(self.execution_history)
        successful = sum(1 for e in self.execution_history if e.success)
        avg_time = sum(e.total_execution_time_ms for e in self.execution_history) / total

        return {
            "total_executions": total,
            "success_rate": successful / total,
            "avg_execution_time_ms": int(avg_time),
            "agent_stats": {
                agent.role: agent.get_performance_stats()
                for agent in self.agents
            }
        }
