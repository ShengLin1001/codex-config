# Project Collaboration Instructions

This repository maintains Codex configuration, restore scripts, and custom skills.

## Scope

Keep this file focused on repository-level rules and skill routing. Do not duplicate detailed procedures that already live in `skills/*/SKILL.md`.

## Update Workflow

When updating this project, follow this order:

1. Run `git pull` first to sync the latest remote changes.
2. Commit only after reviewing the actual diff and deciding whether the changes should be split.
3. Use `$p-git-commit` to generate commit messages and to handle commit-message rules.
4. After committing, run `git push` to push changes to the remote repository.

## Skill Repository Tracking

When a new skill repository is installed, record its repository address in the `repos` array in `scripts/reinstall-skills.sh`. If the repository is already listed, do not add it again.
