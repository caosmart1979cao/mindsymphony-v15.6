"""
Type definitions for ACE Framework cognitive architecture
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class EthicalStatus(Enum):
    """道德评估状态"""
    APPROVED = "approved"
    CONDITIONAL = "conditional"
    REJECTED = "rejected"
    REQUIRES_USER_CONFIRMATION = "requires_user_confirmation"


class PerformanceStatus(Enum):
    """性能状态"""
    EXCELLENT = "excellent"
    GOOD = "good"
    DEGRADED = "degraded"
    POOR = "poor"


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class ProcessType(Enum):
    """流程类型"""
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"
    PARALLEL = "parallel"


@dataclass
class EthicalJudgment:
    """道德判断"""
    status: EthicalStatus
    alignment_score: float  # 0-1, 与核心价值观的对齐度
    risk_level: str  # low, medium, high
    concerns: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    requires_user_consent: bool = False


@dataclass
class Goal:
    """目标"""
    description: str
    priority: int  # 1-10
    deadline: Optional[str] = None
    success_criteria: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)


@dataclass
class Strategy:
    """战略计划"""
    goals: List[Goal]
    milestones: List[Dict[str, Any]]
    timeline: Dict[str, str]
    resources_required: List[str]
    risks: List[Dict[str, Any]]
    ethical_alignment: float  # 0-1


@dataclass
class CapabilityAssessment:
    """能力评估"""
    can_accomplish: bool
    success_probability: float  # 0-1
    required_skills: List[str]
    available_skills: List[str]
    missing_skills: List[str]
    estimated_time_ms: Optional[int] = None
    potential_obstacles: List[str] = field(default_factory=list)
    confidence_level: float = 0.0


@dataclass
class Task:
    """任务"""
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 5  # 1-10
    required_skills: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    estimated_duration_ms: Optional[int] = None
    assigned_to: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    """执行计划"""
    goal: Goal
    tasks: List[Task]
    timeline: Dict[str, str]
    resource_allocation: 'ResourceAllocation'
    checkpoints: List[Dict[str, Any]]
    fallback_strategies: List[str]


@dataclass
class ResourceAllocation:
    """资源分配"""
    cpu_allocation: Dict[str, float]  # skill_name -> percentage
    memory_budget_mb: Dict[str, int]
    skill_slots: Dict[str, int]  # skill_name -> number of concurrent instances
    time_allocation: Dict[str, int]  # skill_name -> milliseconds


@dataclass
class AttentionAllocation:
    """注意力分配"""
    primary_focus: str  # task_id
    background_tasks: List[str]
    attention_weights: Dict[str, float]  # task_id -> weight (0-1)
    context_switch_cost_ms: int


@dataclass
class HealthStatus(Enum):
    """健康状态"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CIRCUIT_OPEN = "circuit_open"
