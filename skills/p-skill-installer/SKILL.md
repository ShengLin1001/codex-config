---
name: p-skill-installer
description: PJ-created skill installer for installing, updating, and verifying Codex skills with the npx `skills` CLI on this CentOS HPC environment. Use when the user asks to add skills from GitHub repos with `npx skills add`, install user-level/global skills, verify Codex skill discovery, troubleshoot npx/GitHub HTTPS clone behavior, fall back from HTTPS to SSH when `git remote-https` fails, or document the supported skill update workflow. This skill preserves CLI-managed lock/update behavior and avoids manual skill file updates.
---

# P Skill Installer

## Overview

Use this workflow to install GitHub-hosted skills through the official `skills`
CLI invoked by `npx`, keeping installs global/user-level and updateable through
the CLI. Do not replace this with manual zip downloads, local checkouts, or
direct edits under `~/.agents/skills`.

## Environment

Use the local Git and curl runtime that work on this host:

```bash
export PATH=/public3/home/scg6928/mysoft/tools/git/2.43.7/bin:$PATH
export LD_LIBRARY_PATH=/public3/soft/curl/lib:$LD_LIBRARY_PATH
```

Rely on the base proxy exported by `~/.bash_soft_env`:

```bash
export http_proxy="http://127.0.0.1:37897"
export https_proxy="http://127.0.0.1:37897"
export HTTP_PROXY="http://127.0.0.1:37897"
export HTTPS_PROXY="http://127.0.0.1:37897"
```

Do not add Git-specific `http.proxy` or `https.proxy` values in `~/.gitconfig`.
Do not add a GitHub `insteadOf` rewrite from HTTPS to SSH unless the user
explicitly asks for an SSH-only workaround.

## Install

Use global mode and the lower-case Codex agent id:

```bash
npx --yes skills add vercel-labs/agent-skills -g --agent codex --skill '*' --yes
```

For another GitHub repo, keep the same shape:

```bash
npx --yes skills add owner/repo -g --agent codex --skill '*' --yes
```

Use the HTTPS shorthand first. If the repo is not a `skills`-compatible repo,
confirm its structure has `skills/<skill-name>/SKILL.md` before trying workarounds.

## Verify

First verify GitHub HTTPS access without SSH rewriting:

```bash
GIT_TRACE=1 git ls-remote https://github.com/vercel-labs/agent-skills.git HEAD
```

The trace should show `git remote-https ...`, not `ssh ... git@github.com`, and
the command should return a commit hash for `HEAD`.

If this HTTPS check fails, convert the GitHub source to SSH for the install
instead of manually downloading or copying skill files:

```bash
npx --yes skills add git@github.com:vercel-labs/agent-skills.git -g --agent codex --skill '*' --yes
```

For another GitHub repo, convert:

```text
https://github.com/owner/repo.git
```

to:

```text
git@github.com:owner/repo.git
```

Use SSH only as the fallback after confirming `git remote-https` is not working
through the base proxy environment.

Then verify the CLI install path:

```bash
npx --yes skills add vercel-labs/agent-skills -g --agent codex --skill '*' --yes
```

Expected result: the CLI reports the HTTPS GitHub source, clones the repository,
finds the skills, installs them under `~/.agents/skills`, and maps them to Codex.

Verify Codex discovery:

```bash
npx --yes skills list -g -a codex
```

Expected result: installed skills list `Agents: Codex`.

Verify update support:

```bash
npx --yes skills update -g -y
```

Expected result: the CLI checks global skills and reports they are updated or
already up to date. Future updates must use this command, not manual file edits.

## Discovery Links

Codex reads user-level skills from `~/.codex/skills`. The `skills` CLI may place
global skill contents under `~/.agents/skills`. If installed skills are not
visible to Codex after the CLI succeeds, create only explicit per-skill symlinks
from `~/.codex/skills/<skill-name>` to `~/.agents/skills/<skill-name>`.

Those symlinks are only for Codex discovery. Keep the source contents and
`.skill-lock.json` managed by `npx skills`.

## Troubleshooting

If HTTPS clone fails, inspect the environment before changing Git configuration:

```bash
env | grep -E '^(http_proxy|https_proxy|HTTP_PROXY|HTTPS_PROXY)='
git config --global --show-origin --get-regexp '^(http|https)\.proxy|^url\.'
```

The preferred state is no Git-specific proxy and no GitHub `insteadOf` rewrite.
If stale Git proxy or rewrite entries exist, remove only those specific Git
config keys after confirming with the user.
