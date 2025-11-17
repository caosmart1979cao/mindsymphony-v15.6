# CrewAI 工作流编排使用指南

## 目录

- [简介](#简介)
- [核心概念](#核心概念)
- [快速开始](#快速开始)
- [Agent 角色系统](#agent-角色系统)
- [Crew 团队协作](#crew-团队协作)
- [Flow 事件驱动](#flow-事件驱动)
- [Hybrid Orchestrator](#hybrid-orchestrator)
- [预定义示例](#预定义示例)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)

---

## 简介

CrewAI 编排系统为 MindSymphony v15.6.2 提供了灵活的多智能体协作能力，支持：

- **Crew 模式**: 自主协作（3种流程：顺序/层级/并行）
- **Flow 模式**: 精确控制（事件驱动、条件路由）
- **Hybrid 模式**: 智能选择（自动分析任务特征）

### 核心优势

| 特性 | Crew 模式 | Flow 模式 |
|------|----------|----------|
| **适用场景** | 复杂协作 | 精确流程 |
| **控制方式** | 自主 | 显式 |
| **灵活性** | 高 | 中 |
| **可预测性** | 中 | 高 |
| **学习曲线** | 低 | 中 |

### 架构概览

```
┌─────────────────────────────────────────┐
│      Hybrid Orchestrator               │
│      (智能选择编排模式)                  │
└──────────┬────────────────┬─────────────┘
           │                │
    ┌──────┴──────┐  ┌─────┴──────┐
    │   Crew      │  │   Flow     │
    │  (自主协作)  │  │  (精确控制) │
    └──────┬──────┘  └─────┬──────┘
           │                │
      ┌────┴────┐      ┌───┴────┐
      │ Agents  │      │ Steps  │
      └────┬────┘      └───┬────┘
           │                │
      ┌────┴─────────────── ┴────┐
      │   72个 MindSymphony 技能  │
      └───────────────────────────┘
```

---

## 核心概念

### Agent (智能体)

专业化的执行单元，具有：
- **Role**: 角色（如 "Research Specialist"）
- **Goal**: 目标
- **Backstory**: 背景故事（提供上下文）
- **Skills**: 可用技能列表
- **Delegation**: 是否允许委派任务

### Crew (团队)

多个 Agent 的协作组织，支持：
- **Sequential**: 顺序执行任务
- **Hierarchical**: 自动选出管理员协调
- **Parallel**: 并行执行任务

### Flow (工作流)

事件驱动的执行流程，使用装饰器定义：
- `@start()`: 起点
- `@listen(event)`: 监听事件
- `@router(event)`: 条件路由

### Hybrid Orchestrator (混合编排器)

智能分析任务特征，自动选择最优模式。

---

## 快速开始

### 安装

```bash
cd mindsymphony-v15.6

# 核心功能无需额外依赖
python test_integration.py  # 验证安装
```

### 5分钟入门

```python
from core.orchestration import Agent, Crew, ProcessType
from core.cognitive.types import Task

# 1. 创建智能体
researcher = Agent(
    role="Research Specialist",
    goal="深度研究并提供洞察",
    backstory="拥有博士学位的资深研究员",
    skills=["knowledge-explorer"],
    verbose=True
)

analyst = Agent(
    role="Data Analyst",
    goal="分析数据并提取模式",
    backstory="数据科学专家",
    skills=["data-analysis"],
    verbose=True
)

# 2. 定义任务
tasks = [
    Task(
        id="research_task",
        description="研究 Transformer 架构",
        required_skills=["knowledge-explorer"]
    ),
    Task(
        id="analysis_task",
        description="分析研究数据",
        required_skills=["data-analysis"]
    )
]

# 3. 创建团队
crew = Crew(
    name="research_team",
    agents=[researcher, analyst],
    tasks=tasks,
    process=ProcessType.SEQUENTIAL,
    verbose=True
)

# 4. 启动协作
result = crew.kickoff({"topic": "AI Architecture"})

print(f"成功: {result.success}")
print(f"耗时: {result.total_execution_time_ms}ms")
print(f"完成任务: {len(result.agent_outputs)} 个")
```

---

## Agent 角色系统

### 创建 Agent

```python
from core.orchestration import Agent

agent = Agent(
    role="Technical Writer",
    goal="撰写清晰、准确的技术文档",
    backstory="拥有10年经验的技术文档专家，擅长将复杂概念简化",
    skills=["official-writer", "documentation"],
    allow_delegation=True,  # 允许委派
    verbose=False  # 不输出详细日志
)
```

### 执行任务

```python
from core.cognitive.types import Task

task = Task(
    id="write_doc",
    description="撰写 API 文档",
    required_skills=["official-writer"],
    priority=8,
    context={"api_spec": {...}}
)

output = agent.execute_task(
    task=task,
    context={"deadline": "tomorrow"},
    skill_executor=None  # 可选：自定义技能执行器
)

print(f"角色: {output.agent_role}")
print(f"成功: {output.success}")
print(f"结果: {output.result}")
print(f"耗时: {output.execution_time_ms}ms")
```

### Agent 性能统计

```python
stats = agent.get_performance_stats()

print(f"总任务数: {stats['total_tasks']}")
print(f"成功率: {stats['success_rate']:.1%}")
print(f"委派率: {stats['delegation_rate']:.1%}")
```

### Agent 上下文消息

```python
# 获取 Agent 的上下文（用于提示工程）
context_msg = agent.get_context_message()
print(context_msg)
# 输出:
# 角色: Technical Writer
# 目标: 撰写清晰、准确的技术文档
# 背景: 拥有10年经验的技术文档专家...
# 技能: official-writer, documentation
```

---

## Crew 团队协作

### 创建 Crew

```python
from core.orchestration import Crew, ProcessType, Agent
from core.cognitive.types import Task

# 定义智能体
agents = [
    Agent("Researcher", "收集信息", "研究专家", ["knowledge-explorer"]),
    Agent("Analyst", "分析数据", "分析师", ["data-analysis"]),
    Agent("Writer", "撰写报告", "技术写作", ["official-writer"])
]

# 定义任务
tasks = [
    Task(id="t1", description="收集文献", required_skills=["knowledge-explorer"]),
    Task(id="t2", description="分析数据", required_skills=["data-analysis"]),
    Task(id="t3", description="撰写报告", required_skills=["official-writer"])
]

# 创建团队
crew = Crew(
    name="research_crew",
    agents=agents,
    tasks=tasks,
    process=ProcessType.SEQUENTIAL,  # 顺序执行
    verbose=True
)
```

### 三种流程模式

#### 1. Sequential (顺序模式)

任务按顺序执行，每个任务完成后进入下一个：

```python
crew = Crew(
    name="sequential_crew",
    agents=agents,
    tasks=tasks,
    process=ProcessType.SEQUENTIAL
)

result = crew.kickoff({"project": "AI Research"})
# 执行顺序: t1 → t2 → t3
```

#### 2. Hierarchical (层级模式)

自动选出管理员，进行任务分配和协调：

```python
crew = Crew(
    name="hierarchical_crew",
    agents=agents,
    tasks=tasks,
    process=ProcessType.HIERARCHICAL  # 自动选管理员
)

result = crew.kickoff({"project": "Complex System"})
# 管理员（技能最多的 Agent）分配任务
# 执行顺序: 由管理员决定（基于优先级）
```

#### 3. Parallel (并行模式)

任务并行执行（简化实现，实际为顺序模拟）：

```python
crew = Crew(
    name="parallel_crew",
    agents=agents,
    tasks=tasks,
    process=ProcessType.PARALLEL
)

result = crew.kickoff({"project": "Multi-Task"})
# 所有任务"同时"执行
```

### Crew 统计

```python
stats = crew.get_crew_stats()

print(f"总执行次数: {stats['total_executions']}")
print(f"成功率: {stats['success_rate']:.1%}")
print(f"平均耗时: {stats['avg_execution_time_ms']}ms")

# 查看每个 Agent 的统计
for role, agent_stats in stats['agent_stats'].items():
    print(f"{role}:")
    print(f"  任务数: {agent_stats['total_tasks']}")
    print(f"  成功率: {agent_stats['success_rate']:.1%}")
```

---

## Flow 事件驱动

### 创建 Flow

```python
from core.orchestration import Flow, start, listen, router, or_

class MyFlow(Flow):
    """自定义工作流"""

    def __init__(self):
        super().__init__(name="my_flow", verbose=True)

    @start()
    def begin(self) -> str:
        """起点：初始化"""
        self.state.data["started"] = True
        print("Flow 开始...")
        return "process_data"  # 返回下一步的名称

    @listen("process_data")
    def process(self) -> str:
        """处理数据"""
        print("处理数据中...")
        self.state.data["processed"] = True
        return "check_condition"

    @router("check_condition")
    def decide(self) -> str:
        """条件路由"""
        if self.state.data.get("use_path_a", True):
            return "path_a"
        else:
            return "path_b"

    @listen("path_a")
    def handle_a(self) -> str:
        """路径 A"""
        print("执行路径 A")
        self.state.data["path"] = "A"
        return "finalize"

    @listen("path_b")
    def handle_b(self) -> str:
        """路径 B"""
        print("执行路径 B")
        self.state.data["path"] = "B"
        return "finalize"

    @listen(or_("finalize", "finalize"))
    def finish(self) -> str:
        """汇聚点"""
        print("Flow 完成!")
        return "END"  # 返回 "END" 或 None 结束

# 运行 Flow
flow = MyFlow()
output = flow.run({"use_path_a": True})

print(f"\n成功: {output.success}")
print(f"总步骤: {output.total_steps}")
print(f"执行路径: {' → '.join(output.execution_path)}")
print(f"最终状态: {output.final_state.data}")
```

### Flow 中调用 Crew

```python
class HybridFlow(Flow):
    """在 Flow 中嵌入 Crew"""

    def __init__(self, crew: Crew):
        super().__init__(name="hybrid_flow")
        self.register_crew("research_crew", crew)

    @start()
    def begin(self):
        return "run_crew"

    @listen("run_crew")
    def execute_crew(self):
        # 调用 Crew
        crew_result = self.call_crew(
            "research_crew",
            {"topic": self.state.data.get("topic")}
        )

        if crew_result.success:
            self.state.data["crew_output"] = crew_result.final_result
            return "analyze_result"
        else:
            return "error_handler"

    @listen("analyze_result")
    def analyze(self):
        # 分析 Crew 的输出
        output = self.state.data["crew_output"]
        # ... 分析逻辑 ...
        return "END"

# 使用
crew = Crew(...)  # 之前定义的 Crew
flow = HybridFlow(crew)
result = flow.run({"topic": "AI Safety"})
```

### Flow 装饰器详解

#### `@start()`

标记工作流的起点，必须有且仅有一个：

```python
@start()
def begin(self):
    # 初始化逻辑
    return "next_step"
```

#### `@listen(event)`

监听单个或多个事件：

```python
# 单个事件
@listen("process")
def handle_process(self):
    return "next"

# 多个事件（OR 逻辑）
@listen(or_("event_a", "event_b"))
def handle_either(self):
    return "next"
```

#### `@router(event)`

条件路由，根据状态选择下一步：

```python
@router("decide")
def make_decision(self):
    if self.state.data.get("condition"):
        return "path_a"
    elif self.state.data.get("other_condition"):
        return "path_b"
    else:
        return "default_path"
```

### Flow 状态管理

```python
class StatefulFlow(Flow):
    @start()
    def begin(self):
        # 设置状态
        self.state.data["counter"] = 0
        self.state.data["results"] = []
        self.state.metadata["start_time"] = time.time()

        return "process"

    @listen("process")
    def process(self):
        # 读取和更新状态
        counter = self.state.data["counter"]
        self.state.data["counter"] = counter + 1
        self.state.data["results"].append(f"Step {counter}")

        if counter < 5:
            return "process"  # 循环
        else:
            return "END"
```

---

## Hybrid Orchestrator

### 创建 Orchestrator

```python
from core.orchestration import HybridOrchestrator

orchestrator = HybridOrchestrator(verbose=True)

# 注册 Crew 和 Flow
orchestrator.register_crew(research_crew)
orchestrator.register_flow(my_flow)
```

### 智能编排

Orchestrator 根据任务特征自动选择模式：

```python
# 高复杂度 + 低控制需求 → Crew
result1 = orchestrator.orchestrate({
    "description": "复杂的多领域研究项目，需要多个专家协作",
    "complexity": "high",       # 高复杂度
    "control_requirement": "low",  # 低控制需求
    "inputs": {"topic": "Quantum Computing"}
})
# → 选择: Crew 模式

# 高控制需求 → Flow
result2 = orchestrator.orchestrate({
    "description": "严格的部署流程，需要精确控制每个步骤",
    "complexity": "medium",
    "control_requirement": "high",  # 高控制需求
    "inputs": {"app": "production"}
})
# → 选择: Flow 模式

# 平衡场景 → Hybrid
result3 = orchestrator.orchestrate({
    "description": "需要团队协作但有一定流程约束的项目",
    "complexity": "high",
    "control_requirement": "medium",
    "inputs": {"project": "ML Pipeline"}
})
# → 选择: Hybrid 模式（Flow 中嵌入 Crew）

print(f"模式选择: {result1['mode']}")  # "crew" / "flow" / "hybrid"
print(f"成功: {result1['success']}")
```

### 决策逻辑

Orchestrator 的决策矩阵：

| 复杂度 | 控制需求 | 选择模式 |
|--------|---------|---------|
| 高 (>0.7) | 低 (<0.5) | **Crew** |
| 任意 | 高 (>0.7) | **Flow** |
| 其他 | 其他 | **Hybrid** |

### 编排统计

```python
stats = orchestrator.get_orchestration_stats()

print(f"总请求数: {stats['total_requests']}")
print(f"模式分布:")
for mode, ratio in stats['mode_distribution'].items():
    print(f"  {mode}: {ratio:.1%}")

print(f"平均复杂度: {stats['avg_complexity']:.2f}")
print(f"平均控制需求: {stats['avg_control_need']:.2f}")
```

---

## 预定义示例

### 示例 1: Research Crew (研究团队)

```python
from core.orchestration import Crew, Agent, ProcessType
from core.cognitive.types import Task

# 定义研究团队
research_crew = Crew(
    name="research_team",
    agents=[
        Agent(
            role="Chief Researcher",
            goal="领导研究并确保质量",
            backstory="拥有博士学位的资深研究员，发表过50+论文",
            skills=["knowledge-explorer", "research-strategist"],
            allow_delegation=True
        ),
        Agent(
            role="Literature Reviewer",
            goal="全面回顾相关文献",
            backstory="专注文献综述的研究助理",
            skills=["knowledge-explorer"],
            allow_delegation=False
        ),
        Agent(
            role="Data Analyst",
            goal="分析研究数据",
            backstory="数据科学专家，擅长统计分析",
            skills=["data-analysis", "performance-tuner"],
            allow_delegation=False
        ),
        Agent(
            role="Technical Writer",
            goal="撰写高质量研究报告",
            backstory="科技写作专家",
            skills=["official-writer", "manuscript-proofreader"],
            allow_delegation=False
        )
    ],
    tasks=[
        Task(
            id="literature_review",
            description="回顾相关文献并总结现状",
            priority=9,
            required_skills=["knowledge-explorer"]
        ),
        Task(
            id="data_collection",
            description="收集实验数据",
            priority=8,
            required_skills=["knowledge-explorer"]
        ),
        Task(
            id="data_analysis",
            description="分析数据并提取洞察",
            priority=9,
            required_skills=["data-analysis"]
        ),
        Task(
            id="report_writing",
            description="撰写研究报告",
            priority=10,
            required_skills=["official-writer"]
        )
    ],
    process=ProcessType.HIERARCHICAL,  # Chief Researcher 自动成为管理员
    verbose=True
)

# 使用
result = research_crew.kickoff({
    "topic": "Large Language Models Safety",
    "deadline": "2 weeks",
    "depth": "comprehensive"
})
```

### 示例 2: Deployment Flow (部署工作流)

```python
from core.orchestration import Flow, start, listen, router

class DeploymentFlow(Flow):
    """生产部署工作流"""

    def __init__(self):
        super().__init__(name="deployment_flow", verbose=True)

    @start()
    def verify_tests(self):
        """验证所有测试通过"""
        tests_passed = self.state.data.get("tests_passed", False)

        if not tests_passed:
            return "run_tests"
        else:
            return "build"

    @listen("run_tests")
    def execute_tests(self):
        """运行测试"""
        # 实际测试逻辑...
        self.state.data["tests_passed"] = True
        return "build"

    @listen("build")
    def build_artifact(self):
        """构建部署包"""
        print("构建部署包...")
        self.state.data["artifact_ready"] = True
        return "deploy_staging"

    @listen("deploy_staging")
    def deploy_to_staging(self):
        """部署到预发布环境"""
        print("部署到 staging...")
        self.state.data["staging_deployed"] = True
        return "validate_staging"

    @listen("validate_staging")
    def validate(self):
        """验证预发布部署"""
        # 验证逻辑...
        validation_ok = True
        self.state.data["validation_passed"] = validation_ok

        if validation_ok:
            return "approve_production"
        else:
            return "rollback_staging"

    @router("approve_production")
    def check_approval(self):
        """检查是否获得生产部署批准"""
        approved = self.state.data.get("production_approved", False)

        if approved:
            return "deploy_production"
        else:
            return "wait_approval"

    @listen("wait_approval")
    def wait_for_approval(self):
        """等待批准"""
        # 在实际系统中，这里会等待外部输入
        self.state.metadata["waiting_approval"] = True
        return "END"  # 暂停，等待外部触发

    @listen("deploy_production")
    def deploy_to_production(self):
        """部署到生产环境"""
        print("部署到 production...")
        self.state.data["production_deployed"] = True
        return "monitor"

    @listen("monitor")
    def monitor_deployment(self):
        """监控部署"""
        print("建立监控...")
        self.state.data["monitoring_active"] = True
        return "END"

    @listen("rollback_staging")
    def rollback(self):
        """回滚"""
        print("回滚 staging 部署...")
        self.state.data["rolled_back"] = True
        return "END"

# 使用
deployment_flow = DeploymentFlow()
result = deployment_flow.run({
    "tests_passed": True,
    "production_approved": True
})

print(f"部署成功: {result.success}")
print(f"执行路径: {' → '.join(result.execution_path)}")
```

### 示例 3: Code Review Crew

```python
code_review_crew = Crew(
    name="code_review_team",
    agents=[
        Agent(
            "Senior Developer",
            "Review code quality and architecture",
            "10+ years software engineering experience",
            ["codebase-ecologist", "structure-analyst"]
        ),
        Agent(
            "Security Expert",
            "Check for security vulnerabilities",
            "Cybersecurity specialist",
            ["security-auditor"]
        ),
        Agent(
            "Performance Analyst",
            "Analyze performance implications",
            "Performance optimization expert",
            ["performance-tuner"]
        )
    ],
    tasks=[
        Task(id="code_quality", description="Review code quality", required_skills=["codebase-ecologist"]),
        Task(id="security_check", description="Security audit", required_skills=["security-auditor"]),
        Task(id="performance_check", description="Performance analysis", required_skills=["performance-tuner"])
    ],
    process=ProcessType.PARALLEL,  # 并行审查
    verbose=True
)

result = code_review_crew.kickoff({
    "pr_number": "123",
    "repository": "myapp"
})
```

---

## 最佳实践

### 1. Agent 设计

✅ **推荐做法**:
- 给每个 Agent 明确的角色定位
- 提供详细的背景故事（提高上下文理解）
- 合理分配技能（避免一个 Agent 包揽所有）
- 适当设置 `allow_delegation`

❌ **避免**:
- 角色模糊不清
- 背景故事过于简单
- 技能分配不均（超级 Agent 或无能 Agent）

**示例**:
```python
# ✅ 好的 Agent 定义
agent = Agent(
    role="Machine Learning Engineer",
    goal="设计和训练高质量的 ML 模型",
    backstory="拥有 ML 硕士学位，5年工业界经验，专注于 NLP 和计算机视觉",
    skills=["model-training", "data-preprocessing", "hyperparameter-tuning"],
    allow_delegation=False
)

# ❌ 不好的 Agent 定义
agent = Agent(
    role="Developer",
    goal="做事情",
    backstory="程序员",
    skills=["everything"],
    allow_delegation=True
)
```

### 2. Crew 组织

✅ **推荐做法**:
- 3-5 个 Agent 为最佳团队规模
- 层级模式适合复杂项目
- 顺序模式适合有依赖的任务
- 设置合理的任务优先级

❌ **避免**:
- 团队规模过大（>10 个 Agent）
- 流程类型选择不当
- 任务依赖关系混乱

### 3. Flow 设计

✅ **推荐做法**:
- 清晰的步骤命名
- 合理的条件路由
- 状态管理规范
- 错误处理机制

❌ **避免**:
- 步骤名称模糊
- 过度复杂的路由逻辑
- 状态污染
- 无错误处理

**示例**:
```python
class GoodFlow(Flow):
    @start()
    def initialize(self):
        # 初始化所有必要状态
        self.state.data["errors"] = []
        return "process"

    @listen("process")
    def process_data(self):
        try:
            # 处理逻辑
            return "success"
        except Exception as e:
            self.state.data["errors"].append(str(e))
            return "error_handler"

    @listen("error_handler")
    def handle_error(self):
        # 错误处理
        return "END"
```

### 4. Hybrid Orchestrator 使用

✅ **推荐做法**:
- 注册多个 Crew 和 Flow
- 提供清晰的任务描述
- 适当设置复杂度和控制需求提示

❌ **避免**:
- 只注册一种编排类型
- 任务描述过于模糊
- 强制指定不合适的模式

---

## 故障排除

### Q: Agent 总是无法执行任务

**A**: 检查技能匹配
```python
# 确保 Agent 的技能包含任务所需技能
agent.skills = ["knowledge-explorer"]  # Agent 的技能
task.required_skills = ["knowledge-explorer"]  # 任务需要的技能
```

### Q: Crew 执行失败

**A**: 检查任务分配
```python
# 确保每个任务都有对应的 Agent 能处理
for task in tasks:
    matching_agents = [a for a in agents if a.can_handle_task(task)]
    if not matching_agents:
        print(f"警告: 任务 {task.description} 没有合适的 Agent")
```

### Q: Flow 无法结束

**A**: 检查返回值
```python
# 确保最终步骤返回 "END" 或 None
@listen("final_step")
def finish(self):
    return "END"  # 或 return None
```

### Q: Hybrid Orchestrator 总是选择同一模式

**A**: 检查注册和描述
```python
# 确保注册了多种编排类型
orchestrator.register_crew(crew1)
orchestrator.register_flow(flow1)

# 提供明确的任务特征
request = {
    "description": "具体描述任务性质...",
    "complexity": "high",  # 或明确指定
    "control_requirement": "low"
}
```

---

## 参考资料

- **CrewAI GitHub**: https://github.com/crewAIInc/crewAI
- **MindSymphony 整合设计**: `INTEGRATION_DESIGN.md`
- **ACE 认知架构指南**: `ACE_COGNITIVE_GUIDE.md`
- **测试代码**: `test_integration.py`

---

**下一步**: 结合 [ACE 认知架构](ACE_COGNITIVE_GUIDE.md) 构建完整的自主认知系统。
