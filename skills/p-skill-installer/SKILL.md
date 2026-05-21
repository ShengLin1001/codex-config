---
name: p-skill-installer
description: PJ 创建的 skill 安装器，通过 npx `skills` CLI 安装、更新并验证 Codex skills。当用户要求使用 `npx skills add` 从 GitHub 仓库添加 skills、安装用户级/全局 skills、验证 Codex skill 发现、排查 npx/GitHub HTTPS 克隆行为、在 `git remote-https` 失败时从 HTTPS 回退到 SSH，或记录受支持的 skill 更新工作流时使用。该 skill 保留 CLI 管理的 lock/update 行为，并避免手动更新 skill 文件。
---

# P Skill Installer

## 概述

使用此工作流通过由 `npx` 调用的官方 `skills` CLI 安装托管在 GitHub 上的 skills，并保持安装为全局/用户级，使其可以通过 CLI 更新。不要用手动下载 zip、本地 checkout，或直接编辑 `~/.agents/skills` 下的文件来替代此流程。

## 安装

使用全局模式，并使用小写的 Codex agent id：

~~~bash
npx --yes skills add vercel-labs/agent-skills -g --agent codex --skill '*' --yes
~~~

对于其他 GitHub 仓库，保持相同格式：

~~~bash
npx --yes skills add owner/repo -g --agent codex --skill '*' --yes
~~~

优先使用 HTTPS 简写形式。如果该仓库不是 `skills` 兼容仓库，应先确认其结构中包含 `skills/<skill-name>/SKILL.md`，再尝试其他 workaround。

## 验证

首先在不使用 SSH 重写的情况下验证 GitHub HTTPS 访问：

~~~bash
GIT_TRACE=1 git ls-remote https://github.com/vercel-labs/agent-skills.git HEAD
~~~

trace 应显示 `git remote-https ...`，而不是 `ssh ... git@github.com`，并且该命令应返回 `HEAD` 对应的 commit hash。

如果此 HTTPS 检查失败，则在安装时将 GitHub source 转换为 SSH，而不是手动下载或复制 skill 文件：

~~~bash
npx --yes skills add git@github.com:vercel-labs/agent-skills.git -g --agent codex --skill '*' --yes
~~~

对于其他 GitHub 仓库，将：

~~~text
https://github.com/owner/repo.git
~~~

转换为：

~~~text
git@github.com:owner/repo.git
~~~

然后验证 CLI 安装路径：

~~~bash
npx --yes skills add vercel-labs/agent-skills -g --agent codex --skill '*' --yes
~~~

预期结果：CLI 报告 HTTPS GitHub source，克隆仓库，发现 skills，将它们安装到 `~/.agents/skills` 下，并映射到 Codex。

验证 Codex 是否能发现这些 skills：

~~~bash
npx --yes skills list -g -a codex
~~~

预期结果：已安装 skills 列表中显示 `Agents: Codex`。

验证更新支持：

~~~bash
npx --yes skills update -g -y
~~~

预期结果：CLI 检查全局 skills，并报告它们已更新或已经是最新版本。未来更新必须使用此命令，而不是手动编辑文件。

## 发现链接

Codex 从 `~/.codex/skills` 读取用户级 skills。`skills` CLI 可能会把全局 skill 内容放在 `~/.agents/skills` 下。如果 CLI 成功后，已安装的 skills 对 Codex 仍不可见，则只创建明确的逐个 skill 符号链接，从 `~/.codex/skills/<skill-name>` 指向 `~/.agents/skills/<skill-name>`。

这些符号链接仅用于 Codex 发现。source 内容和 `.skill-lock.json` 仍应由 `npx skills` 管理。