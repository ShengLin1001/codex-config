#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"

mkdir -p "$codex_home"
mkdir -p "$codex_home/skills/p-skill-installer/agents"

cp -p "$repo_root/codex/config.toml" "$codex_home/config.toml"
cp -p "$repo_root/codex/AGENTS.md" "$codex_home/AGENTS.md"
cp -p "$repo_root/skills/p-skill-installer/SKILL.md" "$codex_home/skills/p-skill-installer/SKILL.md"
cp -p "$repo_root/skills/p-skill-installer/agents/openai.yaml" "$codex_home/skills/p-skill-installer/agents/openai.yaml"

echo "Restored Codex files into $codex_home"
