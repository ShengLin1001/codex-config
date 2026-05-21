# Project Collaboration Instructions

This repository maintains Codex configuration, scripts, and custom skills.

## Update Workflow

When updating this project, follow this order:

1. Run `git pull` first to sync the latest remote changes.
2. Before committing, use the `$p-git-commit` skill to generate the commit message.
3. After committing, run `git push` to push changes to the remote repository.

## Commit Rules

When generating Git commit messages, use the `$p-git-commit` skill by default:

- Check `git status --short`, `git diff --stat`, and `git diff` first.
- Commit messages should use Chinese text, Conventional Commits types, and gitmoji shortcodes.
- Only run `git add` and `git commit` when the user explicitly asks to commit.

## Installing User-Level Codex Skills With npx

When installing `vercel-labs/agent-skills`, use the `skills` CLI through `npx` and keep the installation user-level, not repository-level.

Recommended environment on this CentOS HPC host; this is not needed on Windows:

```bash
export PATH=/public3/home/scg6928/mysoft/tools/git/2.43.7/bin:$PATH
export LD_LIBRARY_PATH=/public3/soft/curl/lib:$LD_LIBRARY_PATH
```

Do not set Git-specific proxy values in `~/.gitconfig` for this project.

Do not add a GitHub HTTPS-to-SSH `insteadOf` rewrite unless `git clone` fails.

Use the lower-case Codex agent id:

```bash
npx --yes skills add vercel-labs/agent-skills --global --agent codex --skill '*' --yes
```

Do not install or update these skills from a manually downloaded zip file or local checkout unless the user explicitly asks for a temporary network workaround. Normal installation must come from the GitHub source so that `~/.agents/.skill-lock.json` is created and future updates remain tracked by the CLI.

Future updates must use the CLI update path:

```bash
npx --yes skills update -g -y
```

Do not manually update files under `~/.agents/skills`. Do not edit `~/.agents/.skill-lock.json`.

If cleanup is needed, use the CLI first:

```bash
npx --yes skills remove -g --all
```

Do not use bulk deletion commands such as `rm -rf`. If the CLI leaves directories behind and the user wants them removed, stop and ask the user to delete them manually, unless removing a single explicit file path is sufficient.

Codex reads user-level skills from `~/.codex/skills`. In this environment, the `skills` CLI may create globally managed npx skills under `~/.agents/skills` and create or update the lock file without automatically linking them into `~/.codex/skills`. If this happens, keep the skill contents managed by `npx skills`, and create only explicit per-skill symlinks from `~/.codex/skills/<skill-name>` to `~/.agents/skills/<skill-name>`. These links are only for Codex discovery; updates must still use `npx --yes skills update -g -y`.

After installing a new skill repository, for example with `npx skills add vercel-labs/agent-skills`, record the corresponding repository address in the `repos` array in `scripts/reinstall-skills.sh`. If that repository is already listed in `repos`, do not add it again.
