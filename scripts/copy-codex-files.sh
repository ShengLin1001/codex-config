#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"
repo_codex_dir="$repo_root/codex"

mkdir -p "$repo_codex_dir"

cp -p "$codex_home/AGENTS.md" "$repo_codex_dir/AGENTS.md"
cp -p "$codex_home/config.toml" "$repo_codex_dir/config.toml"

echo "Copied Codex files from $codex_home into $repo_codex_dir"
