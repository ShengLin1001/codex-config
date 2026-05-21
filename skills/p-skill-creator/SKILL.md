---
name: p-skill-creator
description: PJ 创建的工作流，用于创建新的 Codex skills，将它们发布到 codex-config 仓库，提交并推送该仓库，并使用 p-skill-installer 刷新已安装的 skills。当用户要求创建 PJ skill、将重复性的本地工作流转化为可复用 skill、把生成的 skill 移动到 `$PJ_CODEX_CONFIG/skills` 仓库布局中，或通过 `https://github.com/ShengLin1001/codex-config.git` 发布/更新 skills 时使用。
---

# P Skill Creator

## 概述

创建 PJ 自有的 Codex skills，并通过 `codex-config`
仓库发布它们，以便使用 `p-skill-installer` 进行安装和更新。

## 仓库

从 `PJ_CODEX_CONFIG` 解析仓库路径：

~~~bash
printf '%s\n' "${PJ_CODEX_CONFIG:-}"
~~~

如果 `PJ_CODEX_CONFIG` 为空，则停止并要求用户提供本地
`codex-config` 仓库路径。不要猜测。用户提供路径后，
将其作为当前任务的仓库根目录。

目标布局如下：

~~~text
$PJ_CODEX_CONFIG/skills/<skill-name>/SKILL.md
$PJ_CODEX_CONFIG/skills/<skill-name>/agents/openai.yaml
~~~

## 创建

先使用系统 `skill-creator` 初始化器在临时位置或暂存位置创建 skill。
使用 Codex 专用的 Python 环境：

~~~bash
python \
  ~/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  <skill-name> \
  --path <staging-parent> \
  --interface display_name='<Display Name>' \
  --interface short_description='<Short description>' \
  --interface default_prompt='Use $<skill-name> to <do the workflow>.'
~~~

然后只编辑所请求工作流所需的已生成 skill 文件。
保持 `SKILL.md` 简洁、命令式，并聚焦于可复用的流程性知识。
除非用户明确要求，否则不要添加 README、更新日志、安装指南或其他辅助文档。

发布前验证 skill：

~~~bash
python \
  ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  <path-to-staged-skill>
~~~

## 移入仓库

将完成后的 skill 目录移动到：

~~~text
$PJ_CODEX_CONFIG/skills/<skill-name>
~~~

如果仓库中已经存在同名 skill，先检查它，并在原位置更新。
不要盲目覆盖或删除它。遵守用户禁止批量删除的规则；
绝不要使用 `rm -rf` 或递归删除命令。

## 提交并推送

在 `$PJ_CODEX_CONFIG` 中，提交前先检查改动：

~~~bash
git status --short
git diff -- skills/<skill-name>
~~~

只提交目标 skill 文件：

~~~bash
git add skills/<skill-name>
git commit -m "Add <skill-name> skill"
git push
~~~

如果存在无关改动，保持它们不变，只提交新增或更新的 skill 路径。

## 本地安装

推送后，使用 `p-skill-installer` 的安装工作流，从 GitHub 安装或刷新仓库中的 skills：

~~~bash
npx --yes skills add https://github.com/ShengLin1001/codex-config.git -g --agent codex --skill '*' --yes
~~~

这里使用 install 而不是 update，因为新创建的 skills 可能尚未存在于全局 lock 中。
仓库安装过一次后，之后的常规刷新仍然可以使用：

~~~bash
npx --yes skills update -g -y
~~~

然后验证 Codex 是否能发现这些 skills：

~~~bash
npx --yes skills list -g -a codex
~~~

如果 CLI 安装到了 `~/.agents/skills`，但报告新的 skill 为
`not linked`，则只创建一个明确的符号链接：

~~~bash
ln -s ~/.agents/skills/<skill-name> ~/.codex/skills/<skill-name>
~~~

不要手动编辑 `~/.agents/skills` 或 `~/.agents/.skill-lock.json`。