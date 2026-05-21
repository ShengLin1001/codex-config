# 项目协作说明

本项目用于维护 Codex 配置、脚本和自定义 skills。

## 更新流程

更新本项目时按以下顺序执行：

1. 先执行 `git pull`，同步远端最新内容。
2. 提交前使用 `$p-git-commit` skill 生成 commit message。
3. 完成提交后执行 `git push`，推送到远端仓库。

## Commit 规范

生成 Git commit 信息时默认使用 `$p-git-commit`：

- 先检查 `git status --short`、`git diff --stat` 和 `git diff`。
- commit message 使用中文、Conventional Commits type 和 gitmoji shortcode。
- 只有用户明确要求提交时，才执行 `git add` 和 `git commit`。

