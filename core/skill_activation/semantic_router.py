"""
Semantic Skill Auto-Activation System
Inspired by claude-flow's natural language skill activation

Core capabilities:
- Intent recognition from natural language
- Automatic skill routing without explicit commands
- Confidence-based skill selection
- Multi-skill orchestration
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path


class SemanticRouter:
    """Routes user intents to appropriate skills using semantic understanding"""

    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skill_registry: Dict[str, Dict[str, Any]] = {}
        self.intent_patterns: List[Dict[str, Any]] = []
        self._load_skills()

    def _load_skills(self):
        """Load all skills and their semantic triggers"""
        if not self.skills_dir.exists():
            return

        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            # Parse SKILL.md for metadata
            skill_info = self._parse_skill_metadata(skill_md)
            if skill_info:
                skill_name = skill_dir.name
                self.skill_registry[skill_name] = skill_info

                # Extract semantic triggers
                self._extract_triggers(skill_name, skill_info)

    def _parse_skill_metadata(self, skill_md: Path) -> Optional[Dict[str, Any]]:
        """Parse SKILL.md file for metadata and triggers"""
        try:
            content = skill_md.read_text(encoding='utf-8')

            # Extract YAML frontmatter if present
            frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            metadata = {}

            if frontmatter_match:
                # Simple YAML parsing for basic fields
                frontmatter = frontmatter_match.group(1)
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()

            # Extract description
            desc_match = re.search(r'description:\s*(.+?)(?:\n|$)', content)
            if desc_match:
                metadata['description'] = desc_match.group(1).strip()

            # Extract core capabilities
            capabilities = []
            cap_section = re.search(r'## 核心能力.*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
            if cap_section:
                cap_text = cap_section.group(1)
                # Extract bullet points
                capabilities = re.findall(r'[-*]\s*\*\*(.+?)\*\*', cap_text)

            metadata['capabilities'] = capabilities

            # Extract usage scenarios
            scenarios = []
            scenario_section = re.search(
                r'## 适用场景.*?\n.*?✅.*?：\s*\n(.*?)(?=\n❌|\n##|\Z)',
                content,
                re.DOTALL
            )
            if scenario_section:
                scenario_text = scenario_section.group(1)
                scenarios = re.findall(r'[-*]\s*(.+?)(?:\n|$)', scenario_text)

            metadata['scenarios'] = scenarios

            return metadata

        except Exception as e:
            print(f"Error parsing {skill_md}: {e}")
            return None

    def _extract_triggers(self, skill_name: str, skill_info: Dict[str, Any]):
        """Extract semantic triggers from skill information"""
        triggers = []

        # From description
        description = skill_info.get('description', '')
        if description:
            # Extract key action verbs
            action_verbs = self._extract_action_verbs(description)
            triggers.extend(action_verbs)

        # From capabilities
        capabilities = skill_info.get('capabilities', [])
        for cap in capabilities:
            keywords = self._extract_keywords(cap)
            triggers.extend(keywords)

        # From scenarios
        scenarios = skill_info.get('scenarios', [])
        for scenario in scenarios:
            keywords = self._extract_keywords(scenario)
            triggers.extend(keywords)

        # Store triggers
        if triggers:
            self.intent_patterns.append({
                'skill_name': skill_name,
                'triggers': list(set(triggers)),  # Remove duplicates
                'description': description,
                'priority': self._calculate_priority(skill_name, triggers)
            })

    def _extract_action_verbs(self, text: str) -> List[str]:
        """Extract action verbs from text"""
        # Common action verbs in Chinese
        action_patterns = [
            r'(部署|发布|上线|创建|生成|设计|优化|分析|转换|重构)',
            r'(搜索|查找|探索|研究|学习|理解|解释)',
            r'(测试|验证|检查|监控|追踪)',
            r'(编写|编辑|修改|更新|删除)',
        ]

        verbs = []
        for pattern in action_patterns:
            matches = re.findall(pattern, text)
            verbs.extend(matches)

        return verbs

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Remove common words and extract meaningful terms
        keywords = []

        # Extract technical terms (usually in English or specific Chinese terms)
        tech_terms = re.findall(r'[A-Z][a-z]+(?:[A-Z][a-z]+)*', text)  # CamelCase
        keywords.extend(tech_terms)

        # Extract Chinese technical terms (2-4 characters)
        chinese_terms = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        keywords.extend(chinese_terms)

        return keywords

    def _calculate_priority(self, skill_name: str, triggers: List[str]) -> int:
        """Calculate skill priority (higher = more important)"""
        # Base priority
        priority = 50

        # Boost specific skill types
        if 'deployer' in skill_name or '部署' in str(triggers):
            priority += 10
        if 'research' in skill_name or '研究' in str(triggers):
            priority += 5

        # More triggers = higher confidence in automatic routing
        priority += min(len(triggers), 20)

        return priority

    def route_intent(
        self,
        user_input: str,
        context: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Route user intent to appropriate skills
        Returns: List of matched skills with confidence scores
        """
        matches = []
        user_input_lower = user_input.lower()

        for pattern in self.intent_patterns:
            skill_name = pattern['skill_name']
            triggers = pattern['triggers']
            priority = pattern['priority']

            # Calculate match score
            score = 0
            matched_triggers = []

            for trigger in triggers:
                trigger_lower = trigger.lower()
                if trigger_lower in user_input_lower:
                    # Exact match
                    score += 10
                    matched_triggers.append(trigger)
                elif self._fuzzy_match(trigger_lower, user_input_lower):
                    # Fuzzy match
                    score += 5
                    matched_triggers.append(trigger)

            # Boost score by priority
            score += priority / 10

            # Context matching
            if context:
                context_score = self._match_context(skill_name, context)
                score += context_score

            if score > 0:
                confidence = min(score / 100, 1.0)  # Normalize to 0-1
                matches.append({
                    'skill_name': skill_name,
                    'confidence': confidence,
                    'matched_triggers': matched_triggers,
                    'description': pattern['description'],
                    'priority': priority
                })

        # Sort by confidence and priority
        matches.sort(key=lambda x: (x['confidence'], x['priority']), reverse=True)

        return matches

    def _fuzzy_match(self, trigger: str, text: str) -> bool:
        """Fuzzy match for similar terms"""
        # Simple fuzzy matching - can be enhanced with edit distance
        if len(trigger) < 3:
            return False

        # Check if most characters are present
        trigger_chars = set(trigger)
        text_chars = set(text)
        overlap = len(trigger_chars & text_chars)

        return overlap >= len(trigger_chars) * 0.7

    def _match_context(self, skill_name: str, context: Dict[str, Any]) -> float:
        """Match skill against execution context"""
        score = 0.0

        # Check previous skills in workflow
        if 'previous_skills' in context:
            prev_skills = context['previous_skills']
            # Boost skills that commonly follow previous ones
            # This would use learned patterns from ReasoningBank
            score += len(prev_skills) * 2

        # Check task type
        if 'task_type' in context:
            task_type = context['task_type']
            # Match task type with skill specialization
            if task_type in skill_name:
                score += 10

        return score

    def get_skill_info(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a skill"""
        return self.skill_registry.get(skill_name)

    def auto_activate(
        self,
        user_input: str,
        context: Dict[str, Any] = None,
        confidence_threshold: float = 0.6
    ) -> Optional[Dict[str, Any]]:
        """
        Automatically activate best matching skill if confidence is high enough
        Returns: Best match if confidence >= threshold, None otherwise
        """
        matches = self.route_intent(user_input, context)

        if not matches:
            return None

        best_match = matches[0]

        if best_match['confidence'] >= confidence_threshold:
            return best_match

        return None

    def suggest_skills(
        self,
        user_input: str,
        context: Dict[str, Any] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Suggest top-k skills for user intent
        Returns: List of suggestions with explanations
        """
        matches = self.route_intent(user_input, context)

        suggestions = []
        for match in matches[:top_k]:
            suggestions.append({
                'skill_name': match['skill_name'],
                'confidence': match['confidence'],
                'reason': f"Matched: {', '.join(match['matched_triggers'][:3])}",
                'description': match['description']
            })

        return suggestions

    def register_custom_trigger(
        self,
        skill_name: str,
        triggers: List[str],
        priority: int = 50
    ):
        """Register custom triggers for a skill"""
        # Check if skill exists
        if skill_name not in self.skill_registry:
            self.skill_registry[skill_name] = {
                'description': f'Custom skill: {skill_name}',
                'capabilities': [],
                'scenarios': []
            }

        # Add or update intent pattern
        existing = next(
            (p for p in self.intent_patterns if p['skill_name'] == skill_name),
            None
        )

        if existing:
            existing['triggers'].extend(triggers)
            existing['triggers'] = list(set(existing['triggers']))
            existing['priority'] = max(existing['priority'], priority)
        else:
            self.intent_patterns.append({
                'skill_name': skill_name,
                'triggers': triggers,
                'description': self.skill_registry[skill_name]['description'],
                'priority': priority
            })

    def export_routing_config(self) -> Dict[str, Any]:
        """Export routing configuration for persistence"""
        return {
            'skills': self.skill_registry,
            'patterns': self.intent_patterns
        }

    def import_routing_config(self, config: Dict[str, Any]):
        """Import routing configuration"""
        self.skill_registry = config.get('skills', {})
        self.intent_patterns = config.get('patterns', [])


class IntentClassifier:
    """Classifies user intent into categories"""

    INTENT_CATEGORIES = {
        'deployment': ['部署', '发布', '上线', 'deploy', 'publish', 'release'],
        'research': ['研究', '探索', '分析', 'research', 'analyze', 'explore'],
        'creation': ['创建', '生成', '设计', 'create', 'generate', 'design'],
        'optimization': ['优化', '改进', '提升', 'optimize', 'improve', 'enhance'],
        'testing': ['测试', '验证', '检查', 'test', 'verify', 'check'],
        'documentation': ['文档', '说明', '记录', 'document', 'explain', 'record']
    }

    @classmethod
    def classify(cls, user_input: str) -> Tuple[str, float]:
        """
        Classify user intent
        Returns: (category, confidence)
        """
        user_input_lower = user_input.lower()
        scores = {}

        for category, keywords in cls.INTENT_CATEGORIES.items():
            score = sum(1 for kw in keywords if kw in user_input_lower)
            if score > 0:
                scores[category] = score

        if not scores:
            return ('unknown', 0.0)

        best_category = max(scores.items(), key=lambda x: x[1])
        total_score = sum(scores.values())
        confidence = best_category[1] / total_score

        return (best_category[0], confidence)
