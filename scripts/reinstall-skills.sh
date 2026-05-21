#!/usr/bin/env bash
set -euo pipefail

AGENT="${AGENT:-codex}"
GLOBAL_FLAG="${GLOBAL_FLAG:--g}"

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
  npx --yes skills add "$repo" "$GLOBAL_FLAG" --agent "$AGENT" --skill '*' --yes
done

npx --yes skills list "$GLOBAL_FLAG" -a "$AGENT"

# Update, Needs node > 18 
# npx --yes skills update -g -y

# Remove
# npx --yes skills remove --all -g
