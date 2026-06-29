#!/usr/bin/env bash
set -euo pipefail

# Codex plugin marketplaces to register.
# Format: marketplace_name|codex_source|git_url
marketplaces=(
  "ponytail|DietrichGebert/ponytail|https://github.com/DietrichGebert/ponytail.git"
)

# Codex plugins to install from configured marketplaces.
plugins=(
  "ponytail@ponytail"
)

require_cmd() {
  local cmd="$1"

  if command -v "$cmd" >/dev/null 2>&1; then
    return 0
  fi

  if command -v module >/dev/null 2>&1; then
    module avail "$cmd" 2>&1 || true
  fi

  echo "$cmd was not found. Load or install it first, then rerun." >&2
  exit 127
}

marketplace_registered() {
  local name="$1"
  codex plugin marketplace list | awk 'NR > 1 {print $1}' | grep -Fxq "$name"
}

marketplace_root() {
  local name="$1"
  codex plugin marketplace list | awk -v name="$name" 'NR > 1 && $1 == name {print $2; exit}'
}

plugin_installed() {
  local plugin="$1"
  codex plugin list | awk -v plugin="$plugin" '$1 == plugin && $2 == "installed," {found=1} END {exit !found}'
}

add_local_marketplace_fallback() {
  local name="$1"
  local git_url="$2"

  require_cmd git

  local codex_home="${CODEX_HOME:-$HOME/.codex}"
  local fallback_root="${CODEX_MARKETPLACE_HOME:-$codex_home/marketplaces}"
  local fallback_dir="$fallback_root/$name"

  mkdir -p "$fallback_root"

  if [ -d "$fallback_dir/.git" ]; then
    git -C "$fallback_dir" pull --ff-only
  elif [ -e "$fallback_dir" ]; then
    echo "$fallback_dir exists but is not a Git checkout; move it aside or set CODEX_MARKETPLACE_HOME." >&2
    exit 1
  else
    git clone --depth 1 "$git_url" "$fallback_dir"
  fi

  codex plugin marketplace add "$fallback_dir"
}

register_marketplace() {
  local name="$1"
  local source="$2"
  local git_url="$3"

  if marketplace_registered "$name"; then
    local root
    root="$(marketplace_root "$name")"
    if [[ "$root" == *"/.staging/"* || "$root" == *"\\.staging\\"* ]]; then
      echo "Marketplace $name uses staging checkout $root; re-registering with a stable local clone." >&2
      codex plugin marketplace remove "$name"
      add_local_marketplace_fallback "$name" "$git_url"
      return 0
    fi

    echo "Marketplace $name is already configured."
    return 0
  fi

  if codex plugin marketplace add "$source"; then
    return 0
  fi

  echo "Git marketplace add failed for $source; falling back to a stable local clone." >&2
  add_local_marketplace_fallback "$name" "$git_url"
}

require_cmd codex

for entry in "${marketplaces[@]}"; do
  IFS='|' read -r name source git_url <<< "$entry"
  register_marketplace "$name" "$source" "$git_url"
done

for plugin in "${plugins[@]}"; do
  if plugin_installed "$plugin"; then
    echo "Plugin $plugin is already installed."
  else
    codex plugin add "$plugin"
  fi
done

codex plugin marketplace list
codex plugin list
