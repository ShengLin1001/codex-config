---
name: p-git-commit
description: Generate concise Chinese commit messages that follow Conventional Commits v1.0.0, the @commitlint/config-conventional type enum, and official gitmoji shortcode meanings. Use when the user asks to write, format, polish, choose, or create a git commit message.
---

# P Git Commit

## Overview

生成简洁、中文、便于浏览的 Git commit 信息。默认只输出建议的 commit message；只有用户明确要求提交时，才执行 `git add` / `git commit`。

本 skill 同时遵守三层约定：

- Conventional Commits v1.0.0 规范：格式、`feat`、`fix`、`BREAKING CHANGE` 语义。
- `@commitlint/config-conventional`：常用 type 枚举。
- gitmoji 官方列表：emoji shortcode 及其含义。

## Workflow

1. 先检查改动：

```bash
git status --short
git diff --stat
git diff
```

2. 选择一个 type。优先使用 `@commitlint/config-conventional` 的 11 个 type：

- `feat`: 新功能。对应 Conventional Commits 的 MINOR。
- `fix`: bug 修复。对应 Conventional Commits 的 PATCH。
- `build`: 构建系统或外部依赖变更，例如 make、npm、pip、docker。
- `chore`: 不修改 src 或 test 的其它杂项。
- `ci`: CI 配置或脚本变更。
- `docs`: 仅文档变更。
- `perf`: 性能优化。
- `refactor`: 既不修 bug 也不加功能的代码重构。
- `revert`: 回退之前的提交。
- `style`: 不影响代码含义的格式、空白、标点、风格变更。
- `test`: 添加缺失测试或修正已有测试。

3. scope 只在确实有清晰模块时添加，例如 `DFT`、`Lammps`、`N2P2`、`plot`、`workflow`。没有清晰模块就省略。

4. 如有破坏性变更，必须用以下任一方式标记：

- 在 type/scope 后加 `!`：`feat(api)!: :boom: 修改配置格式`
- 在 footer 中加入：`BREAKING CHANGE: <说明>`

5. 选择一个 gitmoji shortcode。优先选择能表达改动意图的 shortcode，而不是机械按 type 映射。

## Output Format

首行使用：

```text
<type>(<scope>): <emoji-code> <中文标题>
```

没有 scope 时：

```text
<type>: <emoji-code> <中文标题>
```

破坏性变更：

```text
<type>(<scope>)!: <emoji-code> <中文标题>
```

如需要简要描述，在空一行后加 1 句中文正文，不写长段落：

```text
feat(DFT): :sparkles: 添加收敛状态检查

支持批量扫描子任务结果，并在提交前给出简洁统计。
```

## Type To Emoji Defaults

这些是默认优先选择；如果具体改动更适合其它 gitmoji，以具体意图为准。

- `feat`: `:sparkles:`
- `fix`: `:bug:`
- `build`: `:package:`、`:heavy_plus_sign:`、`:heavy_minus_sign:`、`:arrow_up:`、`:arrow_down:`
- `chore`: `:wrench:`、`:hammer:`
- `ci`: `:construction_worker:`、`:green_heart:`
- `docs`: `:memo:`
- `perf`: `:zap:`
- `refactor`: `:recycle:`
- `revert`: `:rewind:`
- `style`: `:art:`
- `test`: `:white_check_mark:`、`:test_tube:`

## Gitmoji Reference

官方 gitmoji shortcode 含义如下。输出 commit 时使用 shortcode，不直接使用 Unicode emoji。

- `:art:`: 改进代码结构或格式。
- `:zap:`: 提升性能。
- `:fire:`: 删除代码或文件。
- `:bug:`: 修复 bug。
- `:ambulance:`: 紧急热修复。
- `:sparkles:`: 引入新功能。
- `:memo:`: 添加或更新文档。
- `:rocket:`: 部署相关。
- `:lipstick:`: 添加或更新 UI 与样式文件。
- `:tada:`: 初始化项目。
- `:white_check_mark:`: 添加、更新或通过测试。
- `:lock:`: 修复安全或隐私问题。
- `:closed_lock_with_key:`: 添加或更新密钥、密文、secrets。
- `:bookmark:`: 发布或版本标签。
- `:rotating_light:`: 修复编译器或 linter 警告。
- `:construction:`: 进行中的工作。
- `:green_heart:`: 修复 CI 构建。
- `:arrow_down:`: 降级依赖。
- `:arrow_up:`: 升级依赖。
- `:pushpin:`: 固定依赖到特定版本。
- `:construction_worker:`: 添加或更新 CI 构建系统。
- `:chart_with_upwards_trend:`: 添加或更新分析、埋点、跟踪代码。
- `:recycle:`: 重构代码。
- `:heavy_plus_sign:`: 添加依赖。
- `:heavy_minus_sign:`: 移除依赖。
- `:wrench:`: 添加或更新配置文件。
- `:hammer:`: 添加或更新开发脚本。
- `:globe_with_meridians:`: 国际化或本地化。
- `:pencil2:`: 修复拼写或文字错误。
- `:poop:`: 写下需要后续改进的坏代码。
- `:rewind:`: 回退变更。
- `:twisted_rightwards_arrows:`: 合并分支。
- `:package:`: 添加或更新编译产物或包。
- `:alien:`: 因外部 API 变化而更新代码。
- `:truck:`: 移动或重命名资源，例如文件、路径、路由。
- `:page_facing_up:`: 添加或更新许可证。
- `:boom:`: 引入破坏性变更。
- `:bento:`: 添加或更新资源文件。
- `:wheelchair:`: 改进无障碍访问。
- `:bulb:`: 添加或更新源码注释。
- `:beers:`: 写下不严肃或临时性质的代码。
- `:speech_balloon:`: 添加或更新文本与字面量。
- `:card_file_box:`: 数据库相关变更。
- `:loud_sound:`: 添加或更新日志。
- `:mute:`: 移除日志。
- `:busts_in_silhouette:`: 添加或更新贡献者。
- `:children_crossing:`: 改进用户体验或可用性。
- `:building_construction:`: 架构层面的变更。
- `:iphone:`: 响应式设计相关。
- `:clown_face:`: mock 相关。
- `:egg:`: 添加或更新彩蛋。
- `:see_no_evil:`: 添加或更新 `.gitignore`。
- `:camera_flash:`: 添加或更新快照。
- `:alembic:`: 实验性变更。
- `:mag:`: 改进 SEO。
- `:label:`: 添加或更新类型。
- `:seedling:`: 添加或更新种子文件。
- `:triangular_flag_on_post:`: 添加、更新或移除 feature flag。
- `:goal_net:`: 捕获错误。
- `:dizzy:`: 添加或更新动画与过渡。
- `:wastebasket:`: 废弃后续需要清理的代码。
- `:passport_control:`: 授权、角色、权限相关代码。
- `:adhesive_bandage:`: 非关键问题的简单修复。
- `:monocle_face:`: 数据探索或检查。
- `:coffin:`: 删除死代码。
- `:test_tube:`: 添加失败测试。
- `:necktie:`: 添加或更新业务逻辑。
- `:stethoscope:`: 添加或更新健康检查。
- `:bricks:`: 基础设施相关变更。
- `:technologist:`: 改进开发者体验。
- `:money_with_wings:`: 赞助或资金相关基础设施。
- `:thread:`: 多线程或并发相关代码。
- `:safety_vest:`: 验证相关代码。
- `:airplane:`: 改进离线支持。
- `:t-rex:`: 添加向后兼容代码。

## Style

- 标题控制在 30 个中文字符左右，动词开头，避免句号。
- header 最长不超过 100 字符。
- 正文最多 1 句；如果改动很小，可以只给首行。
- 中文为主，保留必要的英文模块名、函数名、文件名。
- 不夸大改动，不把多个无关目的硬塞进一条 commit。
- 如果改动混杂，先建议拆分提交；用户要求单条时，选择主目的。

## Commit

用户明确要求提交时，先展示将使用的消息，再只暂存相关文件。多行消息用：

```bash
git commit -m "<type>(<scope>): <emoji-code> <中文标题>" -m "<简要描述>"
```
