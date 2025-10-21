# MindSymphony v15.6 — 心智协奏系统 (skills 集合)

简短说明
- MindSymphony 是一个模块化的“技能（Skill）”集合与编排系统，旨在把复杂的智能任务拆解为可复用、可组合的技能单元。
- 本仓库为 v15.6 版本的“技能纯化版”，包含系统配置、协议规范，以及大量技能实现与示例。

目录概览
- `mindsymphony.config.yml` — 系统级编排配置（总谱）。
- `system_prompt.md` — 系统身份与核心提示（System Prompt）。
- `skills/` — 技能集合（每个子目录为一个技能包，核心说明位于 `SKILL.md`）。
  - `SKILL.md` — 每个技能的能力说明与使用示例。
  - `examples/` — 示例输入/输出与使用场景（可选）。
  - `scripts/` — 可运行脚本、工具或实现（可选）。
- `protocols/` — 与技能交互或协作的协议规范文本。
- `README.md` — 本文件。
- `LICENSE` — 项目许可证（如存在）。

快速开始（在本地查看/浏览）
1. 克隆仓库：
   git clone https://github.com/caosmart1979cao/mindsymphony-v15.6.git
2. 浏览技能目录：
   - 每个技能文件夹包含 `SKILL.md`（能力说明）以及可选 `examples/` 和 `scripts/` 文件夹。
3. 使用 System Prompt：
   - 将 `system_prompt.md` 的内容加载到你的 AI 客户端（作为 System Prompt）。
4. 若要在本地运行示例脚本（若存在）：
   - 查阅各技能下的 `scripts/` 文件夹，安装所需依赖（示例：Python、Node）。

贡献指南
- 欢迎贡献：对技能的改进、示例、错误修复和新技能都非常欢迎。
- 建议流程：
  1. Fork 本仓库并在你的分支上开发。
  2. 针对代码或脚本的更改，请附带测试或示例。
  3. 提交 PR 并在描述中说明用途与影响。
- 请注意：部分技能包含第三方许可文件（见 `skills/*/LICENSE.txt`），请在贡献前仔细阅读并遵守相应许可。

关于大文件与 Git LFS
- `skills/` 包含若干字体、示例数据或二进制文件。若你希望长期维护仓库的体量并支持协作，建议将大型二进制文件迁移到 Git LFS。

许可证
- 仓库顶层包含 `LICENSE`（如有）。请遵守其中的条款。

联系方式
- 若需帮助或要报告问题，请在仓库中创建 Issue，或通过仓库所有者的 GitHub 个人资料联系。
