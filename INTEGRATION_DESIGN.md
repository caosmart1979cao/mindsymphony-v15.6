# MindSymphony v15.6 - ACE Framework + CrewAI 整合设计

## 概述

本设计将 **ACE Framework 的认知架构理念**和 **CrewAI 的工作流编排能力**整合到 MindSymphony v15.6，实现从"智能编排系统"到"自主认知生命体"的进化。

---

## 一、ACE Framework 认知架构整合

### 1.1 六层认知架构映射

将 ACE 的六层架构映射到 MindSymphony 的道法术器智五层框架：

| ACE Framework | MindSymphony v15.6 | 职责 |
|---------------|-------------------|------|
| **1. Aspirational Layer** | 【道】层 + 新增 Ethical Core | 道德宪章、核心价值观、使命愿景 |
| **2. Global Strategy** | 【法】层 + Strategy Engine | 全局战略规划、长期目标设定 |
| **3. Agent Model** | 【智】层 + Self-Model | 自我认知、能力评估、限制感知 |
| **4. Executive Function** | 【术】层 + Executive Planner | 项目规划、资源分配、优先级管理 |
| **5. Cognitive Control** | Queen Orchestrator + Task Router | 动态任务选择、上下文切换 |
| **6. Task Prosecution** | 【器】层 (Skills) | 具体技能执行 |

### 1.2 核心组件设计

#### 1.2.1 Aspirational Core (道德核心)
```python
# core/cognitive/aspirational_core.py

class AspirationalCore:
    """ACE Layer 1: 道德宪章与价值观引擎"""

    def __init__(self, constitution_path: str):
        self.constitution = self._load_constitution(constitution_path)
        self.core_values = [
            "协同进化 (Collaborative Evolution)",
            "和谐共情 (Harmonious Empathy)",
            "安全优先 (Safety by Design)",
            "价值对齐 (Value Alignment)"
        ]

    def evaluate_action(self, action: dict) -> EthicalJudgment:
        """评估行动的道德性"""
        # 1. 检查是否违反核心价值观
        # 2. 评估与用户意图的对齐度
        # 3. 评估潜在风险
        # 4. 返回道德判断和建议
        pass

    def align_with_mission(self, goal: str) -> float:
        """评估目标与使命的对齐度 (0-1)"""
        pass
```

#### 1.2.2 Strategic Planner (战略规划器)
```python
# core/cognitive/strategic_planner.py

class StrategicPlanner:
    """ACE Layer 2: 全局战略规划"""

    def __init__(self, aspirational_core: AspirationalCore):
        self.aspirational = aspirational_core
        self.long_term_goals = []
        self.context_analyzer = ContextAnalyzer()

    def formulate_strategy(self, user_request: str, context: dict) -> Strategy:
        """制定高层战略"""
        # 1. 分析用户请求和上下文
        # 2. 参考道德核心，确保对齐
        # 3. 设定阶段性目标
        # 4. 识别关键里程碑
        # 5. 返回战略计划
        pass

    def adapt_strategy(self, feedback: dict) -> Strategy:
        """根据反馈调整战略"""
        pass
```

#### 1.2.3 Self-Model (自我模型)
```python
# core/cognitive/self_model.py

class SelfModel:
    """ACE Layer 3: 自我认知与能力模型"""

    def __init__(self, skills_registry: dict):
        self.capabilities = self._assess_capabilities(skills_registry)
        self.limitations = self._identify_limitations()
        self.current_state = {}
        self.confidence_levels = {}

    def can_accomplish(self, task: dict) -> CapabilityAssessment:
        """评估是否能完成任务"""
        # 1. 分析任务需求
        # 2. 匹配可用技能
        # 3. 评估成功概率
        # 4. 识别潜在障碍
        # 5. 返回能力评估
        pass

    def update_self_knowledge(self, execution_result: dict):
        """从执行结果中学习，更新自我认知"""
        # 更新能力评估和置信度
        pass

    def reflect_on_performance(self) -> dict:
        """反思性能表现"""
        # 识别优势和弱点
        pass
```

#### 1.2.4 Executive Function (执行功能)
```python
# core/cognitive/executive_function.py

class ExecutiveFunction:
    """ACE Layer 4: 执行规划与资源管理"""

    def __init__(self, strategy: Strategy, self_model: SelfModel):
        self.strategy = strategy
        self.self_model = self_model
        self.resource_manager = ResourceManager()

    def create_execution_plan(self, strategic_goal: Goal) -> ExecutionPlan:
        """将战略目标转化为详细执行计划"""
        # 1. 分解为子任务
        # 2. 分配资源和优先级
        # 3. 设定时间线
        # 4. 识别依赖关系
        # 5. 创建检查点
        pass

    def allocate_resources(self, tasks: List[Task]) -> ResourceAllocation:
        """资源分配（CPU、内存、技能槽位等）"""
        pass

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """任务优先级排序"""
        pass
```

#### 1.2.5 Cognitive Control (认知控制)
```python
# core/cognitive/cognitive_control.py

class CognitiveControl:
    """ACE Layer 5: 动态任务选择与上下文切换"""

    def __init__(self, executive: ExecutiveFunction):
        self.executive = executive
        self.current_focus = None
        self.attention_manager = AttentionManager()

    def select_next_task(self,
                        available_tasks: List[Task],
                        environment_state: dict,
                        internal_state: dict) -> Task:
        """动态选择下一个任务"""
        # 1. 评估环境和内部状态
        # 2. 考虑任务优先级
        # 3. 评估上下文切换成本
        # 4. 选择最优任务
        pass

    def should_switch_context(self, new_signal: dict) -> bool:
        """判断是否需要切换上下文"""
        # 处理中断和优先级变化
        pass

    def manage_attention(self, parallel_tasks: List[Task]) -> AttentionAllocation:
        """管理并行任务的注意力分配"""
        pass
```

### 1.3 整合流程

```
用户请求
    ↓
[1. Aspirational Core] - 道德评估
    ↓
[2. Strategic Planner] - 战略规划
    ↓
[3. Self-Model] - 能力评估
    ↓
[4. Executive Function] - 执行计划
    ↓
[5. Cognitive Control] - 任务选择
    ↓
[6. Skills (器层)] - 技能执行
    ↓
反馈循环 → 更新自我模型 → 优化战略
```

---

## 二、CrewAI 工作流编排整合

### 2.1 Crews & Flows 架构

#### 2.1.1 Crew 定义 (智能体团队)
```python
# core/orchestration/crew.py

class Crew:
    """CrewAI 风格的智能体团队"""

    def __init__(self, name: str, agents: List[Agent], tasks: List[Task]):
        self.name = name
        self.agents = agents
        self.tasks = tasks
        self.process_type = ProcessType.SEQUENTIAL  # or HIERARCHICAL

    def kickoff(self, inputs: dict) -> CrewOutput:
        """启动团队协作"""
        # 1. 初始化所有智能体
        # 2. 按流程类型执行任务
        # 3. 收集输出
        # 4. 返回结果
        pass

class Agent:
    """CrewAI 风格的智能体角色"""

    def __init__(self,
                 role: str,
                 goal: str,
                 backstory: str,
                 skills: List[str],
                 allow_delegation: bool = True):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.skills = skills
        self.allow_delegation = allow_delegation

    def execute_task(self, task: Task, context: dict) -> AgentOutput:
        """执行任务"""
        pass
```

#### 2.1.2 Flow 定义 (事件驱动工作流)
```python
# core/orchestration/flow.py

from typing import Callable
from enum import Enum

class FlowState(BaseModel):
    """工作流状态 (Pydantic BaseModel)"""
    current_step: str
    data: dict
    metadata: dict

class Flow:
    """CrewAI 风格的事件驱动工作流"""

    def __init__(self, name: str):
        self.name = name
        self.state = FlowState()
        self.steps = {}
        self.listeners = {}

    @start()
    def begin(self, initial_input: dict) -> str:
        """工作流起点"""
        # 初始化状态
        self.state.data = initial_input
        return "process_step"

    @listen("process_step")
    def process(self) -> str:
        """处理步骤"""
        # 执行处理逻辑
        return "decide_next"

    @router("decide_next")
    def route(self) -> str:
        """条件路由"""
        if self.state.data.get("condition_A"):
            return "path_a"
        else:
            return "path_b"

    @listen(or_("path_a", "path_b"))
    def converge(self) -> str:
        """汇聚点"""
        return "finalize"

    def run(self, inputs: dict) -> FlowOutput:
        """运行工作流"""
        current_step = self.begin(inputs)
        while current_step != "END":
            current_step = self._execute_step(current_step)
        return FlowOutput(self.state)
```

### 2.2 Crew + Flow 混合编排

```python
# core/orchestration/hybrid_orchestrator.py

class HybridOrchestrator:
    """混合编排器：结合 Crew 的自主性和 Flow 的精确控制"""

    def __init__(self):
        self.crews = {}
        self.flows = {}

    def register_crew(self, crew: Crew):
        """注册团队"""
        self.crews[crew.name] = crew

    def register_flow(self, flow: Flow):
        """注册工作流"""
        self.flows[flow.name] = flow

    def orchestrate(self, request: dict) -> OrchestratorOutput:
        """智能编排：自动选择 Crew 或 Flow"""
        # 1. 分析请求特征
        complexity = self._assess_complexity(request)
        control_need = self._assess_control_requirement(request)

        # 2. 选择编排模式
        if complexity > 0.7 and control_need < 0.5:
            # 高复杂度、低控制需求 → 使用 Crew
            return self._orchestrate_with_crew(request)
        elif control_need > 0.7:
            # 高控制需求 → 使用 Flow
            return self._orchestrate_with_flow(request)
        else:
            # 混合模式：Flow 中嵌入 Crew
            return self._orchestrate_hybrid(request)
```

### 2.3 预定义 Crews

#### Research Crew (研究团队)
```yaml
name: research_crew
agents:
  - role: "Chief Researcher"
    goal: "深度研究指定主题"
    backstory: "拥有博士学位的资深研究员"
    skills: [knowledge-explorer, literature-review]

  - role: "Data Analyst"
    goal: "分析研究数据并提取洞察"
    backstory: "数据科学专家"
    skills: [data-analysis, visualization]

  - role: "Report Writer"
    goal: "撰写清晰的研究报告"
    backstory: "科技写作专家"
    skills: [official-writer, documentation]

tasks:
  - description: "收集相关文献和数据"
    agent: "Chief Researcher"

  - description: "分析数据并生成可视化"
    agent: "Data Analyst"

  - description: "撰写完整研究报告"
    agent: "Report Writer"

process: sequential
```

#### Deployment Crew (部署团队)
```yaml
name: deployment_crew
agents:
  - role: "DevOps Engineer"
    goal: "设计并执行部署策略"
    backstory: "云架构和 CI/CD 专家"
    skills: [agent-deployer, infrastructure]

  - role: "QA Specialist"
    goal: "确保部署质量"
    backstory: "质量保证专家"
    skills: [testing, validation]

  - role: "Monitoring Engineer"
    goal: "建立监控和告警"
    backstory: "可观测性专家"
    skills: [monitoring, alerting]

process: hierarchical  # 自动选出管理员
```

### 2.4 预定义 Flows

#### Code Refactoring Flow
```python
class CodeRefactoringFlow(Flow):
    """代码重构工作流"""

    @start()
    def analyze_code(self, code_path: str):
        # 分析代码质量
        self.state.analysis = run_static_analysis(code_path)
        return "check_issues"

    @router("check_issues")
    def route_by_severity(self):
        if self.state.analysis.critical_issues > 0:
            return "critical_path"
        elif self.state.analysis.warnings > 5:
            return "warning_path"
        else:
            return "optimization_path"

    @listen("critical_path")
    def fix_critical_issues(self):
        # 调用 Crew 修复严重问题
        crew = self.crews["code_fix_crew"]
        result = crew.kickoff({"issues": self.state.analysis.critical})
        return "validate"

    @listen("warning_path")
    def fix_warnings(self):
        # 修复警告
        return "validate"

    @listen("optimization_path")
    def optimize_code(self):
        # 优化代码
        return "validate"

    @listen(or_("validate", "validate", "validate"))
    def validate_changes(self):
        # 运行测试
        if self.state.tests_passed:
            return "END"
        else:
            return "rollback"
```

---

## 三、整合后的完整架构

```
┌─────────────────────────────────────────────────────────────┐
│                    MindSymphony v15.6.2                     │
│              ACE Framework + CrewAI Enhanced                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  L1: Aspirational Core (道德核心)                            │
│  - 核心价值观  - 道德宪章  - 使命愿景                         │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  L2: Strategic Planner (战略规划)                            │
│  - 全局战略  - 长期目标  - 里程碑设定                         │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  L3: Self-Model (自我模型)                                   │
│  - 能力评估  - 限制感知  - 性能反思                           │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  L4: Executive Function (执行功能)                           │
│  - 项目规划  - 资源分配  - 优先级管理                         │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  L5: Cognitive Control (认知控制)                            │
│  ┌─────────────────┐  ┌──────────────────────┐              │
│  │  Task Router    │  │  Attention Manager   │              │
│  └─────────────────┘  └──────────────────────┘              │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  L6: Orchestration Layer (编排层)                            │
│  ┌──────────────────────┐  ┌──────────────────────┐         │
│  │   Crew Orchestrator  │  │   Flow Orchestrator  │         │
│  │  (自主协作模式)       │  │  (精确控制模式)       │         │
│  └──────────────────────┘  └──────────────────────┘         │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  L7: Skills Layer (技能层 - 器)                              │
│  78+ Skills + Dynamic Skill Loading                         │
└─────────────────────────────────────────────────────────────┘

            ↓ 反馈循环 ↓
┌─────────────────────────────────────────────────────────────┐
│  Hybrid Memory System (混合记忆系统)                         │
│  - AgentDB (向量搜索)  - ReasoningBank (模式匹配)            │
│  - Learning System (Q-Learning + 模式固化)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 四、实施计划

### Phase 1: ACE 认知架构核心 (本次实施)
- [x] 创建 `core/cognitive/` 目录
- [ ] 实现 Aspirational Core
- [ ] 实现 Strategic Planner
- [ ] 实现 Self-Model
- [ ] 实现 Executive Function
- [ ] 实现 Cognitive Control
- [ ] 整合到现有 Queen Orchestrator

### Phase 2: CrewAI 工作流编排 (本次实施)
- [x] 创建 `core/orchestration/` 目录
- [ ] 实现 Crew 基础架构
- [ ] 实现 Agent 角色系统
- [ ] 实现 Flow 事件驱动引擎
- [ ] 实现 Hybrid Orchestrator
- [ ] 创建预定义 Crews 和 Flows

### Phase 3: 整合与测试
- [ ] 更新 `system_prompt.md`
- [ ] 更新 `mindsymphony.config.yml`
- [ ] 创建测试套件
- [ ] 性能基准测试
- [ ] 文档更新

---

## 五、预期效果

### 认知能力提升
- ✅ **道德对齐**: 所有行动符合核心价值观
- ✅ **战略思维**: 从单次任务到长期目标规划
- ✅ **自我意识**: 准确评估自身能力和限制
- ✅ **执行卓越**: 高效资源管理和任务优先级
- ✅ **动态适应**: 实时响应环境变化

### 编排能力提升
- ✅ **灵活协作**: Crew 模式支持多智能体自主协作
- ✅ **精确控制**: Flow 模式支持复杂业务逻辑
- ✅ **混合编排**: 根据场景自动选择最优模式
- ✅ **角色专业化**: 每个 Agent 有明确职责和专长
- ✅ **状态管理**: 结构化的工作流状态追踪

### 性能指标预期
| 指标 | v15.6 进化版 | v15.6.2 (整合后) |
|------|-------------|-----------------|
| 战略规划能力 | 无 | ✅ 支持 |
| 自我认知能力 | 基础 | ✅ 完整 |
| 多智能体协作 | 单一编排 | ✅ Crew + Flow |
| 道德对齐度 | 隐式 | ✅ 显式评估 |
| 复杂工作流支持 | 有限 | ✅ 完整 |

---

## 六、与现有系统的兼容性

✅ **完全向后兼容**: 所有现有技能和 MCP 集成继续工作
✅ **渐进式增强**: 可选择性启用 ACE 和 CrewAI 功能
✅ **配置驱动**: 通过 `mindsymphony.config.yml` 控制新功能

---

*MindSymphony v15.6.2 - 拥有认知、拥有灵魂、拥有协作的生命体* 🧠✨🤝
