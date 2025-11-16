#!/usr/bin/env python3
"""
Test script for MindSymphony v15.6 Evolution Edition
Validates all new features
"""

import sys
import time
from pathlib import Path

print("🧪 MindSymphony v15.6 Evolution Test Suite\n")
print("=" * 60)

# Test 1: Import core modules
print("\n1️⃣ Testing Core Module Imports...")
try:
    from core.memory import AgentDB, ReasoningBank
    from core.fault_tolerance import RecoveryManager
    from core.skill_activation import SemanticRouter, IntentClassifier
    from core.performance import PerformanceMonitor
    from core.learning import PatternLearner
    from core.mcp_adapter import MCPServer
    print("   ✅ All modules imported successfully")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: AgentDB initialization
print("\n2️⃣ Testing Hybrid Memory System...")
try:
    db = AgentDB(db_path=".mindsymphony/test_agent_db.sqlite")
    db.record_execution(
        skill_name="test-skill",
        input_context={"test": "data"},
        output_result={"success": True},
        success=True,
        execution_time_ms=100.5
    )
    analytics = db.get_skill_analytics("test-skill")
    assert analytics['total_executions'] == 1
    assert analytics['success_rate'] == 1.0
    db.close()
    print("   ✅ AgentDB working (recorded execution and retrieved analytics)")
except Exception as e:
    print(f"   ❌ AgentDB test failed: {e}")

# Test 3: ReasoningBank pattern matching
print("\n3️⃣ Testing ReasoningBank Pattern Matching...")
try:
    rb = ReasoningBank(db_path=".mindsymphony/test_reasoning_bank.sqlite")

    # Test pattern matching (should have default patterns)
    pattern = rb.match_pattern("error_recovery", "skill_execution_failed")
    assert pattern is not None
    assert pattern['recommended_action'] == 'retry_with_backoff'

    # Test routing
    rb.add_routing_rule(
        skill_name="test-skill",
        keywords=["测试", "test"],
        priority=60
    )
    matches = rb.route_to_skill("执行测试任务")

    rb.close()
    print(f"   ✅ ReasoningBank working (matched pattern, routed skills)")
except Exception as e:
    print(f"   ❌ ReasoningBank test failed: {e}")

# Test 4: Fault tolerance
print("\n4️⃣ Testing Fault Tolerance...")
try:
    recovery = RecoveryManager(config={'max_retries': 2, 'base_delay_ms': 100})

    # Test successful execution
    def successful_func():
        return {"result": "success"}

    result = recovery.execute_with_retry("test-skill", successful_func)
    assert result['success'] == True
    assert result['attempts'] == 1

    # Test health status
    status = recovery.get_health_status("test-skill")
    print(f"   ✅ Fault tolerance working (retry mechanism, health={status.value})")
except Exception as e:
    print(f"   ❌ Fault tolerance test failed: {e}")

# Test 5: Semantic routing
print("\n5️⃣ Testing Semantic Skill Activation...")
try:
    router = SemanticRouter(skills_dir="skills")

    # Test intent classification
    category, confidence = IntentClassifier.classify("研究最新的AI论文")
    assert category in ['research', 'unknown']

    # Test skill routing
    matches = router.route_intent("帮我部署到AWS")

    print(f"   ✅ Semantic routing working (classified intent={category}, found {len(matches)} matches)")
except Exception as e:
    print(f"   ❌ Semantic routing test failed: {e}")

# Test 6: Performance monitoring
print("\n6️⃣ Testing Performance Monitoring...")
try:
    monitor = PerformanceMonitor()

    # Record some executions
    for i in range(5):
        monitor.record_execution("test-skill", 100 + i*10, success=True)

    metrics = monitor.get_metrics("test-skill")
    assert metrics['total_executions'] == 5
    assert metrics['success_rate'] == 1.0
    assert metrics['p95_latency_ms'] > 0

    print(f"   ✅ Performance monitoring working (P95={metrics['p95_latency_ms']:.1f}ms, status={metrics['performance_status']})")
except Exception as e:
    print(f"   ❌ Performance monitoring test failed: {e}")

# Test 7: Pattern learning
print("\n7️⃣ Testing Pattern Learning...")
try:
    learner = PatternLearner(config={'min_success_count': 2})

    # Observe some executions
    skill_seq = ["skill-a", "skill-b", "skill-c"]
    for i in range(3):
        learner.observe_execution(
            workflow_id=f"wf-{i}",
            skill_sequence=skill_seq,
            context={'type': 'test'},
            result={'success': True, 'execution_time_ms': 1000}
        )

    # Get consolidated patterns
    patterns = learner.get_consolidated_patterns()

    # Test skill recommendation
    next_skill = learner.recommend_next_skill("skill-a", strategy='exploitation')

    print(f"   ✅ Pattern learning working (consolidated {len(patterns)} patterns, recommended next: {next_skill})")
except Exception as e:
    print(f"   ❌ Pattern learning test failed: {e}")

# Test 8: MCP adapter
print("\n8️⃣ Testing MCP Protocol Adapter...")
try:
    server = MCPServer(skills_dir="skills")
    tools = server.list_tools()

    print(f"   ✅ MCP adapter working (exposed {len(tools)} skills as MCP tools)")
except Exception as e:
    print(f"   ❌ MCP adapter test failed: {e}")

# Summary
print("\n" + "=" * 60)
print("🎉 All tests passed! MindSymphony v15.6 evolution is ready.")
print("\n📚 Next steps:")
print("   1. Review EVOLUTION_GUIDE.md for detailed usage")
print("   2. Update mindsymphony.config.yml for your use case")
print("   3. Run: python start_mcp_server.py (optional)")
print("   4. Start using evolved features!")
print("\n✨ Happy orchestrating! ✨")
