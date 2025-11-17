"""
MindSymphony Core v15.6.2 - ACE Framework + CrewAI Edition

Core modules for the evolved MindSymphony system:
- memory: Hybrid memory system (AgentDB + ReasoningBank)
- fault_tolerance: Auto-recovery and fault tolerance
- skill_activation: Semantic skill routing
- performance: Performance monitoring and optimization
- learning: Reinforcement learning and pattern consolidation
- mcp_adapter: MCP protocol integration
- cognitive: ACE Framework cognitive architecture (NEW)
- orchestration: CrewAI-inspired orchestration system (NEW)
"""

__version__ = "15.6.2-ace-crewai"

# Optional imports - only import if dependencies are available
__all__ = []

try:
    from .memory import AgentDB, VectorIndex, ReasoningBank
    __all__.extend(['AgentDB', 'VectorIndex', 'ReasoningBank'])
except ImportError:
    pass

try:
    from .fault_tolerance.recovery_manager import RecoveryManager, HealthStatus
    __all__.extend(['RecoveryManager', 'HealthStatus'])
except ImportError:
    pass

try:
    from .skill_activation.semantic_router import SemanticRouter, IntentClassifier
    __all__.extend(['SemanticRouter', 'IntentClassifier'])
except ImportError:
    pass

try:
    from .performance.monitor import PerformanceMonitor, ExecutionTimer
    __all__.extend(['PerformanceMonitor', 'ExecutionTimer'])
except ImportError:
    pass

try:
    from .learning.pattern_learner import PatternLearner
    __all__.extend(['PatternLearner'])
except ImportError:
    pass

try:
    from .mcp_adapter.server import MCPServer
    __all__.extend(['MCPServer'])
except ImportError:
    pass
