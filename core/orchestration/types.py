"""
Type definitions for orchestration system
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from enum import Enum


class ProcessType(Enum):
    """流程类型"""
    SEQUENTIAL = "sequential"  # 顺序执行
    HIERARCHICAL = "hierarchical"  # 层级管理（自动分配管理员）
    PARALLEL = "parallel"  # 并行执行


@dataclass
class AgentOutput:
    """智能体输出"""
    agent_role: str
    task_description: str
    result: Any
    success: bool
    execution_time_ms: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CrewOutput:
    """团队输出"""
    crew_name: str
    agent_outputs: List[AgentOutput]
    final_result: Any
    total_execution_time_ms: int
    success: bool
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FlowState:
    """工作流状态"""
    current_step: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_path: List[str] = field(default_factory=list)


@dataclass
class FlowOutput:
    """工作流输出"""
    flow_name: str
    final_state: FlowState
    execution_path: List[str]
    total_steps: int
    success: bool
    execution_time_ms: int
    metadata: Dict[str, Any] = field(default_factory=dict)
