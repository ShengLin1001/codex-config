---
name: p-git-commit
description: Generate concise Chinese conventional commit messages in the user's preferred VS Code extension style, with type, optional scope, gitmoji-style icon code, short title, and brief description. Use when the user asks to write, format, polish, or choose a git commit message.
---

# P Git Commit

## Overview

生成简洁、中文、便于浏览的 Git commit 信息。默认只输出建议的 commit message；只有用户明确要求提交时，才执行 `git add` / `git commit`。

## Workflow

1. 先检查改动：

```bash
git status --short
git diff --stat
git diff
```

2. 用改动的主要目的选择类型：

- `feat`: 新功能
- `fix`: 修 bug
- `docs`: 文档
- `style`: 代码风格、命名、清理，不改变行为
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建、依赖、配置、杂项

3. scope 只在确实有清晰模块时添加，例如 `DFT`、`docs`、`cli`。没有清晰模块就省略。

4. 选择一个 emoji code，优先贴合改动意图：

- `:sparkles:` 新功能
- `:bug:` 修 bug
- `:memo:` 文档
- `:art:` 整理、结构、可读性
- `:recycle:` 重构
- `:white_check_mark:` 测试或验证
- `:wrench:` 配置、工具
- `:fire:` 删除明确无用内容

## Output Format

首行使用：

```text
<type>(<scope>): <emoji-code> <中文标题>
```

没有 scope 时：

```text
<type>: <emoji-code> <中文标题>
```

如需要简要描述，在空一行后加 1 句中文正文，不写长段落：

```text
feat(DFT): :sparkles: 添加收敛状态检查

支持批量扫描子任务结果，并在提交前给出简洁统计。
```

## Style

- 标题控制在 30 个中文字符左右，动词开头，避免句号。
- 正文最多 1 句；如果改动很小，可以只给首行。
- 中文为主，保留必要的英文模块名、函数名、文件名。
- 不夸大改动，不把多个无关目的硬塞进一条 commit。
- 如果改动混杂，先建议拆分提交；用户要求单条时，选择主目的。

## Commit

用户明确要求提交时，先展示将使用的消息，再只暂存相关文件。多行消息用：

```bash
git commit -m "<type>(<scope>): <emoji-code> <中文标题>" -m "<简要描述>"
```
