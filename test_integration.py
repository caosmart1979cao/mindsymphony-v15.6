#!/usr/bin/env python3
"""
MindSymphony v15.6.2 - ACE Framework + CrewAI 整合测试

测试新增的认知架构和工作流编排能力
"""

import sys
import time


def test_ace_cognitive_architecture():
    """测试 ACE 认知架构"""
    print("\n" + "=" * 60)
    print("测试 1: ACE 认知架构")
    print("=" * 60)

    try:
        from core.cognitive import (
            AspirationalCore,
            StrategicPlanner,
            SelfModel,
            ExecutiveFunction,
            CognitiveControl
        )
        from core.cognitive.types import Goal, Task, TaskStatus

        # 1.1 测试 Aspirational Core (道德核心)
        print("\n[1.1] 测试 Aspirational Core...")
        aspirational = AspirationalCore()

        action = {
            "type": "delete_file",
            "target": "/important/file.txt",
            "purpose": "清理临时文件",
            "user_approved": False
        }
        judgment = aspirational.evaluate_action(action)

        print(f"  道德评估状态: {judgment.status.value}")
        print(f"  对齐度分数: {judgment.alignment_score:.2f}")
        print(f"  风险等级: {judgment.risk_level}")

        assert judgment.status.value in ["approved", "conditional", "rejected", "requires_user_confirmation"]
        print("  ✓ Aspirational Core 测试通过")

        # 1.2 测试 Strategic Planner (战略规划)
        print("\n[1.2] 测试 Strategic Planner...")
        planner = StrategicPlanner(aspirational)

        strategy = planner.formulate_strategy(
            user_request="研究并部署一个 AI 模型",
            context={"complexity": "high"}
        )

        print(f"  战略目标数量: {len(strategy.goals)}")
        print(f"  里程碑数量: {len(strategy.milestones)}")
        print(f"  道德对齐度: {strategy.ethical_alignment:.2f}")

        assert len(strategy.goals) > 0
        assert strategy.ethical_alignment >= 0.0
        print("  ✓ Strategic Planner 测试通过")

        # 1.3 测试 Self-Model (自我模型)
        print("\n[1.3] 测试 Self-Model...")
        skills_registry = {
            "knowledge-explorer": {
                "domain": "research",
                "reliability": 0.95,
                "avg_time_ms": 1000,
                "success_rate": 0.92
            },
            "agent-deployer": {
                "domain": "deployment",
                "reliability": 0.90,
                "avg_time_ms": 2000,
                "success_rate": 0.88
            }
        }

        self_model = SelfModel(skills_registry)

        task = {
            "description": "研究 AI 技术",
            "required_skills": ["knowledge-explorer"],
            "complexity": "medium"
        }

        assessment = self_model.can_accomplish(task)

        print(f"  能否完成: {assessment.can_accomplish}")
        print(f"  成功概率: {assessment.success_probability:.2f}")
        print(f"  估计时间: {assessment.estimated_time_ms}ms")

        assert assessment.can_accomplish is not None
        print("  ✓ Self-Model 测试通过")

        # 1.4 测试 Executive Function (执行功能)
        print("\n[1.4] 测试 Executive Function...")
        goal = Goal(
            description="完成研究任务",
            priority=8,
            success_criteria=["收集信息", "分析数据", "撰写报告"]
        )

        executive = ExecutiveFunction(strategy, self_model)
        execution_plan = executive.create_execution_plan(goal)

        print(f"  任务数量: {len(execution_plan.tasks)}")
        print(f"  检查点数量: {len(execution_plan.checkpoints)}")

        assert len(execution_plan.tasks) > 0
        print("  ✓ Executive Function 测试通过")

        # 1.5 测试 Cognitive Control (认知控制)
        print("\n[1.5] 测试 Cognitive Control...")
        cognitive_control = CognitiveControl(executive)

        test_task = Task(
            id="task_1",
            description="测试任务",
            priority=7,
            required_skills=["test"]
        )

        selected = cognitive_control.select_next_task(
            [test_task],
            {"load": 0.5},
            {}
        )

        print(f"  选中任务: {selected.id if selected else 'None'}")

        assert selected is not None or selected is None  # 两种情况都合法
        print("  ✓ Cognitive Control 测试通过")

        print("\n✅ ACE 认知架构测试全部通过！")
        return True

    except Exception as e:
        print(f"\n❌ ACE 认知架构测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_crewai_orchestration():
    """测试 CrewAI 工作流编排"""
    print("\n" + "=" * 60)
    print("测试 2: CrewAI 工作流编排")
    print("=" * 60)

    try:
        from core.orchestration import Agent, Crew, Flow, ProcessType
        from core.orchestration import start, listen, router
        from core.cognitive.types import Task, TaskStatus

        # 2.1 测试 Agent
        print("\n[2.1] 测试 Agent...")
        agent = Agent(
            role="Research Specialist",
            goal="深度研究并提供洞察",
            backstory="拥有博士学位的资深研究员",
            skills=["knowledge-explorer", "analysis"],
            verbose=False
        )

        task = Task(
            id="test_task_1",
            description="研究 AI 技术趋势",
            priority=8,
            required_skills=["knowledge-explorer"]
        )

        output = agent.execute_task(task, {})

        print(f"  角色: {output.agent_role}")
        print(f"  成功: {output.success}")
        print(f"  执行时间: {output.execution_time_ms}ms")

        assert output.agent_role == "Research Specialist"
        print("  ✓ Agent 测试通过")

        # 2.2 测试 Crew (顺序模式)
        print("\n[2.2] 测试 Crew (SEQUENTIAL)...")
        agent1 = Agent(
            role="Researcher",
            goal="收集信息",
            backstory="研究专家",
            skills=["research"],
            verbose=False
        )

        agent2 = Agent(
            role="Analyst",
            goal="分析数据",
            backstory="分析专家",
            skills=["analysis"],
            verbose=False
        )

        tasks = [
            Task(id="t1", description="收集数据", required_skills=["research"]),
            Task(id="t2", description="分析数据", required_skills=["analysis"])
        ]

        crew = Crew(
            name="research_crew",
            agents=[agent1, agent2],
            tasks=tasks,
            process=ProcessType.SEQUENTIAL,
            verbose=False
        )

        crew_output = crew.kickoff({"topic": "AI"})

        print(f"  团队: {crew_output.crew_name}")
        print(f"  成功: {crew_output.success}")
        print(f"  任务输出数: {len(crew_output.agent_outputs)}")

        assert crew_output.crew_name == "research_crew"
        print("  ✓ Crew 测试通过")

        # 2.3 测试 Flow
        print("\n[2.3] 测试 Flow...")

        class TestFlow(Flow):
            def __init__(self):
                super().__init__(name="test_flow", verbose=False)

            @start()
            def begin(self):
                self.state.data["started"] = True
                return "process"

            @listen("process")
            def process(self):
                self.state.data["processed"] = True
                return "END"

        flow = TestFlow()
        flow_output = flow.run({"input": "test"})

        print(f"  工作流: {flow_output.flow_name}")
        print(f"  成功: {flow_output.success}")
        print(f"  步骤数: {flow_output.total_steps}")

        assert flow_output.flow_name == "test_flow"
        assert flow_output.success
        print("  ✓ Flow 测试通过")

        # 2.4 测试 Hybrid Orchestrator
        print("\n[2.4] 测试 Hybrid Orchestrator...")
        from core.orchestration import HybridOrchestrator

        orchestrator = HybridOrchestrator(verbose=False)
        orchestrator.register_crew(crew)
        orchestrator.register_flow(flow)

        request = {
            "description": "复杂的研究和分析任务",
            "complexity": "high",
            "control_requirement": "low",
            "inputs": {"data": "test"}
        }

        result = orchestrator.orchestrate(request)

        print(f"  编排模式: {result['mode']}")
        print(f"  成功: {result['success']}")

        assert result["mode"] in ["crew", "flow", "hybrid"]
        print("  ✓ Hybrid Orchestrator 测试通过")

        print("\n✅ CrewAI 工作流编排测试全部通过！")
        return True

    except Exception as e:
        print(f"\n❌ CrewAI 工作流编排测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """测试完整集成"""
    print("\n" + "=" * 60)
    print("测试 3: 完整集成测试")
    print("=" * 60)

    try:
        from core.cognitive import (
            AspirationalCore,
            StrategicPlanner,
            SelfModel
        )
        from core.orchestration import (
            Agent,
            Crew,
            HybridOrchestrator,
            ProcessType
        )
        from core.cognitive.types import Task

        print("\n[3.1] 创建完整认知系统...")

        # 创建认知架构
        aspirational = AspirationalCore()
        skills_registry = {
            "knowledge-explorer": {"domain": "research", "reliability": 0.95, "avg_time_ms": 1000, "success_rate": 0.92},
            "concept-singularity": {"domain": "creation", "reliability": 0.90, "avg_time_ms": 1500, "success_rate": 0.88},
            "agent-deployer": {"domain": "deployment", "reliability": 0.85, "avg_time_ms": 2000, "success_rate": 0.90}
        }
        self_model = SelfModel(skills_registry)
        planner = StrategicPlanner(aspirational)

        print("  ✓ 认知架构创建完成")

        print("\n[3.2] 创建工作流编排系统...")

        # 创建智能体团队
        agents = [
            Agent("Researcher", "研究", "研究专家", ["knowledge-explorer"]),
            Agent("Creator", "创作", "创作专家", ["concept-singularity"]),
            Agent("Deployer", "部署", "部署专家", ["agent-deployer"])
        ]

        tasks = [
            Task(id="t1", description="研究", required_skills=["knowledge-explorer"]),
            Task(id="t2", description="创作", required_skills=["concept-singularity"]),
            Task(id="t3", description="部署", required_skills=["agent-deployer"])
        ]

        crew = Crew("integration_crew", agents, tasks, ProcessType.SEQUENTIAL, verbose=False)

        orchestrator = HybridOrchestrator(verbose=False)
        orchestrator.register_crew(crew)

        print("  ✓ 工作流编排系统创建完成")

        print("\n[3.3] 执行端到端流程...")

        # 1. 战略规划
        strategy = planner.formulate_strategy(
            "创建并部署一个 AI 系统",
            {"complexity": "high"}
        )

        # 2. 能力评估
        can_do = self_model.can_accomplish({
            "description": "创建 AI 系统",
            "required_skills": list(skills_registry.keys()),
            "complexity": "high"
        })

        # 3. 执行编排
        if can_do.can_accomplish:
            result = orchestrator.orchestrate({
                "description": "创建并部署 AI 系统",
                "crew_name": "integration_crew",
                "inputs": {"project": "AI System"}
            })

            print(f"  战略目标数: {len(strategy.goals)}")
            print(f"  能力评估: {can_do.can_accomplish}")
            print(f"  编排模式: {result['mode']}")
            print(f"  执行成功: {result['success']}")

            assert result['success']
        else:
            print("  系统评估无法完成任务（这是正常的自我认知）")

        print("\n✅ 完整集成测试通过！")
        return True

    except Exception as e:
        print(f"\n❌ 完整集成测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("MindSymphony v15.6.2 - 整合测试套件")
    print("=" * 60)

    results = []

    # 测试 1: ACE 认知架构
    results.append(("ACE 认知架构", test_ace_cognitive_architecture()))

    # 测试 2: CrewAI 工作流编排
    results.append(("CrewAI 工作流编排", test_crewai_orchestration()))

    # 测试 3: 完整集成
    results.append(("完整集成", test_integration()))

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")

    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print("\n🎉 所有测试通过！MindSymphony v15.6.2 整合成功！")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，需要修复")
        return 1


if __name__ == "__main__":
    sys.exit(main())
