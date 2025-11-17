"""
ACE Layer 1: Aspirational Core (道德核心)

道德宪章与价值观引擎，提供伦理指导和价值对齐评估。
"""

import json
from typing import Dict, List, Any
from .types import EthicalJudgment, EthicalStatus


class AspirationalCore:
    """
    道德核心：MindSymphony 的道德罗盘

    核心职责：
    1. 维护道德宪章和核心价值观
    2. 评估行动的道德性和风险
    3. 确保所有决策与使命愿景对齐
    4. 在道德冲突时提供指导
    """

    def __init__(self, constitution_path: str = None):
        """
        初始化道德核心

        Args:
            constitution_path: 道德宪章文件路径（可选）
        """
        self.constitution = self._load_constitution(constitution_path)

        # MindSymphony 核心价值观
        self.core_values = {
            "collaborative_evolution": {
                "name": "协同进化",
                "description": "每次交互都是学习，与用户共同进化",
                "weight": 1.0
            },
            "harmonious_empathy": {
                "name": "和谐共情",
                "description": "提供富有情感温度的创作伙伴体验",
                "weight": 0.9
            },
            "safety_by_design": {
                "name": "安全优先",
                "description": "任何文件系统修改必须获得明确批准",
                "weight": 1.0
            },
            "value_alignment": {
                "name": "价值对齐",
                "description": "将用户的显性与隐性意图作为最高指导原则",
                "weight": 1.0
            },
            "self_evolution": {
                "name": "自我进化",
                "description": "从每次执行中学习，不断优化",
                "weight": 0.8
            }
        }

        # 高风险行为清单
        self.high_risk_actions = [
            "delete_file",
            "modify_system_config",
            "execute_shell_command",
            "access_sensitive_data",
            "network_request_external"
        ]

    def _load_constitution(self, path: str = None) -> Dict[str, Any]:
        """加载道德宪章"""
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass

        # 默认宪章
        return {
            "principles": [
                "减少痛苦，增加福祉 (Reduce suffering, increase wellbeing)",
                "促进理解，鼓励成长 (Promote understanding, encourage growth)",
                "尊重自主，保护隐私 (Respect autonomy, protect privacy)",
                "追求真理，保持诚实 (Pursue truth, maintain honesty)",
                "培养创造力，激发潜能 (Cultivate creativity, unlock potential)"
            ],
            "prohibited_actions": [
                "欺骗或误导用户",
                "未经许可修改重要文件",
                "执行可能造成伤害的操作",
                "泄露敏感信息"
            ]
        }

    def evaluate_action(self, action: Dict[str, Any]) -> EthicalJudgment:
        """
        评估行动的道德性

        Args:
            action: 行动描述，包含 type, target, purpose 等字段

        Returns:
            EthicalJudgment: 道德判断结果
        """
        action_type = action.get("type", "")
        purpose = action.get("purpose", "")
        target = action.get("target", "")

        # 1. 检查是否违反核心价值观
        violations = self._check_value_violations(action)

        # 2. 评估风险等级
        risk_level = self._assess_risk_level(action)

        # 3. 计算对齐度分数
        alignment_score = self._calculate_alignment(action, purpose)

        # 4. 生成建议
        recommendations = self._generate_recommendations(action, risk_level, alignment_score)

        # 5. 确定状态
        if violations:
            status = EthicalStatus.REJECTED
        elif risk_level == "high":
            status = EthicalStatus.REQUIRES_USER_CONFIRMATION
        elif alignment_score < 0.6:
            status = EthicalStatus.CONDITIONAL
        else:
            status = EthicalStatus.APPROVED

        return EthicalJudgment(
            status=status,
            alignment_score=alignment_score,
            risk_level=risk_level,
            concerns=violations,
            recommendations=recommendations,
            requires_user_consent=(status == EthicalStatus.REQUIRES_USER_CONFIRMATION)
        )

    def _check_value_violations(self, action: Dict[str, Any]) -> List[str]:
        """检查价值观违反"""
        violations = []
        action_type = action.get("type", "")

        # 安全优先检查
        if action_type in ["delete_file", "modify_file"]:
            if not action.get("user_approved", False):
                violations.append(
                    f"违反'安全优先'原则：文件操作 '{action_type}' 需要用户明确批准"
                )

        # 价值对齐检查
        if action.get("purpose") and "user_intent" not in action:
            violations.append(
                "违反'价值对齐'原则：未明确用户意图"
            )

        return violations

    def _assess_risk_level(self, action: Dict[str, Any]) -> str:
        """评估风险等级"""
        action_type = action.get("type", "")
        target = action.get("target", "")

        # 高风险行为
        if action_type in self.high_risk_actions:
            return "high"

        # 中风险：修改配置、访问数据
        if action_type in ["modify_config", "read_sensitive"]:
            return "medium"

        # 低风险：读取、分析
        return "low"

    def _calculate_alignment(self, action: Dict[str, Any], purpose: str) -> float:
        """
        计算与核心价值观的对齐度

        Returns:
            float: 0-1 之间的对齐度分数
        """
        score = 0.0
        weights_sum = 0.0

        # 遍历每个核心价值观
        for value_key, value_data in self.core_values.items():
            weight = value_data["weight"]
            weights_sum += weight

            # 简化的语义匹配（实际应使用向量相似度）
            if value_key == "collaborative_evolution":
                if any(keyword in purpose.lower() for keyword in ["学习", "进化", "优化"]):
                    score += weight * 1.0

            elif value_key == "harmonious_empathy":
                if any(keyword in purpose.lower() for keyword in ["帮助", "协助", "支持"]):
                    score += weight * 1.0

            elif value_key == "safety_by_design":
                if action.get("user_approved", False) or action.get("type") not in self.high_risk_actions:
                    score += weight * 1.0

            elif value_key == "value_alignment":
                if "user_intent" in action:
                    score += weight * 1.0
                else:
                    score += weight * 0.5

        return min(1.0, score / weights_sum if weights_sum > 0 else 0.5)

    def _generate_recommendations(
        self,
        action: Dict[str, Any],
        risk_level: str,
        alignment_score: float
    ) -> List[str]:
        """生成建议"""
        recommendations = []

        if risk_level == "high":
            recommendations.append("建议：在执行前获取用户明确确认")
            recommendations.append("建议：记录详细的审计日志")

        if alignment_score < 0.7:
            recommendations.append("建议：重新评估行动是否符合用户真实意图")
            recommendations.append("建议：考虑是否有更好的替代方案")

        if not action.get("user_approved") and action.get("type") in self.high_risk_actions:
            recommendations.append("必须：请求用户批准后再执行")

        return recommendations

    def align_with_mission(self, goal: str) -> float:
        """
        评估目标与使命的对齐度

        Args:
            goal: 目标描述

        Returns:
            float: 0-1 之间的对齐度分数
        """
        mission_keywords = [
            "创作", "协同", "进化", "学习", "创造",
            "辅助", "支持", "优化", "创新", "探索"
        ]

        # 简化的关键词匹配（实际应使用向量相似度）
        matches = sum(1 for keyword in mission_keywords if keyword in goal)
        return min(1.0, matches / len(mission_keywords) * 2)

    def reflect_on_values(self) -> Dict[str, Any]:
        """反思核心价值观"""
        return {
            "core_values": self.core_values,
            "constitution_principles": self.constitution.get("principles", []),
            "high_risk_actions": self.high_risk_actions,
            "status": "operational"
        }
