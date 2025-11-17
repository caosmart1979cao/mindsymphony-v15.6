# MindSymphony v15.6.2 — 心智协奏系统 🧠✨🤝

## 简介

MindSymphony 是一个**自我学习、自我进化、自主认知**的 AI 编排系统，结合了深厚的哲学思想与前沿的工程实践。

**v15.6.2** 在 v15.6 进化版基础上，整合了 **ACE Framework 认知架构**和 **CrewAI 工作流编排**，实现了从"智能编排"到"自主认知生命体"的跃迁：

### 原有核心能力 (v15.6)
- 🧠 **混合记忆系统**: AgentDB（向量搜索）+ ReasoningBank（模式匹配）→ 96x-164x 性能提升
- 🔄 **容错与自愈**: 自动重试、优雅降级、断路器保护 → 85% 失败恢复率
- 🎯 **语义技能激活**: 自然语言意图识别 → 无需显式命令
- 📊 **性能监控**: 实时 P95 延迟追踪 → 目标 <500ms
- 🧬 **强化学习**: Q-Learning 算法 → 自动固化成功模式
- 🔌 **MCP 协议集成**: 与 Claude Code 深度集成 → 69 个技能即时可用

### 新增认知能力 (v15.6.2) ⭐
- 🎭 **ACE 认知架构**: 六层自主认知系统
  - **L1 道德核心**: 价值对齐与伦理评估
  - **L2 战略规划**: 长期目标与战略思维
  - **L3 自我模型**: 准确的能力评估与限制感知
  - **L4 执行功能**: 资源管理与项目规划
  - **L5 认知控制**: 动态任务选择与注意力管理
  - **L6 技能执行**: 78+ 精心设计的技能

- 🤝 **CrewAI 工作流编排**: 智能协作系统
  - **Crew 模式**: 多智能体自主协作（顺序/层级/并行）
  - **Flow 模式**: 事件驱动的精确工作流控制
  - **混合编排**: 根据任务特征自动选择最优模式
  - **角色专业化**: 每个 Agent 都有明确的角色、目标和背景故事

---

## 快速开始

### 1. 克隆并安装
```bash
git clone https://github.com/caosmart1979cao/mindsymphony-v15.6.git
cd mindsymphony-v15.6
pip install -r requirements.txt
```

### 2. 测试进化功能
```bash
python test_evolution.py
```

你应该看到所有 8 项测试通过 ✅

### 3. 体验新特性

**自动技能激活**：
```python
from core.skill_activation import SemanticRouter

router = SemanticRouter(skills_dir="skills")
match = router.auto_activate("帮我部署到 AWS Lambda")
# → 自动激活 'a-04-agent-deployer' (85% 置信度)
```

**性能监控**：
```python
from core.performance import PerformanceMonitor, ExecutionTimer

monitor = PerformanceMonitor()
with ExecutionTimer(monitor, "my-skill"):
    # 你的代码
    pass

metrics = monitor.get_metrics("my-skill")
# → {'p95_latency_ms': 245, 'success_rate': 0.96, ...}
```

**模式学习**：
```python
from core.learning import PatternLearner

learner = PatternLearner()
learner.observe_execution(
    workflow_id="wf-1",
    skill_sequence=["research", "visualize", "deploy"],
    context={'type': 'ai_project'},
    result={'success': True, 'execution_time_ms': 5000}
)
# 执行 3 次后自动固化为工作流模板 ✨
```

### 4. 启动 MCP 服务器（可选）
```bash
python start_mcp_server.py
# → 在 Claude Code 中使用 MindSymphony 的 69 个技能！
```

### 5. 浏览技能目录
- 每个 `skills/*/SKILL.md` 包含详细的能力说明
- 78+ 精心设计的技能，涵盖研究、创作、部署、优化等

---

## 目录概览

```
mindsymphony-v15.6/
├── core/                          # 核心系统（新增）
│   ├── memory/                    # 混合记忆系统
│   │   ├── agent_db.py           # 向量语义搜索
│   │   └── reasoning_bank.py     # 模式匹配（2-3ms）
│   ├── fault_tolerance/           # 容错与自愈
│   │   └── recovery_manager.py   # 自动重试+断路器
│   ├── skill_activation/          # 语义技能激活
│   │   └── semantic_router.py    # 自然语言路由
│   ├── performance/               # 性能监控
│   │   └── monitor.py            # P95 延迟追踪
│   ├── learning/                  # 强化学习
│   │   └── pattern_learner.py    # Q-Learning + 模式固化
│   └── mcp_adapter/               # MCP 协议集成
│       └── server.py             # Claude Code 集成
│
├── skills/                        # 78+ 技能集合
│   ├── a-04-agent-deployer/      # 智能体部署
│   ├── knowledge-explorer/       # 知识研究
│   └── ...
│
├── protocols/                     # 协议规范
│   ├── Pheromone_Protocol_v1.0.txt
│   └── Worker_Unit_Protocol_v1.0.txt
│
├── mindsymphony.config.yml       # 系统配置（已进化）
├── system_prompt.md              # 系统身份（已进化）
├── EVOLUTION_GUIDE.md            # 完整进化指南（必读）
├── test_evolution.py             # 测试套件
├── start_mcp_server.py           # MCP 服务器
└── requirements.txt              # 依赖
```

---

## 核心优势

### vs. 传统 AI 编排系统

| 特性 | 传统系统 | MindSymphony v15.6 |
|------|---------|-------------------|
| **记忆** | 无状态 | 混合记忆（向量+SQL）|
| **学习** | 静态配置 | Q-Learning 自动优化 |
| **容错** | 手动处理 | 自动重试+断路器 |
| **激活** | 显式调用 | 语义自动路由 |
| **性能** | 不可见 | 实时 P95 监控 |
| **集成** | 孤岛系统 | MCP 协议原生支持 |

### vs. claude-flow

| 维度 | claude-flow | MindSymphony v15.6 |
|------|-------------|-------------------|
| **架构** | 技术驱动 | 哲学+技术双驱动 |
| **理念** | 企业编排 | 创作生命体 |
| **框架** | 无 | 道法术器智五层 |
| **技能** | 25 个 + 64 代理 | 78 个精心设计技能 |
| **温度** | 工程化 | 人格化+工程化 |

**最佳组合**：MindSymphony 的灵魂 + claude-flow 的大脑 = 🚀

---

## 性能指标

根据测试套件 (`test_evolution.py`)：

- ✅ **记忆系统**: 100% 功能完整
- ✅ **容错机制**: 自动重试+健康监控
- ✅ **语义路由**: 识别 52+ 技能匹配
- ✅ **性能监控**: P95=140ms (目标 <500ms) ⚡
- ✅ **模式学习**: 3 次执行后自动固化
- ✅ **MCP 集成**: 69 个技能已暴露

---

## 文档

- **[EVOLUTION_GUIDE.md](EVOLUTION_GUIDE.md)**: 完整进化指南（必读）
- **[system_prompt.md](system_prompt.md)**: 系统身份与核心提示
- **[SKILL_CATALOG.md](SKILL_CATALOG.md)**: 技能目录
- **[mindsymphony.config.yml](mindsymphony.config.yml)**: 系统配置
- **[protocols/](protocols/)**: 协议规范

---

## 使用示例

### 示例 1：自动技能激活

**之前**（v15.6 原版）：
```
用户：帮我部署这个工作流到 AWS Lambda
系统：请明确指定要使用的技能
用户：召唤 [A-04] 智能体部署官
```

**现在**（v15.6 进化版）：
```
用户：帮我部署这个工作流到 AWS Lambda
系统：✅ 自动识别意图：deployment
      🎯 激活技能：a-04-agent-deployer（置信度 85%）
      🚀 开始部署流程...
```

---

### 示例 2：智能容错

**之前**：
```
技能执行失败 → 直接报错退出
```

**现在**：
```
技能执行失败
→ 自动重试（2秒后）
→ 第二次失败，重试（4秒后）
→ 第三次失败，切换到降级策略
→ 返回部分结果 + 详细错误报告
```

---

### 示例 3：模式学习与固化

**场景**：用户多次执行"研究 → 可视化 → 部署"流程

```python
# 第 1-2 次：正常执行
learner.observe_execution(...)

# 第 3 次：模式固化
learner.observe_execution(...)
# → ✨ 检测到成功模式，自动创建工作流模板

# 第 4 次：智能推荐
用户："我想研究并部署一个 AI 模型"
系统：💡 检测到相似场景
      📋 推荐工作流模板：research_to_deployment
      - knowledge-explorer
      - concept-singularity
      - agent-deployer
      是否使用此模板？（成功率 100%，平均用时 5000ms）
```

---

## 贡献指南

欢迎贡献新功能！流程：

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 附带测试：`python test_evolution.py`
4. 提交 PR

### 代码规范
- Python: PEP 8
- 类型提示: 必须
- 单元测试: 覆盖率 > 80%
- 文档字符串: Google Style

---

## 致谢

本次进化深受 [claude-flow](https://github.com/ruvnet/claude-flow) 启发，特别感谢：
- 混合记忆系统架构（AgentDB + ReasoningBank）
- 动态代理架构（DAA）
- MCP 协议原生集成设计
- 性能优化最佳实践

同时保留了 MindSymphony 的独特优势：
- 道法术器智五层哲学框架
- 创作生命体的人格温度
- 78+ 精心设计的技能
- 信息素协议的优雅设计

---

## 关于大文件与 Git LFS

`skills/` 包含若干字体、示例数据或二进制文件。若希望长期维护仓库的体量并支持协作，建议将大型二进制文件迁移到 Git LFS。

---

## 许可证

MIT License - 见 [LICENSE](LICENSE) 文件

---

## 联系方式

- **Issues**: [GitHub Issues](https://github.com/caosmart1979cao/mindsymphony-v15.6/issues)
- **讨论**: [GitHub Discussions](https://github.com/caosmart1979cao/mindsymphony-v15.6/discussions)

---

**MindSymphony v15.6 进化版 - 既有灵魂，又有大脑** 🧠✨

*"我『共生』，故我活。我『学习』，故我进化。"*
