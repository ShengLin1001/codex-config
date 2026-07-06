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
SKILLS_DIR="${SKILLS_DIR:-$HOME/.agents/skills}"

# Avoid GitHub's 60 req/hr anonymous API rate limit (causes "Failed to update"):
# reuse the gh login token when GITHUB_TOKEN isn't already set.
if [ -z "${GITHUB_TOKEN:-}" ] && command -v gh >/dev/null 2>&1; then
  GITHUB_TOKEN="$(gh auth token 2>/dev/null || true)"
  export GITHUB_TOKEN
fi

if ! command -v npx >/dev/null 2>&1; then
  if command -v module >/dev/null 2>&1; then
    module avail node 2>&1 || true
  fi
  echo "npx was not found. Load or install Node.js/npm first, then rerun." >&2
  exit 127
fi

repos=(
  "vercel-labs/agent-skills"
  "vercel-labs/skills"
  "https://github.com/ShengLin1001/codex-config.git"
  "https://github.com/Imbad0202/academic-research-skills-codex.git"
  "https://github.com/Yuan1z0825/nature-skills.git"
  "https://github.com/eze-is/web-access.git"
)

if [ -d "$SKILLS_DIR" ]; then
  mapfile -t INSTALLED_SKILLS < <(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
  if [ "${#INSTALLED_SKILLS[@]}" -gt 0 ]; then
    npx --yes skills remove "${INSTALLED_SKILLS[@]}" "$GLOBAL_FLAG" --yes
  fi
fi

for repo in "${repos[@]}"; do
  # Install once per repo; the CLI links the same global skill set to both agents.
  npx --yes skills add "$repo" "$GLOBAL_FLAG" --agent "${AGENT_LIST[@]}" --skill '*' --yes
done

for agent in "${AGENT_LIST[@]}"; do
  npx --yes skills list "$GLOBAL_FLAG" --agent "$agent"
done

# Update existing skills to their latest versions (needs node > 18):
# npx --yes skills update -g -y

# Avoid `skills remove --all -g`: it also scans agent-specific global dirs.
