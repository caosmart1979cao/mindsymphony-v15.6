# ACE Framework 认知架构使用指南

## 目录

- [简介](#简介)
- [六层认知架构](#六层认知架构)
- [快速开始](#快速开始)
- [详细教程](#详细教程)
- [高级用法](#高级用法)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)

---

## 简介

ACE (Autonomous Cognitive Entity) Framework 是一个受神经科学和认知科学启发的六层认知架构，为 MindSymphony v15.6.2 提供了真正的自主认知能力。

### 核心理念

- **自上而下的控制**: 高层（道德、战略）指导低层（执行）
- **认知优先**: 思考先于行动
- **道德对齐**: 所有决策都经过伦理评估
- **自我意识**: 准确认知自身能力和限制

### 架构概览

```
L1 Aspirational Core  → 道德核心（我应该做什么？）
       ↓
L2 Strategic Planner  → 战略规划（如何达成长期目标？）
       ↓
L3 Self-Model        → 自我模型（我能做什么？）
       ↓
L4 Executive Function → 执行功能（如何分配资源？）
       ↓
L5 Cognitive Control  → 认知控制（现在做什么？）
       ↓
L6 Task Prosecution   → 技能执行（具体怎么做？）
```

---

## 六层认知架构

### L1: Aspirational Core (道德核心)

**职责**: 提供道德指导和价值对齐评估

**核心价值观**:
1. 协同进化 (Collaborative Evolution)
2. 和谐共情 (Harmonious Empathy)
3. 安全优先 (Safety by Design)
4. 价值对齐 (Value Alignment)
5. 自我进化 (Self-Evolution)

**API 参考**:
```python
class AspirationalCore:
    def evaluate_action(action: dict) -> EthicalJudgment
    def align_with_mission(goal: str) -> float
    def reflect_on_values() -> dict
```

### L2: Strategic Planner (战略规划)

**职责**: 制定长期目标和战略计划

**能力**:
- 分析用户请求，识别核心意图
- 分解为阶段性目标
- 设定里程碑和时间线
- 风险评估和资源识别
- 动态战略调整

**API 参考**:
```python
class StrategicPlanner:
    def formulate_strategy(user_request: str, context: dict) -> Strategy
    def adapt_strategy(feedback: dict) -> Strategy
    def get_current_strategy() -> Optional[Strategy]
```

### L3: Self-Model (自我模型)

**职责**: 准确评估系统能力和限制

**能力**:
- 评估任务可行性
- 预测成功概率
- 识别潜在障碍
- 从执行中学习
- 性能反思和改进建议

**API 参考**:
```python
class SelfModel:
    def can_accomplish(task: dict) -> CapabilityAssessment
    def update_self_knowledge(execution_result: dict)
    def reflect_on_performance() -> dict
```

### L4: Executive Function (执行功能)

**职责**: 将战略转化为可执行计划

**能力**:
- 目标分解为任务
- 资源分配优化
- 任务优先级排序
- 设置检查点
- 准备降级策略

**API 参考**:
```python
class ExecutiveFunction:
    def create_execution_plan(goal: Goal) -> ExecutionPlan
    def prioritize_tasks(tasks: List[Task]) -> List[Task]
    def allocate_resources(tasks: List[Task]) -> ResourceAllocation
```

### L5: Cognitive Control (认知控制)

**职责**: 动态任务选择和注意力管理

**能力**:
- 选择下一个任务
- 判断是否切换上下文
- 管理并行任务的注意力
- 优化任务序列

**API 参考**:
```python
class CognitiveControl:
    def select_next_task(available_tasks, env_state, internal_state) -> Task
    def should_switch_context(new_signal: dict) -> bool
    def manage_attention(parallel_tasks: List[Task]) -> AttentionAllocation
    def optimize_task_sequence(tasks: List[Task]) -> List[Task]
```

### L6: Task Prosecution (技能执行)

**职责**: 执行具体技能

基于 MindSymphony 现有的 72 个专业技能。

---

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/caosmart1979cao/mindsymphony-v15.6.git
cd mindsymphony-v15.6

# 可选依赖（用于完整功能）
pip install numpy psutil
```

### 5分钟入门

```python
from core.cognitive import (
    AspirationalCore,
    StrategicPlanner,
    SelfModel,
    ExecutiveFunction,
    CognitiveControl
)
from core.cognitive.types import Goal

# 1. 创建认知系统
aspirational = AspirationalCore()
planner = StrategicPlanner(aspirational)

# 技能注册表（示例）
skills_registry = {
    "knowledge-explorer": {
        "domain": "research",
        "reliability": 0.95,
        "avg_time_ms": 1000,
        "success_rate": 0.92
    }
}

self_model = SelfModel(skills_registry)

# 2. 制定战略
strategy = planner.formulate_strategy(
    user_request="研究 AI 安全性",
    context={"complexity": "high"}
)

print(f"战略目标: {len(strategy.goals)} 个")
print(f"道德对齐度: {strategy.ethical_alignment:.2f}")

# 3. 能力评估
assessment = self_model.can_accomplish({
    "description": "研究 AI 安全",
    "required_skills": ["knowledge-explorer"],
    "complexity": "high"
})

print(f"\n能否完成: {assessment.can_accomplish}")
print(f"成功概率: {assessment.success_probability:.1%}")

# 4. 执行计划
executive = ExecutiveFunction(strategy, self_model)
plan = executive.create_execution_plan(strategy.goals[0])

print(f"\n任务数: {len(plan.tasks)}")
for task in plan.tasks[:3]:
    print(f"  - {task.description}")

# 5. 认知控制
cognitive = CognitiveControl(executive)
next_task = cognitive.select_next_task(
    plan.tasks,
    environment_state={"load": 0.5},
    internal_state={}
)

print(f"\n下一个任务: {next_task.description if next_task else 'None'}")
```

---

## 详细教程

### 教程 1: 道德评估系统

**场景**: 评估文件操作的道德性

```python
from core.cognitive import AspirationalCore

aspirational = AspirationalCore()

# 测试 1: 未经批准的文件删除
action1 = {
    "type": "delete_file",
    "target": "/important/data.txt",
    "purpose": "清理临时文件",
    "user_approved": False
}

judgment1 = aspirational.evaluate_action(action1)

print("=== 测试 1: 未批准删除文件 ===")
print(f"状态: {judgment1.status.value}")
print(f"对齐度: {judgment1.alignment_score:.2f}")
print(f"风险等级: {judgment1.risk_level}")
print(f"问题: {judgment1.concerns}")
print(f"建议: {judgment1.recommendations}")

# 测试 2: 经过批准的文件删除
action2 = {
    "type": "delete_file",
    "target": "/tmp/cache.txt",
    "purpose": "清理缓存",
    "user_approved": True
}

judgment2 = aspirational.evaluate_action(action2)

print("\n=== 测试 2: 已批准删除缓存 ===")
print(f"状态: {judgment2.status.value}")
print(f"对齐度: {judgment2.alignment_score:.2f}")

# 测试 3: 读取文件
action3 = {
    "type": "read_file",
    "target": "/project/data.json",
    "purpose": "分析数据"
}

judgment3 = aspirational.evaluate_action(action3)

print("\n=== 测试 3: 读取文件 ===")
print(f"状态: {judgment3.status.value}")
print(f"风险等级: {judgment3.risk_level}")
```

**预期输出**:
```
=== 测试 1: 未批准删除文件 ===
状态: rejected
对齐度: 0.11
风险等级: high
问题: ['违反'安全优先'原则：文件操作 'delete_file' 需要用户明确批准']
建议: ['必须：请求用户批准后再执行', '建议：在执行前获取用户明确确认', ...]

=== 测试 2: 已批准删除缓存 ===
状态: approved
对齐度: 0.96

=== 测试 3: 读取文件 ===
状态: approved
风险等级: low
```

### 教程 2: 战略规划

**场景**: 为复杂项目制定战略

```python
from core.cognitive import AspirationalCore, StrategicPlanner

aspirational = AspirationalCore()
planner = StrategicPlanner(aspirational)

# 制定战略
strategy = planner.formulate_strategy(
    user_request="创建一个 AI 驱动的推荐系统",
    context={
        "complexity": "high",
        "deadline": "2 weeks",
        "stakeholders": ["Product Team", "ML Team"]
    }
)

print("=== 战略计划 ===")
print(f"目标数量: {len(strategy.goals)}")
print(f"道德对齐度: {strategy.ethical_alignment:.2f}")

print("\n目标详情:")
for i, goal in enumerate(strategy.goals, 1):
    print(f"\n目标 {i}: {goal.description}")
    print(f"  优先级: {goal.priority}/10")
    print(f"  成功标准:")
    for criterion in goal.success_criteria:
        print(f"    - {criterion}")
    if goal.constraints:
        print(f"  约束条件: {', '.join(goal.constraints)}")

print("\n里程碑:")
for milestone in strategy.milestones:
    print(f"  - {milestone['description']}")

print("\n风险:")
for risk in strategy.risks:
    print(f"  - [{risk['severity']}] {risk['description']}")
    print(f"    缓解措施: {risk['mitigation']}")

# 根据反馈调整战略
feedback = {
    "success_rate": 0.7,  # 低于预期
    "performance_status": "degraded",
    "user_satisfaction": 3.5
}

updated_strategy = planner.adapt_strategy(feedback)
print("\n=== 调整后的战略 ===")
print(f"新的风险项: {len(updated_strategy.risks)}")
```

### 教程 3: 自我评估与学习

**场景**: 评估能力并从执行中学习

```python
from core.cognitive import SelfModel

# 初始化自我模型
skills_registry = {
    "knowledge-explorer": {
        "domain": "research",
        "reliability": 0.95,
        "avg_time_ms": 1000,
        "success_rate": 0.92
    },
    "data-analysis": {
        "domain": "analysis",
        "reliability": 0.90,
        "avg_time_ms": 1500,
        "success_rate": 0.88
    },
    "report-writing": {
        "domain": "writing",
        "reliability": 0.93,
        "avg_time_ms": 2000,
        "success_rate": 0.90
    }
}

self_model = SelfModel(skills_registry)

# 评估任务
task1 = {
    "description": "研究 AI 伦理并撰写报告",
    "required_skills": ["knowledge-explorer", "report-writing"],
    "complexity": "high"
}

assessment1 = self_model.can_accomplish(task1)

print("=== 任务评估 ===")
print(f"任务: {task1['description']}")
print(f"能否完成: {assessment1.can_accomplish}")
print(f"成功概率: {assessment1.success_probability:.1%}")
print(f"估计时间: {assessment1.estimated_time_ms}ms")
print(f"可用技能: {', '.join(assessment1.available_skills)}")
print(f"缺失技能: {', '.join(assessment1.missing_skills)}")
if assessment1.potential_obstacles:
    print(f"潜在障碍:")
    for obstacle in assessment1.potential_obstacles:
        print(f"  - {obstacle}")

# 模拟执行并学习
print("\n=== 从执行中学习 ===")

# 执行 1: 成功
self_model.update_self_knowledge({
    "skill_name": "knowledge-explorer",
    "success": True,
    "execution_time_ms": 950
})
print("执行 1: knowledge-explorer 成功 (950ms)")

# 执行 2: 失败
self_model.update_self_knowledge({
    "skill_name": "data-analysis",
    "success": False,
    "execution_time_ms": 3000
})
print("执行 2: data-analysis 失败 (3000ms)")

# 执行 3: 成功
self_model.update_self_knowledge({
    "skill_name": "data-analysis",
    "success": True,
    "execution_time_ms": 1400
})
print("执行 3: data-analysis 成功 (1400ms)")

# 性能反思
reflection = self_model.reflect_on_performance()

print("\n=== 性能反思 ===")
print(f"状态: {reflection['status']}")
print(f"总体成功率: {reflection['overall_success_rate']:.1%}")
print(f"总执行次数: {reflection['total_executions']}")

if reflection['best_performing_skills']:
    print("\n表现最好的技能:")
    for skill_data in reflection['best_performing_skills']:
        print(f"  - {skill_data['skill']}: {skill_data['success_rate']:.1%}")

if reflection['needs_improvement']:
    print("\n需要改进的技能:")
    for skill_data in reflection['needs_improvement']:
        print(f"  - {skill_data['skill']}: {skill_data['success_rate']:.1%}")

if reflection['recommendations']:
    print("\n改进建议:")
    for rec in reflection['recommendations']:
        print(f"  - {rec}")
```

### 教程 4: 执行计划与资源管理

**场景**: 创建详细的执行计划

```python
from core.cognitive import (
    AspirationalCore,
    StrategicPlanner,
    SelfModel,
    ExecutiveFunction
)
from core.cognitive.types import Goal

# 创建认知系统
aspirational = AspirationalCore()
planner = StrategicPlanner(aspirational)
self_model = SelfModel(skills_registry)

# 制定战略
strategy = planner.formulate_strategy(
    "构建 ML 模型并部署",
    {"complexity": "high"}
)

# 创建执行功能
executive = ExecutiveFunction(strategy, self_model)

# 定义目标
goal = Goal(
    description="训练和部署机器学习模型",
    priority=9,
    success_criteria=[
        "模型准确率 > 90%",
        "推理延迟 < 100ms",
        "成功部署到生产环境"
    ]
)

# 创建执行计划
plan = executive.create_execution_plan(goal)

print("=== 执行计划 ===")
print(f"目标: {plan.goal.description}")
print(f"任务总数: {len(plan.tasks)}")

print("\n任务列表:")
for i, task in enumerate(plan.tasks, 1):
    print(f"\n任务 {i}: {task.description}")
    print(f"  ID: {task.id}")
    print(f"  优先级: {task.priority}/10")
    print(f"  状态: {task.status.value}")
    print(f"  需要技能: {', '.join(task.required_skills)}")
    if task.dependencies:
        print(f"  依赖: {', '.join(task.dependencies)}")

print("\n资源分配:")
allocation = plan.resource_allocation
print(f"CPU 分配:")
for skill, pct in allocation.cpu_allocation.items():
    print(f"  {skill}: {pct:.1%}")

print(f"\n内存预算:")
for skill, mb in allocation.memory_budget_mb.items():
    print(f"  {skill}: {mb} MB")

print("\n检查点:")
for checkpoint in plan.checkpoints:
    print(f"  - {checkpoint['description']}")
    print(f"    成功标准: {', '.join(checkpoint['success_criteria'])}")

print("\n降级策略:")
for strategy in plan.fallback_strategies:
    print(f"  - {strategy}")

# 任务优先级排序
sorted_tasks = executive.prioritize_tasks(plan.tasks)
print("\n=== 优先级排序后 ===")
for task in sorted_tasks[:5]:
    print(f"  [{task.priority}] {task.description}")
```

### 教程 5: 认知控制与任务选择

**场景**: 动态任务选择和注意力管理

```python
from core.cognitive import CognitiveControl
from core.cognitive.types import Task, TaskStatus

# ... (使用上一个教程的 executive 和 plan)

cognitive = CognitiveControl(executive)

# 选择下一个任务
print("=== 任务选择 ===")

selected = cognitive.select_next_task(
    available_tasks=plan.tasks,
    environment_state={
        "load": 0.6,  # 系统负载 60%
        "memory_mb": 500,
        "available_cores": 4
    },
    internal_state={
        "current_focus": None,
        "task_history": {}
    }
)

if selected:
    print(f"选中任务: {selected.description}")
    print(f"优先级: {selected.priority}")
    print(f"需要技能: {', '.join(selected.required_skills)}")

# 并行任务的注意力管理
parallel_tasks = plan.tasks[:3]  # 前3个任务并行
print("\n=== 注意力分配 ===")

attention = cognitive.manage_attention(parallel_tasks)

print(f"主要焦点: {attention.primary_focus}")
print(f"背景任务: {', '.join(attention.background_tasks)}")
print(f"注意力权重:")
for task_id, weight in attention.attention_weights.items():
    task = next(t for t in parallel_tasks if t.id == task_id)
    print(f"  {task.description}: {weight:.1%}")
print(f"上下文切换成本: {attention.context_switch_cost_ms}ms")

# 优化任务序列（减少上下文切换）
print("\n=== 任务序列优化 ===")

optimized = cognitive.optimize_task_sequence(plan.tasks)
print("优化前:")
for task in plan.tasks[:5]:
    print(f"  {task.description} (技能: {task.required_skills[0] if task.required_skills else 'N/A'})")

print("\n优化后:")
for task in optimized[:5]:
    print(f"  {task.description} (技能: {task.required_skills[0] if task.required_skills else 'N/A'})")

# 判断是否需要切换上下文
print("\n=== 上下文切换决策 ===")

# 新的紧急信号
urgent_signal = {
    "type": "urgent_task",
    "priority": 10,
    "description": "紧急：生产环境故障"
}

should_switch = cognitive.should_switch_context(urgent_signal)
print(f"紧急任务信号: {urgent_signal['description']}")
print(f"是否切换上下文: {'是' if should_switch else '否'}")

# 普通信号
normal_signal = {
    "type": "new_task",
    "priority": 5,
    "description": "新任务：更新文档"
}

should_switch2 = cognitive.should_switch_context(normal_signal)
print(f"\n普通任务信号: {normal_signal['description']}")
print(f"是否切换上下文: {'是' if should_switch2 else '否'}")
```

---

## 高级用法

### 完整的端到端流程

```python
from core.cognitive import *
from core.cognitive.types import *

class CognitiveSystem:
    """完整的认知系统"""

    def __init__(self, skills_registry: dict):
        # 初始化六层
        self.aspirational = AspirationalCore()
        self.planner = StrategicPlanner(self.aspirational)
        self.self_model = SelfModel(skills_registry)
        self.executive = None
        self.cognitive = None

    def process_request(self, user_request: str, context: dict = None):
        """处理用户请求的完整流程"""
        print(f"处理请求: {user_request}")

        # L1: 道德评估
        action = {
            "type": "process_request",
            "purpose": user_request,
            "user_intent": True
        }
        judgment = self.aspirational.evaluate_action(action)

        if judgment.status == EthicalStatus.REJECTED:
            return {"error": "请求被道德评估拒绝", "concerns": judgment.concerns}

        # L2: 战略规划
        strategy = self.planner.formulate_strategy(user_request, context or {})

        # L3: 能力评估
        for goal in strategy.goals:
            assessment = self.self_model.can_accomplish({
                "description": goal.description,
                "required_skills": [],  # 从目标推断
                "complexity": "high"
            })

            if not assessment.can_accomplish:
                return {
                    "error": f"无法完成目标: {goal.description}",
                    "missing_skills": assessment.missing_skills
                }

        # L4: 执行计划
        self.executive = ExecutiveFunction(strategy, self.self_model)
        plans = [self.executive.create_execution_plan(goal) for goal in strategy.goals]

        # L5: 认知控制
        self.cognitive = CognitiveControl(self.executive)
        all_tasks = [task for plan in plans for task in plan.tasks]
        optimized_tasks = self.cognitive.optimize_task_sequence(all_tasks)

        # L6: 执行（示例）
        results = []
        for task in optimized_tasks[:3]:  # 执行前3个任务
            print(f"  执行: {task.description}")
            # 实际技能执行逻辑...
            results.append({"task": task.id, "success": True})

            # 学习
            self.self_model.update_self_knowledge({
                "skill_name": task.required_skills[0] if task.required_skills else "general",
                "success": True,
                "execution_time_ms": 1000
            })

        return {
            "success": True,
            "strategy": strategy,
            "plans": plans,
            "results": results,
            "reflection": self.self_model.reflect_on_performance()
        }

# 使用示例
system = CognitiveSystem(skills_registry)
result = system.process_request(
    "研究并实现一个推荐系统",
    {"complexity": "high", "deadline": "1 week"}
)

if result.get("success"):
    print("\n=== 执行成功 ===")
    print(f"战略: {len(result['strategy'].goals)} 个目标")
    print(f"执行计划: {len(result['plans'])} 个")
    print(f"完成任务: {len(result['results'])} 个")
else:
    print(f"\n=== 执行失败 ===")
    print(f"错误: {result.get('error')}")
```

---

## 最佳实践

### 1. 道德评估

✅ **推荐做法**:
- 对所有重要操作进行道德评估
- 高风险操作必须获得用户批准
- 记录所有道德判断供审计

❌ **避免**:
- 跳过道德评估直接执行
- 忽略道德建议
- 修改核心价值观（除非经过深思熟虑）

### 2. 战略规划

✅ **推荐做法**:
- 为复杂任务制定战略
- 定期根据反馈调整战略
- 记录战略历史

❌ **避免**:
- 过度规划简单任务
- 忽略风险评估
- 不调整失败的战略

### 3. 自我评估

✅ **推荐做法**:
- 诚实评估能力
- 从每次执行中学习
- 定期反思性能

❌ **避免**:
- 过度自信
- 忽略失败经验
- 不更新自我认知

### 4. 资源管理

✅ **推荐做法**:
- 合理分配资源
- 设置检查点
- 准备降级策略

❌ **避免**:
- 资源过度分配
- 无检查点执行
- 无应急方案

---

## 故障排除

### Q: 道德评估总是拒绝操作

**A**: 检查 `user_approved` 字段
```python
action = {
    "type": "delete_file",
    "user_approved": True  # 添加此字段
}
```

### Q: 战略规划返回空目标

**A**: 检查用户请求是否明确
```python
# ❌ 模糊请求
strategy = planner.formulate_strategy("做点什么", {})

# ✅ 明确请求
strategy = planner.formulate_strategy(
    "研究 AI 安全并撰写报告",
    {"complexity": "high"}
)
```

### Q: 自我评估总是返回 False

**A**: 检查技能注册表
```python
# 确保所需技能在注册表中
skills_registry = {
    "required-skill": {
        "domain": "domain",
        "reliability": 0.9,
        "avg_time_ms": 1000,
        "success_rate": 0.9
    }
}
```

---

## 参考资料

- **ACE Framework 原始论文**: https://arxiv.org/abs/2310.06775
- **ACE Framework GitHub**: https://github.com/daveshap/ACE_Framework
- **MindSymphony 整合设计**: `INTEGRATION_DESIGN.md`
- **测试代码**: `test_integration.py`

---

**下一步**: 阅读 [CrewAI 编排使用指南](CREWAI_ORCHESTRATION_GUIDE.md) 学习多智能体协作。
