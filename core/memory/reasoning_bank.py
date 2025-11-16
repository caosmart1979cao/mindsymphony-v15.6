"""
ReasoningBank - SQLite-based Pattern Matching System
Inspired by claude-flow's 2-3ms query latency

Core capabilities:
- Ultra-fast pattern matching (2-3ms)
- Rule-based reasoning and decision making
- Pattern consolidation from successful executions
"""

import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class ReasoningBank:
    """Fast pattern matching and rule-based reasoning system"""

    def __init__(self, db_path: str = ".mindsymphony/reasoning_bank.sqlite"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_schema()
        self._load_cache()

    def _init_schema(self):
        """Initialize database schema optimized for sub-3ms queries"""
        cursor = self.conn.cursor()

        # Reasoning patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reasoning_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                trigger_condition TEXT NOT NULL,
                recommended_action TEXT NOT NULL,
                confidence_score REAL DEFAULT 0.5,
                usage_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_used DATETIME
            )
        """)

        # Skill routing rules
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skill_routing_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intent_pattern TEXT NOT NULL,
                skill_name TEXT NOT NULL,
                priority INTEGER DEFAULT 50,
                conditions TEXT,
                enabled BOOLEAN DEFAULT 1,
                match_count INTEGER DEFAULT 0
            )
        """)

        # Decision trees
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS decision_trees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tree_name TEXT UNIQUE NOT NULL,
                tree_structure TEXT NOT NULL,
                context_type TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Quick lookup cache (in-memory optimization)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quick_cache (
                cache_key TEXT PRIMARY KEY,
                cache_value TEXT NOT NULL,
                ttl INTEGER DEFAULT 3600,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Workflow templates (learned patterns)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflow_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_name TEXT UNIQUE NOT NULL,
                skill_sequence TEXT NOT NULL,
                description TEXT,
                success_rate REAL,
                avg_duration_ms REAL,
                use_count INTEGER DEFAULT 0,
                auto_generated BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create indexes for ultra-fast queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_pattern_type
            ON reasoning_patterns(pattern_type)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_intent_pattern
            ON skill_routing_rules(intent_pattern)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_priority
            ON skill_routing_rules(priority DESC)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_enabled
            ON skill_routing_rules(enabled)
        """)

        self.conn.commit()
        self._populate_default_rules()

    def _populate_default_rules(self):
        """Populate with default reasoning patterns"""
        cursor = self.conn.cursor()

        # Check if already populated
        cursor.execute("SELECT COUNT(*) FROM reasoning_patterns")
        if cursor.fetchone()[0] > 0:
            return

        default_patterns = [
            {
                'pattern_type': 'error_recovery',
                'trigger_condition': 'skill_execution_failed',
                'recommended_action': 'retry_with_backoff',
                'confidence_score': 0.9
            },
            {
                'pattern_type': 'error_recovery',
                'trigger_condition': 'skill_timeout',
                'recommended_action': 'graceful_degrade',
                'confidence_score': 0.85
            },
            {
                'pattern_type': 'optimization',
                'trigger_condition': 'repeated_skill_sequence',
                'recommended_action': 'create_workflow_template',
                'confidence_score': 0.95
            },
            {
                'pattern_type': 'skill_selection',
                'trigger_condition': 'multiple_skills_match',
                'recommended_action': 'select_highest_success_rate',
                'confidence_score': 0.9
            }
        ]

        for pattern in default_patterns:
            cursor.execute("""
                INSERT INTO reasoning_patterns
                (pattern_type, trigger_condition, recommended_action, confidence_score)
                VALUES (?, ?, ?, ?)
            """, (
                pattern['pattern_type'],
                pattern['trigger_condition'],
                pattern['recommended_action'],
                pattern['confidence_score']
            ))

        self.conn.commit()

    def _load_cache(self):
        """Load frequently used patterns into memory cache"""
        self.memory_cache = {}

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT pattern_type, trigger_condition, recommended_action, confidence_score
            FROM reasoning_patterns
            WHERE usage_count > 10
            ORDER BY usage_count DESC
            LIMIT 100
        """)

        for row in cursor.fetchall():
            cache_key = f"{row[0]}:{row[1]}"
            self.memory_cache[cache_key] = {
                'recommended_action': row[2],
                'confidence_score': row[3]
            }

    def match_pattern(
        self,
        pattern_type: str,
        trigger_condition: str
    ) -> Optional[Dict[str, Any]]:
        """
        Ultra-fast pattern matching (target: <3ms)
        Uses memory cache for frequent patterns
        """
        # Check memory cache first (sub-millisecond)
        cache_key = f"{pattern_type}:{trigger_condition}"
        if cache_key in self.memory_cache:
            return self.memory_cache[cache_key]

        # Database lookup (should be <3ms with indexes)
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT recommended_action, confidence_score, id
            FROM reasoning_patterns
            WHERE pattern_type = ? AND trigger_condition = ?
            ORDER BY confidence_score DESC
            LIMIT 1
        """, (pattern_type, trigger_condition))

        row = cursor.fetchone()
        if row:
            # Update usage count
            cursor.execute("""
                UPDATE reasoning_patterns
                SET usage_count = usage_count + 1,
                    last_used = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (row[2],))
            self.conn.commit()

            result = {
                'recommended_action': row[0],
                'confidence_score': row[1]
            }

            # Add to cache if frequently used
            if cache_key not in self.memory_cache:
                self.memory_cache[cache_key] = result

            return result

        return None

    def route_to_skill(
        self,
        user_intent: str,
        context: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Route user intent to appropriate skills
        Returns ranked list of matching skills
        """
        cursor = self.conn.cursor()

        # Find matching rules (simple pattern matching)
        cursor.execute("""
            SELECT skill_name, priority, conditions, id
            FROM skill_routing_rules
            WHERE enabled = 1
            ORDER BY priority DESC
        """)

        matches = []
        for row in cursor.fetchall():
            skill_name, priority, conditions_json, rule_id = row

            # Simple keyword matching (can be enhanced with NLP)
            # This is optimized for speed
            conditions = json.loads(conditions_json) if conditions_json else {}

            if self._check_conditions(user_intent, conditions, context):
                matches.append({
                    'skill_name': skill_name,
                    'priority': priority,
                    'rule_id': rule_id
                })

                # Update match count
                cursor.execute("""
                    UPDATE skill_routing_rules
                    SET match_count = match_count + 1
                    WHERE id = ?
                """, (rule_id,))

        self.conn.commit()
        return matches

    def _check_conditions(
        self,
        user_intent: str,
        conditions: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> bool:
        """Check if conditions match (fast evaluation)"""
        if not conditions:
            return False

        # Keyword matching
        keywords = conditions.get('keywords', [])
        for keyword in keywords:
            if keyword.lower() in user_intent.lower():
                return True

        # Pattern matching
        patterns = conditions.get('patterns', [])
        for pattern in patterns:
            if pattern.lower() in user_intent.lower():
                return True

        return False

    def add_routing_rule(
        self,
        skill_name: str,
        keywords: List[str] = None,
        patterns: List[str] = None,
        priority: int = 50
    ):
        """Add a new skill routing rule"""
        cursor = self.conn.cursor()

        conditions = {}
        if keywords:
            conditions['keywords'] = keywords
        if patterns:
            conditions['patterns'] = patterns

        # Generate intent pattern for indexing
        intent_pattern = '|'.join(keywords or patterns or [skill_name])

        cursor.execute("""
            INSERT OR REPLACE INTO skill_routing_rules
            (intent_pattern, skill_name, priority, conditions)
            VALUES (?, ?, ?, ?)
        """, (
            intent_pattern,
            skill_name,
            priority,
            json.dumps(conditions)
        ))

        self.conn.commit()

    def consolidate_pattern(
        self,
        skill_sequence: List[str],
        success: bool,
        execution_time_ms: float
    ):
        """Consolidate successful patterns into workflow templates"""
        if not success or len(skill_sequence) < 2:
            return

        cursor = self.conn.cursor()

        # Check if this sequence has been seen before
        sequence_json = json.dumps(skill_sequence)
        template_name = "_".join(skill_sequence).lower()

        cursor.execute("""
            SELECT id, use_count, success_rate, avg_duration_ms
            FROM workflow_templates
            WHERE template_name = ?
        """, (template_name,))

        row = cursor.fetchone()

        if row:
            # Update existing template
            template_id, use_count, success_rate, avg_duration = row
            new_use_count = use_count + 1
            new_success_rate = ((success_rate or 0) * use_count + 1.0) / new_use_count
            new_avg_duration = ((avg_duration or 0) * use_count + execution_time_ms) / new_use_count

            cursor.execute("""
                UPDATE workflow_templates
                SET use_count = ?, success_rate = ?, avg_duration_ms = ?
                WHERE id = ?
            """, (new_use_count, new_success_rate, new_avg_duration, template_id))
        else:
            # Create new template
            description = f"Auto-learned workflow: {' → '.join(skill_sequence)}"

            cursor.execute("""
                INSERT INTO workflow_templates
                (template_name, skill_sequence, description, success_rate,
                 avg_duration_ms, use_count, auto_generated)
                VALUES (?, ?, ?, ?, ?, 1, 1)
            """, (
                template_name,
                sequence_json,
                description,
                1.0,
                execution_time_ms
            ))

        self.conn.commit()

    def get_workflow_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a workflow template by name"""
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT skill_sequence, description, success_rate, avg_duration_ms
            FROM workflow_templates
            WHERE template_name = ?
        """, (template_name,))

        row = cursor.fetchone()
        if row:
            return {
                'skill_sequence': json.loads(row[0]),
                'description': row[1],
                'success_rate': row[2],
                'avg_duration_ms': row[3]
            }

        return None

    def get_recommended_templates(
        self,
        min_success_rate: float = 0.8,
        min_use_count: int = 3
    ) -> List[Dict[str, Any]]:
        """Get recommended workflow templates"""
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT template_name, skill_sequence, description,
                   success_rate, avg_duration_ms, use_count
            FROM workflow_templates
            WHERE success_rate >= ? AND use_count >= ?
            ORDER BY success_rate DESC, use_count DESC
            LIMIT 20
        """, (min_success_rate, min_use_count))

        templates = []
        for row in cursor.fetchall():
            templates.append({
                'template_name': row[0],
                'skill_sequence': json.loads(row[1]),
                'description': row[2],
                'success_rate': row[3],
                'avg_duration_ms': row[4],
                'use_count': row[5]
            })

        return templates

    def record_success(self, pattern_type: str, trigger_condition: str):
        """Record successful pattern application"""
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE reasoning_patterns
            SET success_count = success_count + 1
            WHERE pattern_type = ? AND trigger_condition = ?
        """, (pattern_type, trigger_condition))

        self.conn.commit()

    def get_decision(self, tree_name: str, context: Dict[str, Any]) -> Optional[str]:
        """Make decision using decision tree"""
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT tree_structure FROM decision_trees WHERE tree_name = ?
        """, (tree_name,))

        row = cursor.fetchone()
        if row:
            tree = json.loads(row[0])
            return self._traverse_tree(tree, context)

        return None

    def _traverse_tree(self, node: Dict[str, Any], context: Dict[str, Any]) -> Optional[str]:
        """Traverse decision tree to make decision"""
        if 'action' in node:
            return node['action']

        condition = node.get('condition')
        if not condition:
            return None

        # Evaluate condition
        if self._evaluate_condition(condition, context):
            if 'true_branch' in node:
                return self._traverse_tree(node['true_branch'], context)
        else:
            if 'false_branch' in node:
                return self._traverse_tree(node['false_branch'], context)

        return None

    def _evaluate_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate a condition against context"""
        field = condition.get('field')
        operator = condition.get('operator')
        value = condition.get('value')

        context_value = context.get(field)

        if operator == 'equals':
            return context_value == value
        elif operator == 'greater_than':
            return context_value > value
        elif operator == 'less_than':
            return context_value < value
        elif operator == 'contains':
            return value in str(context_value)

        return False

    def close(self):
        """Close database connection"""
        self.conn.close()
