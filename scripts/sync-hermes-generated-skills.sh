#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  sync-hermes-generated-skills.sh export [--force] <relative-skill-path> [...]
  sync-hermes-generated-skills.sh list

Archive deliberately selected Hermes-created skills in this repository. A
relative skill path is the path below Hermes's skills root, for example
"my-skill" or "research/my-skill".

Commands:
  export  Copy selected local Hermes skills into skills/hermes-generated/.
  list    Show repository-managed and local skills.

The script refuses to replace an existing destination unless --force is given.
It never copies Hermes bundled skills or arbitrary npm-managed skills unless you
name that skill path explicitly.
EOF
}

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_skills_root="$repo_root/skills/hermes-generated"

if command -v hermes >/dev/null 2>&1; then
  hermes_config_path="$(hermes config path)"
  case "$hermes_config_path" in
    [A-Za-z]:\\*) hermes_config_path="$(cygpath -u "$hermes_config_path")" ;;
  esac
  hermes_home="$(dirname "$hermes_config_path")"
elif [ -n "${HERMES_HOME:-}" ]; then
  hermes_home="$HERMES_HOME"
else
  hermes_home="$HOME/.hermes"
fi
hermes_skills_root="$hermes_home/skills"

force=false
command_name="${1:-}"
if [ -z "$command_name" ]; then
  usage >&2
  exit 2
fi
shift

arguments=()
for argument in "$@"; do
  if [ "$argument" = "--force" ]; then
    force=true
  else
    arguments+=("$argument")
  fi
done
set -- "${arguments[@]}"

validate_skill_path() {
  local path="$1"
  case "/$path/" in
    //|*"/../"*|*"//"*)
      echo "Skill path must be a non-empty relative path without '..': $path" >&2
      exit 2
      ;;
  esac
}

copy_skill() {
  local source_root="$1"
  local destination_root="$2"
  local relative_path="$3"
  local source="$source_root/$relative_path"
  local destination="$destination_root/$relative_path"
  local archive

  validate_skill_path "$relative_path"
  if [ ! -f "$source/SKILL.md" ]; then
    echo "Not a Hermes skill (SKILL.md missing): $source" >&2
    exit 1
  fi
  if [ -e "$destination" ]; then
    if [ "$force" != true ]; then
      echo "Destination exists (use --force to replace it): $destination" >&2
      exit 1
    fi
    archive="$destination_root/.archive/sync-$(date +%Y%m%d-%H%M%S)/$relative_path"
    mkdir -p "$(dirname "$archive")"
    mv "$destination" "$archive"
    echo "Archived previous copy at $archive"
  fi
  mkdir -p "$destination"
  cp -a "$source/." "$destination/"
  echo "Synced $relative_path"
}

case "$command_name" in
  export)
    if [ "$#" -eq 0 ]; then
      usage >&2
      exit 2
    fi
    for relative_path in "$@"; do
      copy_skill "$hermes_skills_root" "$repo_skills_root" "$relative_path"
    done
    ;;
  list)
    echo "Repository-managed Hermes skills:"
    first_skill=""
    if [ -d "$repo_skills_root" ]; then
      first_skill="$(find "$repo_skills_root" -type f -name SKILL.md -print -quit)"
    fi
    if [ -n "$first_skill" ]; then
      find "$repo_skills_root" -type f -name SKILL.md -print | \
        while IFS= read -r skill_file; do
          relative_path="${skill_file#$repo_skills_root/}"
          printf '  %s\n' "${relative_path%/SKILL.md}"
        done
    else
      echo "  (none)"
    fi
    echo "Hermes local skills root: $hermes_skills_root"
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    echo "Unknown command: $command_name" >&2
    usage >&2
    exit 2
    ;;
esac
