"""
CrewAI-inspired Agent implementation
"""

import time
from typing import List, Dict, Any, Optional, Callable
from ..cognitive.types import Task
from .types import AgentOutput


class Agent:
    """
    CrewAI 风格的智能体

    每个 Agent 都有明确的角色、目标和背景故事，
    并能够执行特定的任务或委派给其他智能体。
    """

    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        skills: List[str],
        allow_delegation: bool = True,
        verbose: bool = False
    ):
        """
        初始化智能体

        Args:
            role: 角色名称（如 "Research Specialist"）
            goal: 目标描述
            backstory: 背景故事（提供上下文和专业性）
            skills: 可用技能列表
            allow_delegation: 是否允许委派任务给其他智能体
            verbose: 是否输出详细日志
        """
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.skills = skills
        self.allow_delegation = allow_delegation
        self.verbose = verbose

        # 运行时状态
        self.task_history: List[Dict[str, Any]] = []
        self.delegation_count = 0

    def execute_task(
        self,
        task: Task,
        context: Dict[str, Any],
        skill_executor: Optional[Callable] = None
    ) -> AgentOutput:
        """
        执行任务

        Args:
            task: 要执行的任务
            context: 上下文信息
            skill_executor: 技能执行器（可选）

        Returns:
            AgentOutput: 执行结果
        """
        start_time = time.time()

        if self.verbose:
            print(f"[{self.role}] 开始执行任务: {task.description}")

        try:
            # 1. 检查是否有合适的技能
            matching_skills = [
                s for s in task.required_skills
                if s in self.skills
            ]

            if not matching_skills:
                if self.allow_delegation:
                    # 尝试委派
                    result = self._delegate_task(task, context)
                else:
                    raise ValueError(
                        f"Agent '{self.role}' 缺少必需技能: {task.required_skills}"
                    )
            else:
                # 2. 执行技能
                if skill_executor:
                    result = skill_executor(matching_skills[0], task, context)
                else:
                    # 简化执行（实际应调用真实技能）
                    result = {
                        "success": True,
                        "output": f"完成任务: {task.description}",
                        "skill_used": matching_skills[0]
                    }

            execution_time_ms = int((time.time() - start_time) * 1000)

            # 3. 记录任务历史
            self.task_history.append({
                "task": task.description,
                "result": result,
                "timestamp": time.time()
            })

            if self.verbose:
                print(f"[{self.role}] 任务完成，耗时 {execution_time_ms}ms")

            return AgentOutput(
                agent_role=self.role,
                task_description=task.description,
                result=result,
                success=result.get("success", True),
                execution_time_ms=execution_time_ms,
                metadata={
                    "skills_used": matching_skills,
                    "delegation_occurred": False
                }
            )

        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)

            if self.verbose:
                print(f"[{self.role}] 任务失败: {str(e)}")

            return AgentOutput(
                agent_role=self.role,
                task_description=task.description,
                result={"error": str(e)},
                success=False,
                execution_time_ms=execution_time_ms,
                metadata={"error": str(e)}
            )

    def _delegate_task(
        self,
        task: Task,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        委派任务给其他智能体

        Args:
            task: 要委派的任务
            context: 上下文

        Returns:
            Dict: 委派结果
        """
        self.delegation_count += 1

        if self.verbose:
            print(f"[{self.role}] 委派任务: {task.description}")

        # 简化实现：返回委派标记
        # 实际应从 crew 中选择合适的智能体
        return {
            "success": True,
            "output": f"任务已委派",
            "delegated": True
        }

    def can_handle_task(self, task: Task) -> bool:
        """
        检查是否能处理任务

        Args:
            task: 任务

        Returns:
            bool: 是否能处理
        """
        if not task.required_skills:
            return True

        # 检查是否有至少一个匹配的技能
        return any(skill in self.skills for skill in task.required_skills)

    def get_context_message(self) -> str:
        """获取智能体的上下文消息（用于提示工程）"""
        return f"""
角色: {self.role}
目标: {self.goal}
背景: {self.backstory}
技能: {', '.join(self.skills)}
        """.strip()

    def reset_history(self):
        """重置任务历史"""
        self.task_history = []
        self.delegation_count = 0

    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计"""
        if not self.task_history:
            return {
                "total_tasks": 0,
                "success_rate": 0.0,
                "delegation_rate": 0.0
            }

        total_tasks = len(self.task_history)
        successful_tasks = sum(
            1 for t in self.task_history
            if t["result"].get("success", False)
        )

        return {
            "total_tasks": total_tasks,
            "success_rate": successful_tasks / total_tasks,
            "delegation_rate": self.delegation_count / total_tasks,
            "delegations": self.delegation_count
        }
