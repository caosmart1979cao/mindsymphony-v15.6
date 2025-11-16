"""
MindSymphony Core v15.6 - Evolution Edition

Core modules for the evolved MindSymphony system:
- memory: Hybrid memory system (AgentDB + ReasoningBank)
- fault_tolerance: Auto-recovery and fault tolerance
- skill_activation: Semantic skill routing
- performance: Performance monitoring and optimization
- learning: Reinforcement learning and pattern consolidation
- mcp_adapter: MCP protocol integration
"""

__version__ = "15.6.0-evolved"

from .memory import AgentDB, VectorIndex, ReasoningBank
from .fault_tolerance.recovery_manager import RecoveryManager, HealthStatus
from .skill_activation.semantic_router import SemanticRouter, IntentClassifier
from .performance.monitor import PerformanceMonitor, ExecutionTimer
from .learning.pattern_learner import PatternLearner
from .mcp_adapter.server import MCPServer

__all__ = [
    'AgentDB',
    'VectorIndex',
    'ReasoningBank',
    'RecoveryManager',
    'HealthStatus',
    'SemanticRouter',
    'IntentClassifier',
    'PerformanceMonitor',
    'ExecutionTimer',
    'PatternLearner',
    'MCPServer'
]
