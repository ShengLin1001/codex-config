---
name: p-skill-creator
description: PJ-created workflow for creating new Codex skills, publishing them into the codex-config repository, committing and pushing the repository, and refreshing the installed skills with p-skill-installer. Use when the user asks to create a PJ skill, turn a repeated local workflow into a reusable skill, move a generated skill into the `$PJ_CODEX_CONFIG/skills` repository layout, or publish/update skills through `https://github.com/ShengLin1001/codex-config.git`.
---

# P Skill Creator

## Overview

Create PJ-owned Codex skills and publish them through the `codex-config`
repository so they can be installed and updated with `p-skill-installer`.

## Repository

Resolve the repository path from `PJ_CODEX_CONFIG`:

```bash
printf '%s\n' "${PJ_CODEX_CONFIG:-}"
```

If `PJ_CODEX_CONFIG` is empty, stop and ask the user to provide the local
`codex-config` repository path. Do not guess. After the user provides a path,
use it as the repository root for the current task.

The target layout is:

```text
$PJ_CODEX_CONFIG/skills/<skill-name>/SKILL.md
$PJ_CODEX_CONFIG/skills/<skill-name>/agents/openai.yaml
```

## Create

Use the system `skill-creator` initializer to create the skill in a temporary
or staging location first. Use the Codex-specific Python environment:

```bash
/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python \
  /public3/home/scg6928/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  <skill-name> \
  --path <staging-parent> \
  --interface display_name='<Display Name>' \
  --interface short_description='<Short description>' \
  --interface default_prompt='Use $<skill-name> to <do the workflow>.'
```

Then edit only the generated skill files needed for the requested workflow.
Keep `SKILL.md` concise, imperative, and focused on reusable procedural
knowledge. Do not add README, changelog, installation guide, or other auxiliary
documentation unless the user explicitly asks.

Validate the skill before publishing:

```bash
/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python \
  /public3/home/scg6928/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  <path-to-staged-skill>
```

## Move Into Repository

Move the finished skill directory into:

```text
$PJ_CODEX_CONFIG/skills/<skill-name>
```

If a same-named skill already exists in the repository, inspect it first and
update it in place. Do not overwrite or remove it blindly. Respect the user's
rule against bulk deletion; never use `rm -rf` or recursive delete commands.

## Commit And Push

From `$PJ_CODEX_CONFIG`, inspect changes before committing:

```bash
git status --short
git diff -- skills/<skill-name>
```

Commit only the intended skill files:

```bash
git add skills/<skill-name>
git commit -m "Add <skill-name> skill"
git push
```

If unrelated changes exist, leave them untouched and commit only the new or
updated skill path.

## Install Or Update Locally

After pushing, use the `p-skill-installer` workflow to refresh the installed
skills from GitHub:

```bash
npx --yes skills update -g -y
```

If the new skill is not installed by update because it was not previously in the
global lock, install from the repo with:

```bash
npx --yes skills add https://github.com/ShengLin1001/codex-config.git -g --agent codex --skill '*' --yes
```

Then verify Codex discovery:

```bash
npx --yes skills list -g -a codex
```

If the CLI installs under `~/.agents/skills` but reports the new skill as
`not linked`, create only a single explicit symlink:

```bash
ln -s ~/.agents/skills/<skill-name> ~/.codex/skills/<skill-name>
```

Do not manually edit `~/.agents/skills` or `~/.agents/.skill-lock.json`.
