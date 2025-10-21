# [B-06] 终端代理 - 安全代码重构示例

## 场景描述

用户需要对一个TypeScript项目进行安全的代码重构，包括重命名文件、修改代码、运行测试验证。整个过程需要终端代理配合其他灵魂完成。

## 用户请求

```
我需要将src/utils/helper.ts重命名为src/utils/string-helper.ts，
并更新所有引用它的文件。请确保安全执行并验证测试通过。
```

## 执行过程

### 步骤 1：协同[B-07]代码库生态学家分析影响范围

**[B-06] 终端代理授权请求 #001**：

```markdown
## 授权请求 #001

**操作类型**: 读取
**风险等级**: 低风险
**目标**: 扫描项目查找helper.ts的所有引用

### 操作详情
使用ripgrep扫描所有TypeScript文件中对helper.ts的import语句

### AI安全评估
- **风险分类**: SAFE
- **潜在影响**: 无，仅读取操作
- **警告信息**: 无

### 请求
[低风险] 请批准执行。
```

**用户**: 批准

**执行结果**：
```
找到12个文件引用了helper.ts：
- src/components/Header.tsx
- src/components/Footer.tsx
- src/services/api.ts
- ...（共12个文件）
```

### 步骤 2：执行文件重命名

**[B-06] 终端代理授权请求 #002**：

```markdown
## 授权请求 #002

**操作类型**: 文件操作
**风险等级**: 中风险
**目标**: mv src/utils/helper.ts src/utils/string-helper.ts

### 操作详情
重命名文件：helper.ts → string-helper.ts

### AI安全评估
- **风险分类**: SAFE
- **潜在影响**:
  - 文件移动，不会丢失数据
  - 会导致现有引用失效（需要后续修复）
- **警告信息**:
  ℹ️ 重命名后需要更新所有12个引用文件
  ℹ️ 建议先用git暂存当前更改

### 请求
[中风险] 请批准执行。
```

**用户**: 批准

**执行结果**：
```
文件已成功重命名
- 原路径: src/utils/helper.ts
- 新路径: src/utils/string-helper.ts
```

### 步骤 3：批量更新import语句

**[B-06] 终端代理授权请求 #003**：

```markdown
## 授权请求 #003

**操作类型**: 批量修改
**风险等级**: 高风险
**目标**: 更新12个文件中的import语句

### 操作详情
使用sed批量替换：
./utils/helper → ./utils/string-helper
（在12个文件中）

### AI安全评估
- **风险分类**: HIGH_RISK_FILESYSTEM_CHANGE
- **潜在影响**:
  - 修改12个源文件的import语句
  - 如果正则表达式有误可能导致代码损坏
- **警告信息**:
  ⚠️ 批量修改操作，建议逐文件确认
  ⚠️ 确保已git commit当前状态
  ⚠️ 建议先在1个文件上测试替换规则

### 建议的安全流程
1. 先git commit当前状态
2. 在Header.tsx上测试替换
3. 确认无误后对剩余文件执行

### 请求
[高风险] 请确认已commit并批准。（输入"确认"继续）
```

**用户**: 确认

**执行结果**：
```
成功更新12个文件的import语句：
✓ src/components/Header.tsx
✓ src/components/Footer.tsx
✓ src/services/api.ts
... (共12个文件)

无错误，所有替换均成功
```

### 步骤 4：运行测试验证

**[B-06] 终端代理授权请求 #004**：

```markdown
## 授权请求 #004

**操作类型**: 执行
**风险等级**: 低风险
**目标**: npm test

### 操作详情
运行项目测试套件验证重构未破坏功能

### AI安全评估
- **风险分类**: SAFE
- **潜在影响**:
  - 读取源文件
  - 执行测试代码
  - 占用CPU资源（约30秒-2分钟）
- **警告信息**: 无

### 请求
[低风险] 请批准执行。
```

**用户**: 批准

**执行结果**：
```
npm test

> project@1.0.0 test
> jest

 PASS  src/utils/string-helper.test.ts
 PASS  src/components/Header.test.tsx
 PASS  src/services/api.test.ts
 ...

Test Suites: 15 passed, 15 total
Tests:       127 passed, 127 total
Snapshots:   0 total
Time:        45.234 s

✓ 所有测试通过！
```

### 步骤 5：最终验证与清理

**[B-06] 终端代理授权请求 #005**：

```markdown
## 授权请求 #005

**操作类型**: 验证
**风险等级**: 低风险
**目标**: 运行TypeScript类型检查

### 操作详情
运行tsc --noEmit验证没有类型错误

### AI安全评估
- **风险分类**: SAFE
- **潜在影响**: 无，仅类型检查
- **警告信息**: 无

### 请求
[低风险] 请批准执行。
```

**用户**: 批准

**执行结果**：
```
tsc --noEmit

✓ No type errors found!
```

## 最终输出

```markdown
## 重构完成报告

### 执行摘要
成功将helper.ts重命名为string-helper.ts，并更新所有引用

### 执行统计
- 重命名文件: 1个
- 更新的文件: 12个
- 修改的import语句: 12处
- 测试结果: 127/127通过
- 类型检查: 无错误

### 影响范围
**修改的文件**:
1. src/utils/helper.ts → src/utils/string-helper.ts (重命名)
2. src/components/Header.tsx (更新import)
3. src/components/Footer.tsx (更新import)
... (共12个文件更新import)

### 验证结果
✓ 所有单元测试通过
✓ TypeScript类型检查通过
✓ 无构建错误

### 建议
- 可以安全地commit这些更改
- 建议commit信息: "refactor: rename helper.ts to string-helper.ts"
- 如需回滚，使用: git reset --hard HEAD~1
```

## 关键要点

1. **分步执行**：将复杂重构分解为多个安全的小步骤
2. **风险评估**：每步都进行AI安全审查，高风险操作需要确认
3. **灵魂协同**：与代码库生态学家协同分析影响范围
4. **全程验证**：每步完成后运行测试和类型检查
5. **可回滚**：建议在关键步骤前git commit，确保可恢复

## 经验总结

- ✅ **AI安全顾问**有效识别了批量修改的风险
- ✅ **分步确认**机制防止了一次性执行过多高风险操作
- ✅ **透明报告**让用户清楚了解每一步的影响
- ✅ **测试验证**确保重构没有破坏现有功能
- ✅ **类型检查**捕获了潜在的类型不匹配问题

这个示例展示了终端代理如何通过AI辅助安全审查、多层授权机制、完整的验证流程，实现安全可靠的代码重构操作。
