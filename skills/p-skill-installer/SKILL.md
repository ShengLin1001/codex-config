---
name: p-skill-installer
description: For test, PJ 创建的 skill 安装器，通过 npx `skills` CLI 安装、更新并验证 Codex skills。当用户要求使用 `npx skills add` 从 GitHub 仓库添加 skills、安装用户级/全局 skills、验证 Codex skill 发现、排查 npx/GitHub HTTPS 克隆行为、在 `git remote-https` 失败时从 HTTPS 回退到 SSH，或记录受支持的 skill 更新工作流时使用。该 skill 保留 CLI 管理的 lock/update 行为，并避免手动更新 skill 文件。
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

预期结果：CLI 报告 HTTPS GitHub source，克隆仓库，发现 skills，并将它们安装到 `~/.agents/skills` 下。

查看 CLI 的全局安装状态：

~~~bash
npx --yes skills list -g -a codex
~~~

如果这里显示 `Agents: not linked`，不要因此创建 `~/.codex/skills/<skill-name>` 符号链接。当前 Codex 可以直接从 `~/.agents/skills` 发现并调用用户级 skills；`not linked` 只是 `skills` CLI 的 agent linkage 显示，不等同于 Codex 不可用。真正的验证方式是在 Codex 中调用对应 skill。

验证更新支持：

~~~bash
npx --yes skills update -g -y
~~~

预期结果：CLI 检查全局 skills，并报告它们已更新或已经是最新版本。未来更新必须使用此命令，而不是手动编辑文件。

## 发现链接

Codex 从 `~/.agents/skills` 读取用户级 skills。无需在 `~/.codex/skills/<skill-name>` 创建符号链接指向 `~/.agents/skills/<skill-name>`。不要因为 `npx skills list -g -a codex` 显示 `Agents: not linked` 就创建符号链接；只有在用户明确要求调试 Codex 发现路径，且实测 Codex 无法调用该 skill 时，才进一步排查。
