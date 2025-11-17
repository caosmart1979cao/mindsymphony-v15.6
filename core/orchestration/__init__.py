"""
CrewAI-inspired Orchestration System

实现 Crew (自主协作) 和 Flow (精确控制) 双轨制编排能力
"""

from .types import ProcessType, AgentOutput, CrewOutput, FlowOutput, FlowState
from .agent import Agent
from .crew import Crew
from .flow import Flow, start, listen, router, or_, and_
from .hybrid_orchestrator import HybridOrchestrator

__all__ = [
    'ProcessType',
    'AgentOutput',
    'CrewOutput',
    'FlowOutput',
    'FlowState',
    'Agent',
    'Crew',
    'Flow',
    'start',
    'listen',
    'router',
    'or_',
    'and_',
    'HybridOrchestrator',
]
