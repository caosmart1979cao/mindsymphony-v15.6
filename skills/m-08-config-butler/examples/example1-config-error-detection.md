# 示例 1：配置错误检测与修复引导

## 场景描述

用户在修改配置文件时犯了几个常见错误：
1. 将布尔值写成了字符串
2. 引用了不存在的灵魂ID
3. 缺少必需的字段
4. 使用了已废弃的配置项

配置管家需要检测所有错误并提供清晰的修复指导。

## 错误的配置文件

```yaml
# mindsymphony.config.yml (含错误)
version: "15.3"

system:
  name: "我的心智协奏系统"
  security_level: "standard"  # ❌ 错误1: 字符串应该是枚举值（不加引号）

souls:
  m-03:
    enabled: "true"  # ❌ 错误2: 布尔值不应该用引号
    priority: high

  b-06:
    enabled: true
    security_level: paranoid

  c-99:  # ❌ 错误3: 引用了不存在的灵魂
    enabled: true

workflows:
  custom-research:
    # ❌ 错误4: 缺少必需的 description 字段
    steps:
      - soul: c-06
        action: research
      - soul: c-99  # ❌ 错误5: 再次引用不存在的灵魂
        action: analyze

  legacy-workflow:
    description: "旧版工作流"
    use_v14_api: true  # ❌ 错误6: 使用了已废弃的配置项
    steps:
      - soul: a-03
        action: strategize
```

## 配置管家的验证输出

```markdown
╔════════════════════════════════════════════════════════════╗
║  心智协奏系统™ v15.3 - 配置验证失败                        ║
╚════════════════════════════════════════════════════════════╝

❌ 检测到 6 个配置错误，系统启动已中止

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【错误 #1】字段类型不匹配

  位置: 第 5 行, system.security_level
  当前值: "standard" (string)
  期望类型: enum (paranoid | standard | trusted)

  问题说明:
  枚举类型的值不应该用引号括起来

  当前配置:
  ```yaml
  system:
    security_level: "standard"  ❌
  ```

  正确配置:
  ```yaml
  system:
    security_level: standard  ✓
  ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【错误 #2】字段类型不匹配

  位置: 第 9 行, souls.m-03.enabled
  当前值: "true" (string)
  期望类型: boolean

  问题说明:
  布尔值应该是 true 或 false，不要用引号

  当前配置:
  ```yaml
  souls:
    m-03:
      enabled: "true"  ❌
  ```

  正确配置:
  ```yaml
  souls:
    m-03:
      enabled: true  ✓
  ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【错误 #3】引用的灵魂不存在

  位置: 第 17 行, souls.c-99
  问题: 灵魂ID "c-99" 在系统中不存在

  可用的认知类灵魂:
  - c-01: 逻辑解构专家
  - c-02: 批判性思维引擎
  - c-03: 元认知观察者
  - c-04: 思辨智核系统
  - c-05: IMO解题熔炉
  - c-06: 知识勘探家
  - c-07: 跨域类比引擎
  - c-08: 因果推理专家

  修复建议:
  1. 检查拼写是否正确
  2. 从上述可用列表中选择正确的灵魂ID
  3. 或者删除此配置项

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【错误 #4】必需字段缺失

  位置: 第 20 行, workflows.custom-research
  缺失字段: description
  字段类型: string

  问题说明:
  每个工作流都必须有 description 字段来说明其用途

  当前配置:
  ```yaml
  workflows:
    custom-research:
      steps:  ❌ 缺少 description
        - soul: c-06
  ```

  正确配置:
  ```yaml
  workflows:
    custom-research:
      description: "自定义研究工作流"  ✓
      steps:
        - soul: c-06
  ```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【错误 #5】工作流引用的灵魂不存在

  位置: 第 25 行, workflows.custom-research.steps[1]
  问题: 工作流步骤引用了不存在的灵魂 "c-99"

  影响:
  此工作流在执行到第2步时会失败

  修复建议:
  将 "c-99" 替换为有效的灵魂ID（参见错误 #3）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【错误 #6】使用了已废弃的配置项

  位置: 第 30 行, workflows.legacy-workflow.use_v14_api
  问题: 配置项 "use_v14_api" 在 v15.0 中已废弃

  废弃原因:
  v15.x 已完全移除 v14 兼容层

  修复建议:
  删除此配置项，工作流将自动使用 v15 API

  迁移指南:
  查看 ./docs/migration/v14-to-v15.md 了解详细迁移步骤

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【修复清单】

请按以下步骤修复配置：

1. 打开配置文件:
   > vim mindsymphony.config.yml

2. 修复错误（按优先级排序）:
   □ 错误 #1: 第 5 行，去掉 "standard" 的引号
   □ 错误 #2: 第 9 行，去掉 "true" 的引号
   □ 错误 #3: 第 17 行，删除或修正 c-99 的配置
   □ 错误 #4: 第 20 行，添加 description 字段
   □ 错误 #5: 第 25 行，修正工作流中的 c-99 引用
   □ 错误 #6: 第 30 行，删除 use_v14_api 配置项

3. 保存后验证配置:
   > mindsymphony config validate

4. 确认无误后启动系统:
   > mindsymphony start

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【需要帮助？】

📖 查看配置文档: ./docs/configuration-guide.md
📋 查看配置示例: ./docs/config-examples/
🔍 运行交互式配置向导: mindsymphony config wizard
💬 获取在线帮助: mindsymphony help config

╔════════════════════════════════════════════════════════════╗
║  System startup aborted. Please fix errors and try again.  ║
╚════════════════════════════════════════════════════════════╝
```

## 修复后的正确配置

```yaml
# mindsymphony.config.yml (已修复)
version: "15.3"

system:
  name: "我的心智协奏系统"
  security_level: standard  # ✓ 修复1: 去掉引号

souls:
  m-03:
    enabled: true  # ✓ 修复2: 去掉引号
    priority: high

  b-06:
    enabled: true
    security_level: paranoid

  # ✓ 修复3: 删除了不存在的 c-99 配置

workflows:
  custom-research:
    description: "自定义研究工作流"  # ✓ 修复4: 添加描述
    steps:
      - soul: c-06
        action: research
      - soul: c-04  # ✓ 修复5: 改为存在的灵魂
        action: analyze

  legacy-workflow:
    description: "旧版工作流（已迁移到v15）"
    # ✓ 修复6: 删除了废弃的配置项
    steps:
      - soul: a-03
        action: strategize
```

## 修复后的验证输出

```markdown
╔════════════════════════════════════════════════════════════╗
║  心智协奏系统™ v15.3 - 配置验证报告                        ║
╚════════════════════════════════════════════════════════════╝

✓ 配置文件位置: ./mindsymphony.config.yml
✓ 文件大小: 1.8 KB
✓ 最后修改: 2025-10-21 14:45:32

【验证结果】
✓ 语法验证通过
✓ 结构验证通过
✓ 字段验证通过 (18/18)
✓ 逻辑验证通过
✓ 完整性验证通过
✓ 所有错误已修复！

【配置摘要】
- 已激活灵魂: 2 个 (m-03, b-06)
- 定义工作流: 2 个
- 安全级别: standard
- 配置版本: 15.3

【优化建议】
ℹ️ 您只启用了 2 个灵魂，如需使用完整功能，
   可以启用更多灵魂或使用预设编组。

💡 建议启用审计日志以便追踪系统行为：
   ```yaml
   audit_log:
     enabled: true
     path: ~/.mindsymphony/audit.log
   ```

╔════════════════════════════════════════════════════════════╗
║  System Config OK. Hive is active.                         ║
╚════════════════════════════════════════════════════════════╝

系统启动就绪。移交控制权给 [M-03] 认知建筑师...
```

## 关键学习点

1. **类型准确性**：YAML中的布尔值、枚举值不要用引号
2. **引用完整性**：确保引用的资源（灵魂、工作流等）都存在
3. **必需字段**：检查所有必需字段是否都已定义
4. **版本兼容**：注意废弃的配置项，及时迁移到新版本
5. **渐进修复**：配置管家会列出所有错误，可以一次性修复
6. **验证优先**：修改后先验证，再启动系统

## 使用建议

- 在大规模修改配置前，先备份原配置文件
- 使用 `mindsymphony config validate` 进行修改后的验证
- 启用详细模式获得更多学习指导
- 参考官方配置示例，避免常见错误
