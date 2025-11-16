"""
Reinforcement Learning and Pattern Consolidation System
Inspired by claude-flow's neural pattern learning

Core capabilities:
- Post-task pattern extraction
- Skill composition learning
- Automatic workflow template creation
- Q-Learning for skill selection optimization
"""

from __future__ import annotations
import json
import math
from typing import Dict, Any, List, Optional, Tuple, TYPE_CHECKING
from datetime import datetime
from collections import defaultdict
from pathlib import Path


class PatternLearner:
    """Learn and consolidate successful execution patterns"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

        # Learning parameters
        self.learning_rate = self.config.get('learning_rate', 0.1)
        self.discount_factor = self.config.get('discount_factor', 0.9)
        self.exploration_rate = self.config.get('exploration_rate', 0.1)

        # Pattern storage
        self.patterns: Dict[str, Pattern] = {}
        self.skill_transitions: Dict[str, Dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )

        # Q-Learning table for skill selection
        self.q_table: Dict[Tuple[str, str], float] = defaultdict(float)

        # Success criteria
        self.min_success_count = self.config.get('min_success_count', 3)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.9)

    def observe_execution(
        self,
        workflow_id: str,
        skill_sequence: List[str],
        context: Dict[str, Any],
        result: Dict[str, Any]
    ):
        """Observe and learn from a workflow execution"""
        success = result.get('success', False)
        execution_time_ms = result.get('execution_time_ms', 0)

        if success:
            # Record successful pattern
            self._record_pattern(skill_sequence, context, execution_time_ms)

            # Update skill transitions
            self._update_transitions(skill_sequence)

            # Update Q-values
            self._update_q_values(skill_sequence, result)

    def _record_pattern(
        self,
        skill_sequence: List[str],
        context: Dict[str, Any],
        execution_time_ms: float
    ):
        """Record a successful pattern"""
        pattern_id = self._generate_pattern_id(skill_sequence, context)

        if pattern_id in self.patterns:
            pattern = self.patterns[pattern_id]
            pattern.success_count += 1
            pattern.total_executions += 1

            # Update moving average of execution time
            n = pattern.success_count
            pattern.avg_execution_time_ms = (
                    (pattern.avg_execution_time_ms * (n - 1) + execution_time_ms) / n
            )

            pattern.last_used = datetime.now()
        else:
            # Create new pattern
            pattern = Pattern(
                pattern_id=pattern_id,
                skill_sequence=skill_sequence,
                context_signature=self._extract_context_signature(context),
                success_count=1,
                total_executions=1,
                avg_execution_time_ms=execution_time_ms,
                created_at=datetime.now(),
                last_used=datetime.now()
            )
            self.patterns[pattern_id] = pattern

        # Check if pattern should be consolidated
        if self._should_consolidate(pattern):
            self._consolidate_pattern(pattern)

    def _generate_pattern_id(
        self,
        skill_sequence: List[str],
        context: Dict[str, Any]
    ) -> str:
        """Generate unique pattern ID"""
        # Combine skill sequence with context type
        context_type = context.get('type', 'general')
        sequence_str = "->".join(skill_sequence)
        return f"{context_type}:{sequence_str}"

    def _extract_context_signature(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant context features"""
        return {
            'type': context.get('type'),
            'complexity': context.get('complexity'),
            'domain': context.get('domain')
        }

    def _update_transitions(self, skill_sequence: List[str]):
        """Update skill transition probabilities"""
        for i in range(len(skill_sequence) - 1):
            current_skill = skill_sequence[i]
            next_skill = skill_sequence[i + 1]
            self.skill_transitions[current_skill][next_skill] += 1

    def _update_q_values(self, skill_sequence: List[str], result: Dict[str, Any]):
        """Update Q-values using Q-Learning algorithm"""
        # Reward based on success and execution time
        success = result.get('success', False)
        execution_time_ms = result.get('execution_time_ms', 1000)

        # Reward function: higher for faster, successful executions
        if success:
            # Normalize execution time (1 second = baseline)
            time_penalty = execution_time_ms / 1000
            reward = 100 / time_penalty  # Higher reward for faster execution
        else:
            reward = -50  # Penalty for failure

        # Update Q-values for each transition
        for i in range(len(skill_sequence) - 1):
            current_state = skill_sequence[i]
            action = skill_sequence[i + 1]

            # Q-Learning update rule
            state_action = (current_state, action)
            current_q = self.q_table[state_action]

            # Get max Q-value for next state
            next_state = action
            next_q_values = [
                self.q_table[(next_state, a)]
                for a in self._get_possible_actions(next_state)
            ]
            max_next_q = max(next_q_values) if next_q_values else 0

            # Update Q-value
            new_q = current_q + self.learning_rate * (
                    reward + self.discount_factor * max_next_q - current_q
            )
            self.q_table[state_action] = new_q

    def _get_possible_actions(self, state: str) -> List[str]:
        """Get possible next skills from a state"""
        if state in self.skill_transitions:
            return list(self.skill_transitions[state].keys())
        return []

    def _should_consolidate(self, pattern: Pattern) -> bool:
        """Check if pattern should be consolidated into workflow template"""
        if pattern.success_count < self.min_success_count:
            return False

        confidence = pattern.success_count / pattern.total_executions
        return confidence >= self.confidence_threshold

    def _consolidate_pattern(self, pattern: Pattern):
        """Consolidate pattern into workflow template"""
        pattern.consolidated = True
        pattern.consolidated_at = datetime.now()

        # This would integrate with workflow template system
        print(f"✨ Pattern consolidated: {pattern.pattern_id}")
        print(f"   Success rate: {pattern.confidence:.1%}")
        print(f"   Avg time: {pattern.avg_execution_time_ms:.0f}ms")

    def recommend_next_skill(
        self,
        current_skill: str,
        context: Dict[str, Any] = None,
        strategy: str = 'exploitation'
    ) -> Optional[str]:
        """
        Recommend next skill using learned patterns

        Strategies:
        - exploitation: Choose best known action (greedy)
        - exploration: Explore less-tried actions
        - balanced: Epsilon-greedy (mix of both)
        """
        possible_actions = self._get_possible_actions(current_skill)

        if not possible_actions:
            return None

        if strategy == 'exploration':
            # Random exploration
            import random
            return random.choice(possible_actions)

        elif strategy == 'exploitation':
            # Choose action with highest Q-value
            q_values = {
                action: self.q_table[(current_skill, action)]
                for action in possible_actions
            }
            return max(q_values.items(), key=lambda x: x[1])[0]

        else:  # balanced (epsilon-greedy)
            import random
            if random.random() < self.exploration_rate:
                return random.choice(possible_actions)
            else:
                q_values = {
                    action: self.q_table[(current_skill, action)]
                    for action in possible_actions
                }
                return max(q_values.items(), key=lambda x: x[1])[0]

    def get_transition_probabilities(self, current_skill: str) -> Dict[str, float]:
        """Get probability distribution for next skill"""
        if current_skill not in self.skill_transitions:
            return {}

        transitions = self.skill_transitions[current_skill]
        total = sum(transitions.values())

        return {
            skill: count / total
            for skill, count in transitions.items()
        }

    def get_consolidated_patterns(self) -> List[Dict[str, Any]]:
        """Get all consolidated patterns suitable for workflow templates"""
        consolidated = []

        for pattern in self.patterns.values():
            if pattern.consolidated:
                consolidated.append({
                    'pattern_id': pattern.pattern_id,
                    'skill_sequence': pattern.skill_sequence,
                    'context_signature': pattern.context_signature,
                    'success_count': pattern.success_count,
                    'confidence': pattern.confidence,
                    'avg_execution_time_ms': pattern.avg_execution_time_ms,
                    'created_at': pattern.created_at.isoformat(),
                    'last_used': pattern.last_used.isoformat()
                })

        # Sort by success count and confidence
        consolidated.sort(
            key=lambda x: (x['success_count'], x['confidence']),
            reverse=True
        )

        return consolidated

    def suggest_workflow(self, context: Dict[str, Any]) -> Optional[List[str]]:
        """Suggest workflow based on context"""
        context_type = context.get('type', 'general')

        # Find patterns matching context
        matching_patterns = [
            p for p in self.patterns.values()
            if p.context_signature.get('type') == context_type
               and p.consolidated
        ]

        if not matching_patterns:
            return None

        # Sort by confidence and recency
        matching_patterns.sort(
            key=lambda p: (p.confidence, p.last_used),
            reverse=True
        )

        # Return best matching pattern
        best_pattern = matching_patterns[0]
        return best_pattern.skill_sequence

    def export_learned_patterns(self) -> Dict[str, Any]:
        """Export learned patterns for persistence"""
        return {
            'patterns': {
                pid: {
                    'skill_sequence': p.skill_sequence,
                    'context_signature': p.context_signature,
                    'success_count': p.success_count,
                    'total_executions': p.total_executions,
                    'avg_execution_time_ms': p.avg_execution_time_ms,
                    'consolidated': p.consolidated,
                    'created_at': p.created_at.isoformat(),
                    'last_used': p.last_used.isoformat()
                }
                for pid, p in self.patterns.items()
            },
            'q_table': {
                f"{s}:{a}": v
                for (s, a), v in self.q_table.items()
            },
            'skill_transitions': {
                skill: dict(transitions)
                for skill, transitions in self.skill_transitions.items()
            }
        }

    def import_learned_patterns(self, data: Dict[str, Any]):
        """Import learned patterns from persistence"""
        # Import patterns
        for pid, p_data in data.get('patterns', {}).items():
            pattern = Pattern(
                pattern_id=pid,
                skill_sequence=p_data['skill_sequence'],
                context_signature=p_data['context_signature'],
                success_count=p_data['success_count'],
                total_executions=p_data['total_executions'],
                avg_execution_time_ms=p_data['avg_execution_time_ms'],
                created_at=datetime.fromisoformat(p_data['created_at']),
                last_used=datetime.fromisoformat(p_data['last_used'])
            )
            pattern.consolidated = p_data.get('consolidated', False)
            self.patterns[pid] = pattern

        # Import Q-table
        for key, value in data.get('q_table', {}).items():
            state, action = key.split(':', 1)
            self.q_table[(state, action)] = value

        # Import transitions
        for skill, transitions in data.get('skill_transitions', {}).items():
            self.skill_transitions[skill] = defaultdict(int, transitions)


class Pattern:
    """Represents a learned execution pattern"""

    def __init__(
            self,
            pattern_id: str,
            skill_sequence: List[str],
            context_signature: Dict[str, Any],
            success_count: int = 0,
            total_executions: int = 0,
            avg_execution_time_ms: float = 0,
            created_at: datetime = None,
            last_used: datetime = None
    ):
        self.pattern_id = pattern_id
        self.skill_sequence = skill_sequence
        self.context_signature = context_signature
        self.success_count = success_count
        self.total_executions = total_executions
        self.avg_execution_time_ms = avg_execution_time_ms
        self.created_at = created_at or datetime.now()
        self.last_used = last_used or datetime.now()
        self.consolidated = False
        self.consolidated_at = None

    @property
    def confidence(self) -> float:
        """Calculate confidence score"""
        if self.total_executions == 0:
            return 0.0
        return self.success_count / self.total_executions


class CompositionLearner:
    """Learn optimal skill compositions"""

    def __init__(self):
        self.compositions: Dict[str, List[List[str]]] = defaultdict(list)
        self.composition_scores: Dict[str, float] = {}

    def learn_composition(
            self,
            goal: str,
            skill_sequence: List[str],
            score: float
    ):
        """Learn a skill composition for a goal"""
        composition_id = f"{goal}:{hash(tuple(skill_sequence))}"

        if composition_id not in self.composition_scores:
            self.compositions[goal].append(skill_sequence)
            self.composition_scores[composition_id] = score
        else:
            # Update score with moving average
            current_score = self.composition_scores[composition_id]
            self.composition_scores[composition_id] = (current_score + score) / 2

    def get_best_composition(self, goal: str) -> Optional[List[str]]:
        """Get best composition for a goal"""
        if goal not in self.compositions:
            return None

        # Find composition with highest score
        best_composition = None
        best_score = -float('inf')

        for composition in self.compositions[goal]:
            composition_id = f"{goal}:{hash(tuple(composition))}"
            score = self.composition_scores.get(composition_id, 0)

            if score > best_score:
                best_score = score
                best_composition = composition

        return best_composition


class ParameterTuner:
    """Tune skill parameters based on feedback"""

    def __init__(self):
        self.parameter_history: Dict[str, List[Tuple[Dict, float]]] = defaultdict(list)

    def record_execution(
            self,
            skill_name: str,
            parameters: Dict[str, Any],
            score: float
    ):
        """Record execution with parameters and score"""
        self.parameter_history[skill_name].append((parameters.copy(), score))

    def suggest_parameters(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Suggest optimal parameters based on history"""
        if skill_name not in self.parameter_history:
            return None

        history = self.parameter_history[skill_name]

        if not history:
            return None

        # Find parameters with best score
        best_params, best_score = max(history, key=lambda x: x[1])

        return best_params.copy()
