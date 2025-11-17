"""
ACE Framework Cognitive Architecture Integration

六层认知架构：
1. Aspirational Core - 道德核心
2. Strategic Planner - 战略规划
3. Self-Model - 自我模型
4. Executive Function - 执行功能
5. Cognitive Control - 认知控制
6. Task Prosecution - 技能执行 (现有 Skills 层)
"""

from .types import (
    EthicalJudgment,
    Strategy,
    Goal,
    CapabilityAssessment,
    ExecutionPlan,
    Task,
    ResourceAllocation
)
from .aspirational_core import AspirationalCore
from .strategic_planner import StrategicPlanner
from .self_model import SelfModel
from .executive_function import ExecutiveFunction
from .cognitive_control import CognitiveControl

__all__ = [
    'EthicalJudgment',
    'Strategy',
    'Goal',
    'CapabilityAssessment',
    'ExecutionPlan',
    'Task',
    'ResourceAllocation',
    'AspirationalCore',
    'StrategicPlanner',
    'SelfModel',
    'ExecutiveFunction',
    'CognitiveControl',
]
