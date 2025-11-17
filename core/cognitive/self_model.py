"""
ACE Layer 3: Self-Model (自我模型)

自我认知与能力模型，负责评估系统自身的能力和限制。
"""

import json
from typing import Dict, List, Any, Optional
from .types import CapabilityAssessment, PerformanceStatus


class SelfModel:
    """
    自我模型：知道自己能做什么、不能做什么

    核心职责：
    1. 评估系统能力和限制
    2. 从执行结果中学习，更新自我认知
    3. 提供准确的能力评估和成功概率预测
    4. 反思性能表现，识别优势和弱点
    """

    def __init__(self, skills_registry: Dict[str, Any]):
        """
        初始化自我模型

        Args:
            skills_registry: 技能注册表
        """
        self.skills_registry = skills_registry
        self.capabilities = self._assess_capabilities(skills_registry)
        self.limitations = self._identify_limitations()
        self.current_state = {
            "load": 0.0,  # 0-1
            "health": "healthy",
            "active_tasks": 0,
            "memory_usage_mb": 0
        }
        self.confidence_levels = {}  # skill_name -> confidence (0-1)
        self.performance_history = []

    def _assess_capabilities(self, skills_registry: Dict[str, Any]) -> Dict[str, Any]:
        """评估系统能力"""
        capabilities = {
            "skills": {},
            "domains": set(),
            "limitations": []
        }

        for skill_name, skill_data in skills_registry.items():
            capabilities["skills"][skill_name] = {
                "available": True,
                "reliability": skill_data.get("reliability", 0.9),
                "avg_execution_time_ms": skill_data.get("avg_time_ms", 1000),
                "success_rate": skill_data.get("success_rate", 0.95)
            }

            # 识别领域
            domain = skill_data.get("domain", "general")
            capabilities["domains"].add(domain)

        return capabilities

    def _identify_limitations(self) -> List[str]:
        """识别系统限制"""
        return [
            "无法访问互联网（除非明确配置）",
            "无法直接修改硬件",
            "需要用户批准才能执行高风险操作",
            "依赖可用技能集合",
            "受计算资源限制"
        ]

    def can_accomplish(self, task: Dict[str, Any]) -> CapabilityAssessment:
        """
        评估是否能完成任务

        Args:
            task: 任务描述

        Returns:
            CapabilityAssessment: 能力评估结果
        """
        required_skills = task.get("required_skills", [])
        task_complexity = task.get("complexity", "medium")
        task_description = task.get("description", "")

        # 1. 检查所需技能是否可用
        available_skills = []
        missing_skills = []

        for skill in required_skills:
            if skill in self.capabilities["skills"]:
                available_skills.append(skill)
            else:
                missing_skills.append(skill)

        # 2. 计算成功概率
        success_probability = self._calculate_success_probability(
            available_skills,
            missing_skills,
            task_complexity
        )

        # 3. 估算执行时间
        estimated_time_ms = self._estimate_execution_time(
            available_skills,
            task_complexity
        )

        # 4. 识别潜在障碍
        obstacles = self._identify_obstacles(task, missing_skills)

        # 5. 确定是否能完成
        can_accomplish = (
            len(missing_skills) == 0 and
            success_probability > 0.6 and
            self.current_state["load"] < 0.9
        )

        return CapabilityAssessment(
            can_accomplish=can_accomplish,
            success_probability=success_probability,
            required_skills=required_skills,
            available_skills=available_skills,
            missing_skills=missing_skills,
            estimated_time_ms=estimated_time_ms,
            potential_obstacles=obstacles,
            confidence_level=success_probability
        )

    def _calculate_success_probability(
        self,
        available_skills: List[str],
        missing_skills: List[str],
        task_complexity: str
    ) -> float:
        """计算成功概率"""
        if missing_skills:
            # 有缺失技能，概率大幅下降
            base_probability = 0.3
        else:
            base_probability = 0.9

        # 根据技能可靠性调整
        if available_skills:
            avg_reliability = sum(
                self.capabilities["skills"][skill]["reliability"]
                for skill in available_skills
                if skill in self.capabilities["skills"]
            ) / len(available_skills)
            base_probability *= avg_reliability

        # 根据复杂度调整
        complexity_factors = {
            "low": 1.0,
            "medium": 0.85,
            "high": 0.7
        }
        base_probability *= complexity_factors.get(task_complexity, 0.85)

        # 根据当前负载调整
        load_factor = 1.0 - (self.current_state["load"] * 0.2)
        base_probability *= load_factor

        return min(1.0, max(0.0, base_probability))

    def _estimate_execution_time(
        self,
        available_skills: List[str],
        task_complexity: str
    ) -> Optional[int]:
        """估算执行时间（毫秒）"""
        if not available_skills:
            return None

        # 基础时间：技能平均执行时间之和
        base_time = sum(
            self.capabilities["skills"][skill]["avg_execution_time_ms"]
            for skill in available_skills
            if skill in self.capabilities["skills"]
        )

        # 复杂度系数
        complexity_multipliers = {
            "low": 1.0,
            "medium": 1.5,
            "high": 2.5
        }
        multiplier = complexity_multipliers.get(task_complexity, 1.5)

        return int(base_time * multiplier)

    def _identify_obstacles(
        self,
        task: Dict[str, Any],
        missing_skills: List[str]
    ) -> List[str]:
        """识别潜在障碍"""
        obstacles = []

        if missing_skills:
            obstacles.append(
                f"缺少必需技能：{', '.join(missing_skills)}"
            )

        if self.current_state["load"] > 0.8:
            obstacles.append("当前系统负载较高，可能影响性能")

        if task.get("requires_user_approval") and not task.get("user_approved"):
            obstacles.append("需要用户批准才能执行")

        # 检查资源限制
        if task.get("estimated_memory_mb", 0) > 1000:
            obstacles.append("任务可能需要大量内存")

        return obstacles

    def update_self_knowledge(self, execution_result: Dict[str, Any]):
        """
        从执行结果中学习，更新自我认知

        Args:
            execution_result: 执行结果
        """
        skill_name = execution_result.get("skill_name")
        success = execution_result.get("success", False)
        execution_time_ms = execution_result.get("execution_time_ms", 0)

        if skill_name and skill_name in self.capabilities["skills"]:
            skill_data = self.capabilities["skills"][skill_name]

            # 更新成功率（移动平均）
            old_success_rate = skill_data["success_rate"]
            skill_data["success_rate"] = (
                old_success_rate * 0.9 +
                (1.0 if success else 0.0) * 0.1
            )

            # 更新平均执行时间
            old_avg_time = skill_data["avg_execution_time_ms"]
            skill_data["avg_execution_time_ms"] = int(
                old_avg_time * 0.9 + execution_time_ms * 0.1
            )

            # 更新可靠性
            if success:
                skill_data["reliability"] = min(1.0, skill_data["reliability"] + 0.01)
            else:
                skill_data["reliability"] = max(0.0, skill_data["reliability"] - 0.05)

            # 更新置信度
            self.confidence_levels[skill_name] = skill_data["reliability"]

        # 记录性能历史
        self.performance_history.append(execution_result)

        # 保持历史记录在合理范围内
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]

    def reflect_on_performance(self) -> Dict[str, Any]:
        """反思性能表现"""
        if not self.performance_history:
            return {
                "status": "no_data",
                "message": "暂无执行历史数据"
            }

        recent_executions = self.performance_history[-100:]

        # 计算总体成功率
        success_count = sum(1 for r in recent_executions if r.get("success"))
        overall_success_rate = success_count / len(recent_executions)

        # 识别表现最好的技能
        skill_performance = {}
        for result in recent_executions:
            skill_name = result.get("skill_name")
            if skill_name:
                if skill_name not in skill_performance:
                    skill_performance[skill_name] = {"successes": 0, "total": 0}
                skill_performance[skill_name]["total"] += 1
                if result.get("success"):
                    skill_performance[skill_name]["successes"] += 1

        best_skills = sorted(
            skill_performance.items(),
            key=lambda x: x[1]["successes"] / x[1]["total"] if x[1]["total"] > 0 else 0,
            reverse=True
        )[:5]

        # 识别需要改进的技能
        worst_skills = sorted(
            skill_performance.items(),
            key=lambda x: x[1]["successes"] / x[1]["total"] if x[1]["total"] > 0 else 0
        )[:5]

        # 性能状态
        if overall_success_rate > 0.95:
            status = PerformanceStatus.EXCELLENT
        elif overall_success_rate > 0.85:
            status = PerformanceStatus.GOOD
        elif overall_success_rate > 0.7:
            status = PerformanceStatus.DEGRADED
        else:
            status = PerformanceStatus.POOR

        return {
            "status": status.value,
            "overall_success_rate": overall_success_rate,
            "total_executions": len(recent_executions),
            "best_performing_skills": [
                {
                    "skill": skill,
                    "success_rate": perf["successes"] / perf["total"]
                }
                for skill, perf in best_skills if perf["total"] >= 3
            ],
            "needs_improvement": [
                {
                    "skill": skill,
                    "success_rate": perf["successes"] / perf["total"]
                }
                for skill, perf in worst_skills if perf["total"] >= 3
            ],
            "recommendations": self._generate_improvement_recommendations(
                overall_success_rate,
                worst_skills
            )
        }

    def _generate_improvement_recommendations(
        self,
        success_rate: float,
        worst_skills: List
    ) -> List[str]:
        """生成改进建议"""
        recommendations = []

        if success_rate < 0.8:
            recommendations.append(
                "建议：检查并优化经常失败的技能"
            )

        if worst_skills:
            for skill, perf in worst_skills[:3]:
                if perf["total"] >= 3 and perf["successes"] / perf["total"] < 0.7:
                    recommendations.append(
                        f"建议：重点改进技能 '{skill}' 的可靠性"
                    )

        if self.current_state["load"] > 0.8:
            recommendations.append(
                "建议：减少并发任务数量以降低系统负载"
            )

        return recommendations

    def update_current_state(self, state_updates: Dict[str, Any]):
        """更新当前状态"""
        self.current_state.update(state_updates)

    def get_capabilities_summary(self) -> Dict[str, Any]:
        """获取能力摘要"""
        return {
            "total_skills": len(self.capabilities["skills"]),
            "domains": list(self.capabilities["domains"]),
            "limitations": self.limitations,
            "current_state": self.current_state,
            "avg_confidence": (
                sum(self.confidence_levels.values()) / len(self.confidence_levels)
                if self.confidence_levels else 0.0
            )
        }
