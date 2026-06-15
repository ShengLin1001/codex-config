#!/usr/bin/env bash
set -euo pipefail

# Agents to install skills into (space-separated).
# Defaults to both Codex and Claude Code. Override examples:
#   AGENTS="claude-code" bash scripts/reinstall-skills.sh   # only Claude Code
#   AGENTS="codex"       bash scripts/reinstall-skills.sh   # only Codex
#   AGENTS="*"           bash scripts/reinstall-skills.sh   # all detected agents
# Backward compat: the old single-agent AGENT variable is still honored.
AGENTS="${AGENTS:-${AGENT:-codex claude-code}}"
GLOBAL_FLAG="${GLOBAL_FLAG:--g}"
read -r -a AGENT_LIST <<< "$AGENTS"

if ! command -v npx >/dev/null 2>&1; then
  if command -v module >/dev/null 2>&1; then
    module avail node 2>&1 || true
  fi
  echo "npx was not found. Load or install Node.js/npm first, then rerun." >&2
  exit 127
fi

repos=(
  "vercel-labs/agent-skills"
  "https://github.com/ShengLin1001/codex-config.git"
  "https://github.com/Imbad0202/academic-research-skills-codex.git"
  "https://github.com/Yuan1z0825/nature-skills.git"
)

for repo in "${repos[@]}"; do
  for agent in "${AGENT_LIST[@]}"; do
    npx --yes skills add "$repo" "$GLOBAL_FLAG" --agent "$agent" --skill '*' --yes
  done
done

npx --yes skills list "$GLOBAL_FLAG"

# Update existing skills to their latest versions (needs node > 18):
# npx --yes skills update -g -y

# Remove all global skills:
# npx --yes skills remove --all -g
