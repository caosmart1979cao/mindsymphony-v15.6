"""
Hybrid Orchestrator: 智能选择 Crew 或 Flow

根据任务特征自动选择最优编排模式
"""

from typing import Dict, Any, Optional
from .crew import Crew
from .flow import Flow


class HybridOrchestrator:
    """
    混合编排器：结合 Crew 的自主性和 Flow 的精确控制

    决策逻辑：
    - 高复杂度 + 低控制需求 → Crew (自主协作)
    - 高控制需求 → Flow (精确控制)
    - 混合场景 → Flow 中嵌入 Crew
    """

    def __init__(self, verbose: bool = False):
        """
        初始化混合编排器

        Args:
            verbose: 是否输出详细日志
        """
        self.crews: Dict[str, Crew] = {}
        self.flows: Dict[str, Flow] = {}
        self.verbose = verbose

        # 决策历史
        self.decision_history: list = []

    def register_crew(self, crew: Crew):
        """注册 Crew"""
        self.crews[crew.name] = crew
        if self.verbose:
            print(f"[HybridOrchestrator] 注册 Crew: {crew.name}")

    def register_flow(self, flow: Flow):
        """注册 Flow"""
        self.flows[flow.name] = flow
        if self.verbose:
            print(f"[HybridOrchestrator] 注册 Flow: {flow.name}")

    def orchestrate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        智能编排：自动选择 Crew 或 Flow

        Args:
            request: 请求描述，包含：
                - description: 任务描述
                - complexity: 复杂度 (可选)
                - control_requirement: 控制需求 (可选)
                - preferred_mode: 偏好模式 (可选)

        Returns:
            Dict: 编排结果
        """
        description = request.get("description", "")

        # 1. 分析请求特征
        complexity = self._assess_complexity(request)
        control_need = self._assess_control_requirement(request)

        # 2. 决策编排模式
        mode = self._decide_orchestration_mode(
            complexity,
            control_need,
            request.get("preferred_mode")
        )

        # 3. 记录决策
        self.decision_history.append({
            "request": description,
            "complexity": complexity,
            "control_need": control_need,
            "chosen_mode": mode,
            "reason": self._explain_decision(complexity, control_need, mode)
        })

        if self.verbose:
            print(f"\n[HybridOrchestrator] 决策:")
            print(f"  复杂度: {complexity:.2f}")
            print(f"  控制需求: {control_need:.2f}")
            print(f"  选择模式: {mode}")
            print(f"  理由: {self.decision_history[-1]['reason']}\n")

        # 4. 执行编排
        if mode == "crew":
            return self._orchestrate_with_crew(request)
        elif mode == "flow":
            return self._orchestrate_with_flow(request)
        elif mode == "hybrid":
            return self._orchestrate_hybrid(request)
        else:
            raise ValueError(f"未知编排模式: {mode}")

    def _assess_complexity(self, request: Dict[str, Any]) -> float:
        """
        评估任务复杂度 (0-1)

        考虑因素：
        - 任务数量
        - 涉及的领域数量
        - 任务间依赖关系
        - 明确指定的复杂度
        """
        if "complexity" in request:
            complexity_map = {"low": 0.3, "medium": 0.6, "high": 0.9}
            return complexity_map.get(request["complexity"], 0.6)

        description = request.get("description", "").lower()

        complexity = 0.5  # 基础值

        # 关键词匹配
        if any(kw in description for kw in ["复杂", "系统", "端到端", "全面"]):
            complexity += 0.2

        if any(kw in description for kw in ["多个", "集成", "协调"]):
            complexity += 0.1

        if any(kw in description for kw in ["简单", "单一", "快速"]):
            complexity -= 0.2

        # 任务数量
        tasks = request.get("tasks", [])
        if len(tasks) > 5:
            complexity += 0.2
        elif len(tasks) > 10:
            complexity += 0.3

        return min(1.0, max(0.0, complexity))

    def _assess_control_requirement(self, request: Dict[str, Any]) -> float:
        """
        评估控制需求 (0-1)

        考虑因素：
        - 是否需要精确的执行顺序
        - 是否有复杂的条件逻辑
        - 是否需要严格的错误处理
        """
        if "control_requirement" in request:
            control_map = {"low": 0.3, "medium": 0.6, "high": 0.9}
            return control_map.get(request["control_requirement"], 0.6)

        description = request.get("description", "").lower()

        control_need = 0.5  # 基础值

        # 关键词匹配
        if any(kw in description for kw in ["严格", "精确", "顺序", "流程", "步骤"]):
            control_need += 0.2

        if any(kw in description for kw in ["条件", "分支", "判断", "路由"]):
            control_need += 0.2

        if any(kw in description for kw in ["灵活", "自主", "协作"]):
            control_need -= 0.2

        # 部署和关键任务需要高控制
        if any(kw in description for kw in ["部署", "发布", "上线"]):
            control_need += 0.3

        return min(1.0, max(0.0, control_need))

    def _decide_orchestration_mode(
        self,
        complexity: float,
        control_need: float,
        preferred_mode: Optional[str] = None
    ) -> str:
        """
        决策编排模式

        决策矩阵：
        - complexity > 0.7 AND control_need < 0.5 → crew
        - control_need > 0.7 → flow
        - 其他 → hybrid
        """
        if preferred_mode in ["crew", "flow", "hybrid"]:
            return preferred_mode

        if complexity > 0.7 and control_need < 0.5:
            return "crew"

        if control_need > 0.7:
            return "flow"

        return "hybrid"

    def _explain_decision(
        self,
        complexity: float,
        control_need: float,
        mode: str
    ) -> str:
        """解释决策理由"""
        if mode == "crew":
            return f"高复杂度 ({complexity:.2f}) + 低控制需求 ({control_need:.2f}) → 使用 Crew 自主协作"
        elif mode == "flow":
            return f"高控制需求 ({control_need:.2f}) → 使用 Flow 精确控制"
        elif mode == "hybrid":
            return f"平衡复杂度 ({complexity:.2f}) 和控制需求 ({control_need:.2f}) → 使用混合模式"
        else:
            return "未知理由"

    def _orchestrate_with_crew(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """使用 Crew 编排"""
        crew_name = request.get("crew_name")

        if crew_name and crew_name in self.crews:
            crew = self.crews[crew_name]
        elif self.crews:
            # 选择第一个可用的 crew
            crew = list(self.crews.values())[0]
        else:
            return {
                "success": False,
                "error": "没有可用的 Crew",
                "mode": "crew"
            }

        result = crew.kickoff(request.get("inputs", {}))

        return {
            "success": result.success,
            "mode": "crew",
            "crew_name": crew.name,
            "output": result
        }

    def _orchestrate_with_flow(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """使用 Flow 编排"""
        flow_name = request.get("flow_name")

        if flow_name and flow_name in self.flows:
            flow = self.flows[flow_name]
        elif self.flows:
            # 选择第一个可用的 flow
            flow = list(self.flows.values())[0]
        else:
            return {
                "success": False,
                "error": "没有可用的 Flow",
                "mode": "flow"
            }

        result = flow.run(request.get("inputs", {}))

        return {
            "success": result.success,
            "mode": "flow",
            "flow_name": flow.name,
            "output": result
        }

    def _orchestrate_hybrid(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """混合编排：Flow 中嵌入 Crew"""
        # 简化实现：优先使用 Flow，如果有 Crew 则注册到 Flow 中
        if not self.flows:
            return self._orchestrate_with_crew(request)

        flow = list(self.flows.values())[0]

        # 将所有 Crew 注册到 Flow
        for crew_name, crew in self.crews.items():
            flow.register_crew(crew_name, crew)

        result = flow.run(request.get("inputs", {}))

        return {
            "success": result.success,
            "mode": "hybrid",
            "flow_name": flow.name,
            "registered_crews": list(self.crews.keys()),
            "output": result
        }

    def get_orchestration_stats(self) -> Dict[str, Any]:
        """获取编排统计信息"""
        if not self.decision_history:
            return {
                "total_requests": 0,
                "mode_distribution": {},
                "avg_complexity": 0,
                "avg_control_need": 0
            }

        total = len(self.decision_history)

        # 模式分布
        mode_counts = {}
        for decision in self.decision_history:
            mode = decision["chosen_mode"]
            mode_counts[mode] = mode_counts.get(mode, 0) + 1

        mode_distribution = {
            mode: count / total for mode, count in mode_counts.items()
        }

        # 平均复杂度和控制需求
        avg_complexity = sum(d["complexity"] for d in self.decision_history) / total
        avg_control_need = sum(d["control_need"] for d in self.decision_history) / total

        return {
            "total_requests": total,
            "mode_distribution": mode_distribution,
            "avg_complexity": avg_complexity,
            "avg_control_need": avg_control_need,
            "registered_crews": len(self.crews),
            "registered_flows": len(self.flows)
        }
