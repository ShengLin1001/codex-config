---
name: p-git-commit
description: For test 生成简洁的中文 commit message，遵循 Conventional Commits v1.0.0、@commitlint/config-conventional 的 type 枚举，以及官方 gitmoji shortcode 含义。当用户要求编写、格式化、润色、选择或创建 git commit message 时使用。
---

# P Git Commit

## 概述

For test 
生成简洁、中文、易于快速浏览的 Git commit message。默认情况下，只输出建议的 commit message。只有当用户明确要求提交时，才运行 `git add` 或 `git commit`。

本 skill 遵循三层约定：

- Conventional Commits v1.0.0：格式、`feat`、`fix` 和 `BREAKING CHANGE` 语义。
- `@commitlint/config-conventional`：常用 type 枚举。
- 官方 gitmoji 列表：shortcode 含义。

## 工作流

1. 先检查改动：

~~~bash
git status --short
git diff --stat
git diff
~~~

2. 选择 type。优先使用 `@commitlint/config-conventional` 中的 11 种 type：

- `feat`：新增功能。对应 Conventional Commits 中的 MINOR。
- `fix`：修复 bug。对应 Conventional Commits 中的 PATCH。
- `build`：构建系统或外部依赖变更，例如 make、npm、pip 或 docker。
- `chore`：杂项改动，不修改 src 或 test 文件。
- `ci`：CI 配置或脚本变更。
- `docs`：仅文档改动。
- `perf`：性能优化。
- `refactor`：代码重构，既不修复 bug，也不新增功能。
- `revert`：回退之前的 commit。
- `style`：格式、空白、标点或代码风格改动，不影响代码含义。
- `test`：添加缺失测试或修正已有测试。

3. 只有在存在明确模块时才添加 scope，例如 `DFT`、`Lammps`、`N2P2`、`plot` 或 `workflow`。如果没有明确模块，则省略 scope。

4. 对于破坏性变更，使用以下任一形式标记：

- 在 type 或 scope 后添加 `!`：`feat(api)!: :boom: 修改配置格式`
- 添加 footer：`BREAKING CHANGE: <description>`

5. 选择一个能够表达改动意图的 gitmoji shortcode。不要只按 type 机械映射；如果另一个 shortcode 更准确，应根据具体意图选择。

## 输出格式

使用以下 header 格式：

~~~text
<type>(<scope>): <emoji-code> <中文标题>
~~~

不带 scope 时：

~~~text
<type>: <emoji-code> <中文标题>
~~~

对于破坏性变更：

~~~text
<type>(<scope>)!: <emoji-code> <中文标题>
~~~

如果需要简短正文，在空行后添加一句中文说明。不要写长段落：

~~~text
feat(DFT): :sparkles: 添加收敛状态检查

支持批量扫描子任务结果，并在提交前给出简洁统计。
~~~

## Type 到 Emoji 的默认映射

以下是默认优先选择。如果具体改动更适合另一个 gitmoji，则根据具体意图选择。

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

## Gitmoji 参考

官方 gitmoji shortcode 含义如下。commit message 中使用 shortcode，而不是 Unicode emoji。

- `:art:`：改进代码结构或格式。
- `:zap:`：提升性能。
- `:fire:`：删除代码或文件。
- `:bug:`：修复 bug。
- `:ambulance:`：关键热修复。
- `:sparkles:`：引入新功能。
- `:memo:`：新增或更新文档。
- `:rocket:`：部署相关改动。
- `:lipstick:`：新增或更新 UI 与样式文件。
- `:tada:`：初始化项目。
- `:white_check_mark:`：新增、更新或通过测试。
- `:lock:`：修复安全或隐私问题。
- `:closed_lock_with_key:`：新增或更新密钥。
- `:bookmark:`：发布或版本标签。
- `:rotating_light:`：修复编译器或 linter 警告。
- `:construction:`：进行中的工作。
- `:green_heart:`：修复 CI 构建。
- `:arrow_down:`：降级依赖。
- `:arrow_up:`：升级依赖。
- `:pushpin:`：将依赖固定到特定版本。
- `:construction_worker:`：新增或更新 CI 构建系统。
- `:chart_with_upwards_trend:`：新增或更新分析、追踪或指标代码。
- `:recycle:`：重构代码。
- `:heavy_plus_sign:`：添加依赖。
- `:heavy_minus_sign:`：移除依赖。
- `:wrench:`：新增或更新配置文件。
- `:hammer:`：新增或更新开发脚本。
- `:globe_with_meridians:`：国际化或本地化。
- `:pencil2:`：修正拼写或文本错误。
- `:poop:`：编写需要后续改进的代码。
- `:rewind:`：回退改动。
- `:twisted_rightwards_arrows:`：合并分支。
- `:package:`：新增或更新编译产物或包。
- `:alien:`：因外部 API 变化而更新代码。
- `:truck:`：移动或重命名资源，例如文件、路径或路由。
- `:page_facing_up:`：新增或更新许可证。
- `:boom:`：引入破坏性变更。
- `:bento:`：新增或更新资源文件。
- `:wheelchair:`：改进无障碍访问。
- `:bulb:`：新增或更新源码注释。
- `:beers:`：编写不严肃或临时代码。
- `:speech_balloon:`：新增或更新文本与字面量。
- `:card_file_box:`：数据库相关改动。
- `:loud_sound:`：新增或更新日志。
- `:mute:`：移除日志。
- `:busts_in_silhouette:`：新增或更新贡献者。
- `:children_crossing:`：改善用户体验或可用性。
- `:building_construction:`：架构性改动。
- `:iphone:`：响应式设计改动。
- `:clown_face:`：mock 相关改动。
- `:egg:`：新增或更新彩蛋。
- `:see_no_evil:`：新增或更新 `.gitignore`。
- `:camera_flash:`：新增或更新快照。
- `:alembic:`：实验性改动。
- `:mag:`：改进 SEO。
- `:label:`：新增或更新类型。
- `:seedling:`：新增或更新种子文件。
- `:triangular_flag_on_post:`：新增、更新或移除 feature flag。
- `:goal_net:`：捕获错误。
- `:dizzy:`：新增或更新动画与过渡效果。
- `:wastebasket:`：弃用后续应清理的代码。
- `:passport_control:`：授权、角色或权限代码。
- `:adhesive_bandage:`：简单修复非关键问题。
- `:monocle_face:`：数据探索或检查。
- `:coffin:`：移除死代码。
- `:test_tube:`：添加失败测试。
- `:necktie:`：新增或更新业务逻辑。
- `:stethoscope:`：新增或更新健康检查。
- `:bricks:`：基础设施相关改动。
- `:technologist:`：改善开发者体验。
- `:money_with_wings:`：赞助或资金基础设施。
- `:thread:`：多线程或并发相关代码。
- `:safety_vest:`：验证相关代码。
- `:airplane:`：改善离线支持。
- `:t-rex:`：添加向后兼容代码。

## 风格

- 标题控制在约 30 个中文字符。
- 标题以动词开头，不以句号结尾。
- header 控制在 100 个字符以内。
- 正文最多使用一句话；对于小改动，只输出 header。
- 以中文为主要语言，同时保留必要的英文模块名、函数名和文件名。
- 不夸大改动。
- 不要把多个无关目的强行塞进一个 commit。
- 如果改动内容混杂，先建议拆分成多个 commit。如果用户要求单个 commit，则选择主要目的。

## 提交

当用户明确要求提交时，先展示将要使用的 message，然后只暂存相关文件。例如：“$p-git-commit 提交” 意味着需要执行 `git commit` 命令暂存相关文件，不需要`git pull` 和 `git push`。

多行 message 使用以下形式：

~~~bash
git commit -m "<type>(<scope>): <emoji-code> <中文标题>" -m "<简短中文说明>"
~~~