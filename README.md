# codex-config

This repository maintains personal Codex configuration, global instructions, restore scripts, and custom skills. It is intended to make the same Codex setup easy to restore on this CentOS HPC host or on a new environment.

## Repository Contents

- `AGENTS.md`: collaboration and update rules for this repository.
- `codex/config.toml`: repository copy of `~/.codex/config.toml`.
- `codex/AGENTS.md`: repository copy of `~/.codex/AGENTS.md`, used to preserve Codex global instructions.
- `skills/`: custom Codex skills maintained in this repository.
- `scripts/copy-codex-files.sh`: copies `AGENTS.md` and `config.toml` from `~/.codex` into this repository's `codex/` directory.
- `scripts/restore-codex-files.sh`: restores Codex configuration from this repository into `~/.codex`.
- `scripts/reinstall-skills.sh`: reinstalls external skill repositories through `npx skills`.

## Common Workflows

### Sync From the Current Codex Environment

After changing `~/.codex/AGENTS.md` or `~/.codex/config.toml`, run this from the repository root:

```bash
bash scripts/copy-codex-files.sh
```

This updates `codex/AGENTS.md` and `codex/config.toml`.

### Restore Into the Codex Environment

Run this from the repository root:

```bash
bash scripts/restore-codex-files.sh
```

This restores the repository copy of the Codex configuration into `~/.codex`.

### Reinstall External Skills

Run this from the repository root:

```bash
bash scripts/reinstall-skills.sh
```

The script reads the `repos` array in `scripts/reinstall-skills.sh` and installs those skill repositories through `npx skills add`.

After installing a new skill repository, add its repository address to the `repos` array in `scripts/reinstall-skills.sh`. If the repository is already listed, do not add it again.

## Environment Rules

The current host is a CentOS HPC environment. Codex-related Python work should use this isolated virtual environment by default:

```bash
/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python
```

Do not install Codex-related Python packages into the main `dft` virtual environment.

If a required command is missing or its version is unsuitable, first check whether suitable software is available through `module avail`.

## Git Workflow

When updating this repository, follow this order:

1. Run `git pull` to sync the remote branch.
2. Use `$p-git-commit` to generate a Chinese commit message.
3. Run `git push` to push changes to GitHub.
