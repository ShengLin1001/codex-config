#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"

mkdir -p "$codex_home"
mkdir -p "$codex_home/skills/p-skill-installer/agents"
mkdir -p "$codex_home/memories/rollout_summaries"

cp -p "$repo_root/codex/config.toml" "$codex_home/config.toml"
cp -p "$repo_root/codex/AGENTS.md" "$codex_home/AGENTS.md"
cp -p "$repo_root/skills/p-skill-installer/SKILL.md" "$codex_home/skills/p-skill-installer/SKILL.md"
cp -p "$repo_root/skills/p-skill-installer/agents/openai.yaml" "$codex_home/skills/p-skill-installer/agents/openai.yaml"
cp -p "$repo_root/memories/MEMORY.md" "$codex_home/memories/MEMORY.md"
cp -p "$repo_root/memories/memory_summary.md" "$codex_home/memories/memory_summary.md"

for file in "$repo_root"/memories/rollout_summaries/*.md; do
  [ -e "$file" ] || continue
  cp -p "$file" "$codex_home/memories/rollout_summaries/$(basename "$file")"
done

echo "Restored Codex files into $codex_home"
