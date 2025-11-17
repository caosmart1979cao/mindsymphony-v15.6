"""
ACE Layer 4: Executive Function (执行功能)

执行规划与资源管理，将战略目标转化为可执行的详细计划。
"""

from typing import List, Dict, Any
from .types import (
    Strategy,
    Goal,
    ExecutionPlan,
    Task,
    TaskStatus,
    ResourceAllocation
)
from .self_model import SelfModel


class ExecutiveFunction:
    """
    执行功能：从战略到战术的转化

    核心职责：
    1. 将战略目标分解为具体任务
    2. 分配资源和设定优先级
    3. 创建详细的执行计划和时间线
    4. 设置检查点和应急方案
    """

    def __init__(self, strategy: Strategy, self_model: SelfModel):
        """
        初始化执行功能

        Args:
            strategy: 战略计划
            self_model: 自我模型引用
        """
        self.strategy = strategy
        self.self_model = self_model
        self.active_plans: Dict[str, ExecutionPlan] = {}
        self.task_counter = 0

    def create_execution_plan(self, strategic_goal: Goal) -> ExecutionPlan:
        """
        将战略目标转化为详细执行计划

        Args:
            strategic_goal: 战略目标

        Returns:
            ExecutionPlan: 执行计划
        """
        # 1. 分解为子任务
        tasks = self._decompose_into_tasks(strategic_goal)

        # 2. 设置依赖关系
        tasks = self._set_dependencies(tasks)

        # 3. 分配资源
        resource_allocation = self._allocate_resources(tasks)

        # 4. 设定时间线
        timeline = self._create_timeline(tasks)

        # 5. 创建检查点
        checkpoints = self._create_checkpoints(tasks)

        # 6. 准备降级策略
        fallback_strategies = self._prepare_fallback_strategies(strategic_goal)

        plan = ExecutionPlan(
            goal=strategic_goal,
            tasks=tasks,
            timeline=timeline,
            resource_allocation=resource_allocation,
            checkpoints=checkpoints,
            fallback_strategies=fallback_strategies
        )

        self.active_plans[f"plan_{self.task_counter}"] = plan
        self.task_counter += 1

        return plan

    def _decompose_into_tasks(self, goal: Goal) -> List[Task]:
        """分解目标为具体任务"""
        tasks = []
        goal_desc = goal.description.lower()

        # 根据目标类型创建任务
        if "研究" in goal_desc or "分析" in goal_desc:
            tasks.extend(self._create_research_tasks(goal))

        if "创建" in goal_desc or "生成" in goal_desc:
            tasks.extend(self._create_creation_tasks(goal))

        if "优化" in goal_desc:
            tasks.extend(self._create_optimization_tasks(goal))

        if "部署" in goal_desc:
            tasks.extend(self._create_deployment_tasks(goal))

        # 如果没有匹配的模式，创建通用任务
        if not tasks:
            tasks.append(self._create_task(
                description=f"执行：{goal.description}",
                priority=goal.priority,
                required_skills=["general"]
            ))

        return tasks

    def _create_research_tasks(self, goal: Goal) -> List[Task]:
        """创建研究类任务"""
        return [
            self._create_task(
                description="收集相关信息和文献",
                priority=goal.priority,
                required_skills=["knowledge-explorer"]
            ),
            self._create_task(
                description="分析和提取关键洞察",
                priority=goal.priority,
                required_skills=["analysis"]
            ),
            self._create_task(
                description="撰写研究报告",
                priority=goal.priority - 1,
                required_skills=["official-writer"]
            )
        ]

    def _create_creation_tasks(self, goal: Goal) -> List[Task]:
        """创建创作类任务"""
        return [
            self._create_task(
                description="设计和规划创作方案",
                priority=goal.priority,
                required_skills=["concept-singularity"]
            ),
            self._create_task(
                description="执行创作",
                priority=goal.priority,
                required_skills=["creation"]
            ),
            self._create_task(
                description="质量检查和优化",
                priority=goal.priority - 1,
                required_skills=["quality-check"]
            )
        ]

    def _create_optimization_tasks(self, goal: Goal) -> List[Task]:
        """创建优化类任务"""
        return [
            self._create_task(
                description="性能分析和瓶颈识别",
                priority=goal.priority,
                required_skills=["analysis", "performance_monitor"]
            ),
            self._create_task(
                description="实施优化措施",
                priority=goal.priority,
                required_skills=["optimization"]
            ),
            self._create_task(
                description="验证优化效果",
                priority=goal.priority - 1,
                required_skills=["testing"]
            )
        ]

    def _create_deployment_tasks(self, goal: Goal) -> List[Task]:
        """创建部署类任务"""
        return [
            self._create_task(
                description="准备部署环境",
                priority=goal.priority,
                required_skills=["infrastructure"]
            ),
            self._create_task(
                description="执行部署",
                priority=goal.priority + 1,  # 部署是关键任务
                required_skills=["agent-deployer"]
            ),
            self._create_task(
                description="验证部署成功",
                priority=goal.priority,
                required_skills=["testing", "monitoring"]
            ),
            self._create_task(
                description="建立监控和告警",
                priority=goal.priority - 1,
                required_skills=["monitoring"]
            )
        ]

    def _create_task(
        self,
        description: str,
        priority: int,
        required_skills: List[str]
    ) -> Task:
        """创建单个任务"""
        task_id = f"task_{self.task_counter}_{len(self.active_plans)}"
        return Task(
            id=task_id,
            description=description,
            priority=priority,
            required_skills=required_skills
        )

    def _set_dependencies(self, tasks: List[Task]) -> List[Task]:
        """设置任务依赖关系"""
        # 简化的顺序依赖：后续任务依赖前面的任务
        for i in range(1, len(tasks)):
            tasks[i].dependencies.append(tasks[i - 1].id)

        return tasks

    def _allocate_resources(self, tasks: List[Task]) -> ResourceAllocation:
        """分配资源"""
        cpu_allocation = {}
        memory_budget_mb = {}
        skill_slots = {}
        time_allocation = {}

        total_tasks = len(tasks)
        base_cpu_per_task = 1.0 / total_tasks if total_tasks > 0 else 1.0

        for task in tasks:
            # CPU 分配（根据优先级调整）
            cpu_share = base_cpu_per_task * (task.priority / 10.0)

            for skill in task.required_skills:
                if skill not in cpu_allocation:
                    cpu_allocation[skill] = 0.0
                    memory_budget_mb[skill] = 100
                    skill_slots[skill] = 1
                    time_allocation[skill] = 0

                cpu_allocation[skill] += cpu_share

                # 内存分配（基础 100MB + 根据技能调整）
                if "research" in skill or "analysis" in skill:
                    memory_budget_mb[skill] = max(
                        memory_budget_mb[skill],
                        200
                    )

                # 时间分配
                assessment = self.self_model.can_accomplish({
                    "required_skills": [skill],
                    "complexity": "medium"
                })
                if assessment.estimated_time_ms:
                    time_allocation[skill] += assessment.estimated_time_ms

        # 归一化 CPU 分配
        total_cpu = sum(cpu_allocation.values())
        if total_cpu > 0:
            cpu_allocation = {
                k: v / total_cpu for k, v in cpu_allocation.items()
            }

        return ResourceAllocation(
            cpu_allocation=cpu_allocation,
            memory_budget_mb=memory_budget_mb,
            skill_slots=skill_slots,
            time_allocation=time_allocation
        )

    def _create_timeline(self, tasks: List[Task]) -> Dict[str, str]:
        """创建时间线"""
        timeline = {}

        for i, task in enumerate(tasks):
            # 简化的阶段划分
            if i < len(tasks) // 3:
                phase = "初期"
            elif i < 2 * len(tasks) // 3:
                phase = "中期"
            else:
                phase = "后期"

            timeline[task.id] = phase

        return timeline

    def _create_checkpoints(self, tasks: List[Task]) -> List[Dict[str, Any]]:
        """创建检查点"""
        checkpoints = []

        # 在关键任务后设置检查点
        high_priority_tasks = [t for t in tasks if t.priority >= 8]

        for i, task in enumerate(high_priority_tasks):
            checkpoints.append({
                "id": f"checkpoint_{i}",
                "after_task": task.id,
                "description": f"验证任务 '{task.description}' 的完成质量",
                "success_criteria": [
                    "任务成功完成",
                    "输出质量符合标准",
                    "无阻塞性错误"
                ]
            })

        # 添加最终检查点
        if tasks:
            checkpoints.append({
                "id": "final_checkpoint",
                "after_task": tasks[-1].id,
                "description": "验证所有任务完成",
                "success_criteria": [
                    "所有任务状态为 COMPLETED",
                    "目标达成",
                    "质量检查通过"
                ]
            })

        return checkpoints

    def _prepare_fallback_strategies(self, goal: Goal) -> List[str]:
        """准备降级策略"""
        strategies = []

        if goal.priority >= 9:
            strategies.append("高优先级目标：失败时立即通知用户并请求指导")

        strategies.append("任务失败：尝试备用技能或方法")
        strategies.append("资源不足：降低并发度，顺序执行")
        strategies.append("超时：返回部分结果并标记为未完成")

        if "部署" in goal.description:
            strategies.append("部署失败：自动回滚到上一个稳定版本")

        return strategies

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """
        任务优先级排序

        Args:
            tasks: 任务列表

        Returns:
            List[Task]: 排序后的任务列表
        """
        # 按优先级降序排序，优先级相同则按依赖关系排序
        return sorted(
            tasks,
            key=lambda t: (-t.priority, len(t.dependencies))
        )

    def update_task_status(self, task_id: str, new_status: TaskStatus):
        """更新任务状态"""
        for plan in self.active_plans.values():
            for task in plan.tasks:
                if task.id == task_id:
                    task.status = new_status
                    return

    def get_active_plans(self) -> Dict[str, ExecutionPlan]:
        """获取所有活跃的执行计划"""
        return self.active_plans
