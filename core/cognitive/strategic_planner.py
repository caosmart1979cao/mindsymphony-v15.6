"""
ACE Layer 2: Strategic Planner (战略规划器)

全局战略规划引擎，负责长期目标设定和战略路线图制定。
"""

import time
from typing import Dict, List, Any, Optional
from .types import Strategy, Goal
from .aspirational_core import AspirationalCore


class StrategicPlanner:
    """
    战略规划器：从战术到战略的提升

    核心职责：
    1. 分析用户请求和上下文，制定高层战略
    2. 设定阶段性目标和里程碑
    3. 根据反馈动态调整战略
    4. 确保战略符合道德核心的指导
    """

    def __init__(self, aspirational_core: AspirationalCore):
        """
        初始化战略规划器

        Args:
            aspirational_core: 道德核心引用
        """
        self.aspirational = aspirational_core
        self.long_term_goals: List[Goal] = []
        self.active_strategy: Optional[Strategy] = None
        self.context_history: List[Dict[str, Any]] = []

    def formulate_strategy(
        self,
        user_request: str,
        context: Dict[str, Any]
    ) -> Strategy:
        """
        制定高层战略

        Args:
            user_request: 用户请求描述
            context: 上下文信息（历史、环境、资源等）

        Returns:
            Strategy: 战略计划
        """
        # 1. 分析用户请求，识别核心意图
        core_intent = self._analyze_intent(user_request, context)

        # 2. 分解为阶段性目标
        goals = self._decompose_into_goals(core_intent, context)

        # 3. 确保与道德核心对齐
        for goal in goals:
            alignment = self.aspirational.align_with_mission(goal.description)
            if alignment < 0.5:
                # 重新评估目标
                goal.priority = max(1, goal.priority - 2)

        # 4. 设定里程碑
        milestones = self._create_milestones(goals)

        # 5. 规划时间线
        timeline = self._plan_timeline(goals, milestones)

        # 6. 识别所需资源
        resources_required = self._identify_resources(goals)

        # 7. 风险评估
        risks = self._assess_risks(goals, context)

        # 8. 计算总体道德对齐度
        ethical_alignment = self._calculate_strategy_alignment(goals)

        strategy = Strategy(
            goals=goals,
            milestones=milestones,
            timeline=timeline,
            resources_required=resources_required,
            risks=risks,
            ethical_alignment=ethical_alignment
        )

        self.active_strategy = strategy
        self.context_history.append({
            "timestamp": time.time(),
            "user_request": user_request,
            "context": context,
            "strategy": strategy
        })

        return strategy

    def _analyze_intent(
        self,
        user_request: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """分析用户意图"""
        # 识别请求类型
        request_types = {
            "research": ["研究", "分析", "探索", "调查"],
            "creation": ["创建", "生成", "制作", "设计"],
            "optimization": ["优化", "改进", "提升", "加速"],
            "deployment": ["部署", "发布", "上线"],
            "documentation": ["文档", "说明", "记录"]
        }

        detected_types = []
        for req_type, keywords in request_types.items():
            if any(keyword in user_request for keyword in keywords):
                detected_types.append(req_type)

        # 识别复杂度
        complexity = self._estimate_complexity(user_request, context)

        return {
            "types": detected_types or ["general"],
            "complexity": complexity,
            "original_request": user_request,
            "context_hints": context.get("hints", [])
        }

    def _estimate_complexity(
        self,
        user_request: str,
        context: Dict[str, Any]
    ) -> str:
        """估算任务复杂度"""
        complexity_indicators = {
            "high": ["系统", "完整", "端到端", "全面", "复杂"],
            "medium": ["多个", "集成", "协调"],
            "low": ["简单", "单一", "快速"]
        }

        for level, indicators in complexity_indicators.items():
            if any(ind in user_request for ind in indicators):
                return level

        # 根据上下文判断
        if context.get("previous_failures", 0) > 2:
            return "high"

        return "medium"

    def _decompose_into_goals(
        self,
        core_intent: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[Goal]:
        """分解为阶段性目标"""
        goals = []
        request_types = core_intent["types"]
        complexity = core_intent["complexity"]

        # 根据请求类型创建目标
        if "research" in request_types:
            goals.append(Goal(
                description="深度研究并收集相关信息",
                priority=8,
                success_criteria=[
                    "收集至少 5 个高质量信息源",
                    "提取关键洞察和模式",
                    "生成结构化研究报告"
                ]
            ))

        if "creation" in request_types:
            goals.append(Goal(
                description="创建高质量的输出成果",
                priority=9,
                success_criteria=[
                    "符合用户需求和期望",
                    "通过质量检查",
                    "提供清晰的文档"
                ]
            ))

        if "optimization" in request_types:
            goals.append(Goal(
                description="优化性能和效率",
                priority=7,
                success_criteria=[
                    "识别性能瓶颈",
                    "实施优化措施",
                    "验证性能提升"
                ]
            ))

        if "deployment" in request_types:
            goals.append(Goal(
                description="安全可靠地部署",
                priority=10,
                success_criteria=[
                    "通过所有测试",
                    "建立监控和告警",
                    "提供回滚方案"
                ],
                constraints=["需要用户明确批准"]
            ))

        # 如果没有特定类型，创建通用目标
        if not goals:
            goals.append(Goal(
                description="完成用户请求",
                priority=8,
                success_criteria=["满足用户需求", "提供高质量输出"]
            ))

        # 根据复杂度调整
        if complexity == "high":
            # 添加额外的质量保证目标
            goals.append(Goal(
                description="确保质量和可靠性",
                priority=9,
                success_criteria=[
                    "执行全面测试",
                    "验证所有边界条件",
                    "提供详细文档"
                ]
            ))

        return goals

    def _create_milestones(self, goals: List[Goal]) -> List[Dict[str, Any]]:
        """创建里程碑"""
        milestones = []

        for i, goal in enumerate(goals, 1):
            milestones.append({
                "id": f"milestone_{i}",
                "description": f"完成目标：{goal.description}",
                "goal_index": i - 1,
                "checkpoint": True,
                "success_criteria": goal.success_criteria
            })

        # 添加最终里程碑
        milestones.append({
            "id": "final_milestone",
            "description": "所有目标达成，战略完成",
            "goal_index": len(goals),
            "checkpoint": True,
            "success_criteria": ["所有目标成功完成", "用户满意度 >= 4.0"]
        })

        return milestones

    def _plan_timeline(
        self,
        goals: List[Goal],
        milestones: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """规划时间线"""
        timeline = {}

        # 估算每个阶段的时间
        for i, goal in enumerate(goals):
            phase_name = f"phase_{i + 1}"
            # 简化的时间估算（实际应根据历史数据）
            estimated_duration = "短期" if goal.priority < 7 else "中期"
            timeline[phase_name] = estimated_duration

        return timeline

    def _identify_resources(self, goals: List[Goal]) -> List[str]:
        """识别所需资源"""
        resources = set()

        for goal in goals:
            desc = goal.description.lower()

            if "研究" in desc or "分析" in desc:
                resources.add("knowledge-explorer")
                resources.add("research_crew")

            if "创建" in desc or "生成" in desc:
                resources.add("concept-singularity")
                resources.add("creation_crew")

            if "部署" in desc:
                resources.add("agent-deployer")
                resources.add("deployment_crew")

            if "优化" in desc:
                resources.add("code-refactoring-workflow")

        # 添加通用资源
        resources.add("performance_monitor")
        resources.add("recovery_manager")

        return list(resources)

    def _assess_risks(
        self,
        goals: List[Goal],
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """风险评估"""
        risks = []

        # 复杂度风险
        high_priority_goals = [g for g in goals if g.priority >= 9]
        if len(high_priority_goals) > 3:
            risks.append({
                "type": "complexity",
                "severity": "medium",
                "description": "多个高优先级目标可能导致资源竞争",
                "mitigation": "按优先级顺序执行，避免并行"
            })

        # 依赖风险
        if context.get("external_dependencies"):
            risks.append({
                "type": "dependency",
                "severity": "medium",
                "description": "依赖外部资源或服务",
                "mitigation": "实施降级策略和缓存机制"
            })

        # 时间风险
        if any(g.deadline for g in goals):
            risks.append({
                "type": "deadline",
                "severity": "high",
                "description": "存在时间约束",
                "mitigation": "优先处理有截止日期的目标"
            })

        return risks

    def _calculate_strategy_alignment(self, goals: List[Goal]) -> float:
        """计算战略的总体道德对齐度"""
        if not goals:
            return 0.5

        total_alignment = sum(
            self.aspirational.align_with_mission(goal.description)
            for goal in goals
        )

        return total_alignment / len(goals)

    def adapt_strategy(self, feedback: Dict[str, Any]) -> Strategy:
        """
        根据反馈调整战略

        Args:
            feedback: 反馈信息（成功/失败、性能指标等）

        Returns:
            Strategy: 调整后的战略
        """
        if not self.active_strategy:
            raise ValueError("没有活跃的战略可供调整")

        # 分析反馈
        success_rate = feedback.get("success_rate", 1.0)
        performance = feedback.get("performance_status", "good")
        user_satisfaction = feedback.get("user_satisfaction", 4.0)

        # 调整目标优先级
        if success_rate < 0.8:
            # 降低复杂目标的优先级
            for goal in self.active_strategy.goals:
                if len(goal.success_criteria) > 3:
                    goal.priority = max(1, goal.priority - 1)

        # 调整资源分配
        if performance == "degraded":
            # 增加性能监控资源
            if "performance_monitor" not in self.active_strategy.resources_required:
                self.active_strategy.resources_required.append("performance_monitor")

        # 调整风险评估
        if user_satisfaction < 3.0:
            self.active_strategy.risks.append({
                "type": "user_satisfaction",
                "severity": "high",
                "description": "用户满意度低于预期",
                "mitigation": "重新评估用户需求，调整执行方式"
            })

        return self.active_strategy

    def get_current_strategy(self) -> Optional[Strategy]:
        """获取当前活跃的战略"""
        return self.active_strategy

    def get_strategy_history(self) -> List[Dict[str, Any]]:
        """获取战略历史"""
        return self.context_history
