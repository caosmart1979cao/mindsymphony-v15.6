"""
ACE Layer 5: Cognitive Control (认知控制)

动态任务选择与上下文切换，管理并行任务和注意力分配。
"""

import time
from typing import List, Dict, Any, Optional
from .types import Task, TaskStatus, AttentionAllocation
from .executive_function import ExecutiveFunction


class CognitiveControl:
    """
    认知控制：动态任务管理与注意力分配

    核心职责：
    1. 动态选择下一个要执行的任务
    2. 判断是否需要切换上下文
    3. 管理并行任务的注意力分配
    4. 处理中断和优先级变化
    """

    def __init__(self, executive: ExecutiveFunction):
        """
        初始化认知控制

        Args:
            executive: 执行功能引用
        """
        self.executive = executive
        self.current_focus: Optional[Task] = None
        self.task_queue: List[Task] = []
        self.context_switch_history: List[Dict[str, Any]] = []
        self.attention_state = AttentionAllocation(
            primary_focus="",
            background_tasks=[],
            attention_weights={},
            context_switch_cost_ms=50
        )

    def select_next_task(
        self,
        available_tasks: List[Task],
        environment_state: Dict[str, Any],
        internal_state: Dict[str, Any]
    ) -> Optional[Task]:
        """
        动态选择下一个任务

        Args:
            available_tasks: 可用任务列表
            environment_state: 环境状态（资源、负载等）
            internal_state: 内部状态（当前焦点、历史等）

        Returns:
            Task: 选中的任务，如果没有合适的任务则返回 None
        """
        if not available_tasks:
            return None

        # 过滤出可以执行的任务（依赖已满足）
        executable_tasks = [
            task for task in available_tasks
            if self._dependencies_satisfied(task, available_tasks)
        ]

        if not executable_tasks:
            return None

        # 计算每个任务的选择分数
        task_scores = []
        for task in executable_tasks:
            score = self._calculate_task_score(
                task,
                environment_state,
                internal_state
            )
            task_scores.append((task, score))

        # 选择得分最高的任务
        task_scores.sort(key=lambda x: x[1], reverse=True)
        selected_task = task_scores[0][0]

        # 记录选择
        self._record_task_selection(selected_task, task_scores)

        return selected_task

    def _dependencies_satisfied(
        self,
        task: Task,
        all_tasks: List[Task]
    ) -> bool:
        """检查任务依赖是否已满足"""
        if not task.dependencies:
            return True

        # 创建任务 ID 到状态的映射
        task_status_map = {t.id: t.status for t in all_tasks}

        # 检查所有依赖任务是否已完成
        for dep_id in task.dependencies:
            if dep_id in task_status_map:
                if task_status_map[dep_id] != TaskStatus.COMPLETED:
                    return False
            # 如果依赖任务不在列表中，假设已完成
        return True

    def _calculate_task_score(
        self,
        task: Task,
        environment_state: Dict[str, Any],
        internal_state: Dict[str, Any]
    ) -> float:
        """
        计算任务选择分数

        考虑因素：
        1. 优先级
        2. 资源可用性
        3. 上下文切换成本
        4. 估算执行时间
        """
        score = 0.0

        # 1. 优先级权重 (0-10)
        priority_weight = task.priority / 10.0
        score += priority_weight * 40.0  # 最高 40 分

        # 2. 资源可用性
        system_load = environment_state.get("load", 0.5)
        if system_load < 0.7:
            # 负载低，可以执行
            score += 20.0
        elif system_load < 0.9:
            # 负载中等
            score += 10.0
        else:
            # 负载高，降低分数
            score -= 10.0

        # 3. 上下文切换成本
        if self.current_focus:
            # 如果需要切换技能，扣分
            current_skills = set(self.current_focus.required_skills)
            new_skills = set(task.required_skills)
            if current_skills != new_skills:
                score -= 5.0  # 切换成本
            else:
                score += 10.0  # 延续当前上下文，加分

        # 4. 时间考虑
        if task.estimated_duration_ms:
            # 短任务优先（在优先级相近时）
            if task.estimated_duration_ms < 5000:
                score += 5.0
            elif task.estimated_duration_ms > 30000:
                score -= 5.0

        # 5. 历史表现
        if task.id in internal_state.get("task_history", {}):
            history = internal_state["task_history"][task.id]
            if history.get("previous_success", True):
                score += 5.0
            else:
                score -= 10.0  # 曾经失败，降低选择概率

        return score

    def _record_task_selection(
        self,
        selected_task: Task,
        all_scores: List[tuple]
    ):
        """记录任务选择决策"""
        self.context_switch_history.append({
            "timestamp": time.time(),
            "selected_task": selected_task.id,
            "previous_focus": self.current_focus.id if self.current_focus else None,
            "all_scores": [
                {"task_id": task.id, "score": score}
                for task, score in all_scores
            ]
        })

    def should_switch_context(self, new_signal: Dict[str, Any]) -> bool:
        """
        判断是否需要切换上下文

        Args:
            new_signal: 新信号（紧急任务、用户中断等）

        Returns:
            bool: 是否应该切换
        """
        signal_type = new_signal.get("type")
        signal_priority = new_signal.get("priority", 5)

        # 用户中断：立即切换
        if signal_type == "user_interrupt":
            return True

        # 紧急任务
        if signal_type == "urgent_task":
            if signal_priority > (self.current_focus.priority if self.current_focus else 0):
                return True

        # 系统错误/警告
        if signal_type == "system_alert":
            severity = new_signal.get("severity", "low")
            if severity in ["critical", "high"]:
                return True

        # 当前任务阻塞
        if signal_type == "task_blocked":
            # 如果当前任务被阻塞，切换到其他任务
            return True

        # 默认不切换
        return False

    def manage_attention(self, parallel_tasks: List[Task]) -> AttentionAllocation:
        """
        管理并行任务的注意力分配

        Args:
            parallel_tasks: 并行执行的任务列表

        Returns:
            AttentionAllocation: 注意力分配方案
        """
        if not parallel_tasks:
            return AttentionAllocation(
                primary_focus="",
                background_tasks=[],
                attention_weights={},
                context_switch_cost_ms=50
            )

        # 选择主要焦点（最高优先级）
        primary_task = max(parallel_tasks, key=lambda t: t.priority)

        # 其余为背景任务
        background_tasks = [t for t in parallel_tasks if t.id != primary_task.id]

        # 计算注意力权重
        total_priority = sum(t.priority for t in parallel_tasks)
        attention_weights = {
            task.id: task.priority / total_priority
            for task in parallel_tasks
        }

        # 确保主要任务获得至少 60% 的注意力
        if attention_weights.get(primary_task.id, 0) < 0.6:
            # 重新分配
            attention_weights[primary_task.id] = 0.6
            remaining = 0.4
            for task in background_tasks:
                attention_weights[task.id] = (
                    remaining / len(background_tasks)
                    if background_tasks else 0
                )

        # 估算上下文切换成本
        context_switch_cost_ms = 50 * len(background_tasks)  # 每个背景任务增加 50ms

        allocation = AttentionAllocation(
            primary_focus=primary_task.id,
            background_tasks=[t.id for t in background_tasks],
            attention_weights=attention_weights,
            context_switch_cost_ms=context_switch_cost_ms
        )

        self.attention_state = allocation
        return allocation

    def update_focus(self, new_task: Optional[Task]):
        """更新当前焦点"""
        if self.current_focus and new_task:
            # 记录上下文切换
            self.context_switch_history.append({
                "timestamp": time.time(),
                "from_task": self.current_focus.id,
                "to_task": new_task.id,
                "reason": "focus_change"
            })

        self.current_focus = new_task

    def get_focus_statistics(self) -> Dict[str, Any]:
        """获取焦点统计信息"""
        if not self.context_switch_history:
            return {
                "total_switches": 0,
                "avg_switch_interval_s": 0,
                "most_focused_task": None
            }

        total_switches = len(self.context_switch_history)

        # 计算平均切换间隔
        if total_switches > 1:
            first_time = self.context_switch_history[0]["timestamp"]
            last_time = self.context_switch_history[-1]["timestamp"]
            avg_interval = (last_time - first_time) / (total_switches - 1)
        else:
            avg_interval = 0

        # 统计任务焦点时间
        task_focus_time = {}
        for i in range(len(self.context_switch_history) - 1):
            task_id = self.context_switch_history[i].get("selected_task")
            if not task_id:
                continue

            start_time = self.context_switch_history[i]["timestamp"]
            end_time = self.context_switch_history[i + 1]["timestamp"]
            duration = end_time - start_time

            if task_id not in task_focus_time:
                task_focus_time[task_id] = 0
            task_focus_time[task_id] += duration

        # 找出焦点时间最长的任务
        most_focused = max(
            task_focus_time.items(),
            key=lambda x: x[1]
        )[0] if task_focus_time else None

        return {
            "total_switches": total_switches,
            "avg_switch_interval_s": avg_interval,
            "most_focused_task": most_focused,
            "task_focus_times": task_focus_time,
            "current_attention": self.attention_state.__dict__
        }

    def optimize_task_sequence(self, tasks: List[Task]) -> List[Task]:
        """
        优化任务执行顺序以减少上下文切换

        Args:
            tasks: 任务列表

        Returns:
            List[Task]: 优化后的任务顺序
        """
        if len(tasks) <= 1:
            return tasks

        # 按技能分组
        skill_groups: Dict[str, List[Task]] = {}
        for task in tasks:
            # 使用第一个技能作为分组键
            key = task.required_skills[0] if task.required_skills else "general"
            if key not in skill_groups:
                skill_groups[key] = []
            skill_groups[key].append(task)

        # 组内按优先级排序
        for skill, group_tasks in skill_groups.items():
            group_tasks.sort(key=lambda t: t.priority, reverse=True)

        # 重组任务列表（相同技能的任务连续执行）
        optimized_tasks = []
        for group_tasks in skill_groups.values():
            optimized_tasks.extend(group_tasks)

        return optimized_tasks
