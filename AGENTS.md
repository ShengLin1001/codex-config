# 项目协作说明

本仓库用于维护 Codex 配置、恢复脚本和自定义 skills。

## 范围

保持此文件聚焦于仓库级规则和 skill 路由。不要重复 `skills/*/SKILL.md` 中已经包含的详细流程。

## 更新工作流

更新此项目时，按以下顺序执行：

1. 先运行 `git pull`，同步远程仓库的最新改动。
2. 只有在查看实际 diff 并判断改动是否需要拆分后，才进行 commit。
3. 使用 `$p-git-commit` 生成 commit message，并处理 commit message 规则。
4. commit 后，运行 `git push` 将改动推送到远程仓库。

## Skill 仓库跟踪

安装新的 skill 仓库后，将其仓库地址记录到 `scripts/reinstall-skills.sh` 中的 `repos` 数组里。如果该仓库已经列出，则不要重复添加。

## 其他说明

在未显式说明更新时，不要按照上述工作流运行。例如 “生成 commit” 意味着无须执行 `git pull` 或 `git push`，只需生成 commit message 并运行 `git commit` 即可。