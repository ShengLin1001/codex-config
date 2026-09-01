#!/usr/bin/env bash
# =============================================================================
# sync-hermes-device.sh — 本机 ~/.hermes/ ↔ codex-config/hermes/<device>/ 双向同步
#
# 设计理念：
#   每个设备的 hermes 配置直接作为 codex-config/hermes/<device>/ 下的文件管理，
#   而非复制快照。pull 把本机配置同步到仓库目录，push 把仓库目录写回本机。
#
# 同步范围：
#   config.yaml, SOUL.md      — 配置文件（key_env 引用，无明文密钥）
#   memories/                  — MEMORY.md, USER.md（跨会话记忆）
#   cron/                      — jobs.json（定时任务定义）
#   skills/                    — 分类处理（见下）
#
# Skills 分类策略：
#   1. 自建 skill（真实目录，非 symlink）          → 直接同步整个目录
#   2. bundled skill 被修改的（如 ocr-and-documents）→ 直接同步整个目录
#   3. git 安装的 skill（symlink → ~/.agents/）    → 只记录到 .skill-lock.json 索引
#
# 排除内容（不同步）：
#   .env, auth.json, *.bak, *.lock, *.db, state.db*, sessions/, cache/,
#   logs/, audio_cache/, image_cache/, models_dev_cache.json, *.db-shm, *.db-wal
#
# 用法：
#   bash sync-hermes-device.sh pull <device>     # 本机 → 仓库（默认安全方向）
#   bash sync-hermes-device.sh push <device>     # 仓库 → 本机（需确认）
#   bash sync-hermes-device.sh pull <device> --dry  # 预览
#   bash sync-hermes-device.sh status <device>   # 比较差异
#   bash sync-hermes-device.sh list-devices      # 列出已管理的设备
# =============================================================================

set -euo pipefail

# ── 路径解析 ─────────────────────────────────────────────────────────────────
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_BASE="$REPO_ROOT/hermes"

if [[ -n "${HERMES_HOME:-}" ]]; then
    HERMES_SRC="$HERMES_HOME"
elif [[ -d "$HOME/.hermes" ]]; then
    HERMES_SRC="$HOME/.hermes"
elif [[ -d "$HOME/AppData/Local/hermes" ]]; then
    HERMES_SRC="$HOME/AppData/Local/hermes"
else
    echo "ERROR: 找不到 Hermes 配置目录（~/.hermes 或 ~/AppData/Local/hermes）" >&2
    exit 1
fi

# ── 辅助函数 ─────────────────────────────────────────────────────────────────
log()  { echo "  $*"; }
warn() { echo "  ⚠ $*" >&2; }
die()  { echo "  ✖ $*" >&2; exit 1; }

# safe_copy <src> <dst> <dry>
safe_copy() {
    local src="$1" dst="$2" dry="${3:-false}"
    [[ -f "$src" ]] || { warn "源文件不存在: $src"; return 0; }
    if [[ "$dry" == "true" ]]; then
        log "[dry] $src → $dst"
    else
        mkdir -p "$(dirname "$dst")"
        cp "$src" "$dst"
        log "✓ $(basename "$src")"
    fi
}

# sync_tree <src_dir> <dst_dir> <dry> — 递归复制目录（跳过 symlink 和 .lock）
sync_tree() {
    local src="$1" dst="$2" dry="${3:-false}"
    [[ -d "$src" ]] || { warn "源目录不存在: $src"; return 0; }
    if [[ "$dry" == "true" ]]; then
        local count
        count=$(find "$src" -type f ! -name "*.lock" 2>/dev/null | wc -l)
        log "[dry] $src → $dst ($count files)"
        return 0
    fi
    mkdir -p "$dst"
    local count=0
    while IFS= read -r -d '' f; do
        local rel="${f#$src/}"
        mkdir -p "$dst/$(dirname "$rel")"
        cp "$f" "$dst/$rel"
        ((count++)) || true
    done < <(find "$src" -type f ! -name "*.lock" -print0)
    log "✓ $(basename "$src")/ ($count files)"
}

# sync_skill_tree — 同步单个 skill 目录（包括嵌套的，如 productivity/ocr-and-documents）
# 用法: sync_skill_tree <skills_src> <skills_dst> <dry>
sync_skills() {
    local src="$1" dst="$2" dry="${3:-false}"
    [[ -d "$src" ]] || { warn "skills 目录不存在: $src"; return 0; }

    local symlink_skills=()
    local real_skills=0
    local modified_bundled=0

    # 检测被修改的 bundled skill（通过 hermes skills list-modified）
    # 输出格式: "  ~ ocr-and-documents"（波浪号前缀标记 modified）
    local modified_list=()
    if command -v hermes >/dev/null 2>&1; then
        while IFS= read -r line; do
            # 只提取以 ~ 开头的行中的 skill 名
            if [[ "$line" == *~* ]]; then
                local name
                name=$(echo "$line" | sed 's/.*~[[:space:]]*//' | awk '{print $1}')
                [[ -n "$name" ]] && modified_list+=("$name")
            fi
        done < <(hermes skills list-modified 2>/dev/null || true)
    fi

    echo "[skills] 分类处理"
    cd "$src"
    for d in */; do
        d="${d%/}"
        [[ "$d" == .* ]] && continue
        local full="$src/$d"
        if [[ -L "$d" ]]; then
            # symlink → git 安装的 skill，只记录索引
            local target
            target=$(readlink "$d")
            symlink_skills+=("$d:$target")
            if [[ "$dry" == "true" ]]; then
                log "[dry] [symlink-index] $d → $target"
            fi
        elif [[ -d "$d" ]]; then
            # 真实目录 — 检查是否含 SKILL.md 或 DESCRIPTION.md（直接或嵌套）
            if find "$d" -name "SKILL.md" -o -name "DESCRIPTION.md" | grep -q .; then
                sync_tree "$full" "$dst/$d" "$dry"
                ((real_skills++)) || true
            else
                warn "跳过无 SKILL.md/DESCRIPTION.md 的目录: $d"
            fi
        fi
    done
    cd - >/dev/null

    # 写入 .skill-lock.json 索引（git 安装的 skill 来源记录）
    if [[ "$dry" != "true" ]]; then
        local lock_file="$dst/.skill-lock.json"
        # 也从 ~/.agents/.skill-lock.json 复制完整索引（如果存在）
        if [[ -f "$HOME/.agents/.skill-lock.json" ]]; then
            cp "$HOME/.agents/.skill-lock.json" "$lock_file"
            log "✓ .skill-lock.json (来自 ~/.agents/)"
        else
            # 手动生成索引
            printf '{\n  "skills": {\n' > "$lock_file"
            local first=true
            for entry in "${symlink_skills[@]}"; do
                local name="${entry%%:*}"
                local target="${entry#*:}"
                if [[ "$first" == "true" ]]; then
                    first=false
                else
                    printf ',\n' >> "$lock_file"
                fi
                printf '    "%s": {"target": "%s"}' "$name" "$target" >> "$lock_file"
            done
            printf '\n  }\n}\n' >> "$lock_file"
            log "✓ .skill-lock.json (${#symlink_skills[@]} symlink skills)"
        fi
    else
        log "[dry] .skill-lock.json (${#symlink_skills[@]} symlink skills indexed)"
    fi

    log "  自建/modified skill: $real_skills, git 安装(symlink): ${#symlink_skills[@]}"
    if [[ ${#modified_list[@]} -gt 0 ]]; then
        log "  bundled modified: ${modified_list[*]}"
    fi
}

# ── pull: 本机 → 仓库 ────────────────────────────────────────────────────────
do_pull() {
    local device="$1" dry="${2:-false}"
    local dst="$HERMES_BASE/$device"
    [[ -n "$device" ]] || die "缺少设备名。用法: $0 pull <device>"

    echo "=== PULL: 本机 Hermes ($HERMES_SRC) → 仓库 ($dst) ==="
    echo "设备: $device"
    echo ""

    echo "[config] config.yaml + SOUL.md"
    safe_copy "$HERMES_SRC/config.yaml" "$dst/config.yaml" "$dry"
    safe_copy "$HERMES_SRC/SOUL.md" "$dst/SOUL.md" "$dry"
    echo ""

    echo "[memories] MEMORY.md + USER.md"
    safe_copy "$HERMES_SRC/memories/MEMORY.md" "$dst/memories/MEMORY.md" "$dry"
    safe_copy "$HERMES_SRC/memories/USER.md" "$dst/memories/USER.md" "$dry"
    echo ""

    echo "[cron] jobs.json"
    safe_copy "$HERMES_SRC/cron/jobs.json" "$dst/cron/jobs.json" "$dry"
    echo ""

    do_sync_skills "$dst/skills" "$dry"

    if [[ "$dry" != "true" ]]; then
        date "+%Y-%m-%d %H:%M:%S %z" > "$dst/.last_pull"
        echo ""
        echo "=== 完成。快照时间: $(cat "$dst/.last_pull") ==="
    fi
}

# ── push: 仓库 → 本机 ────────────────────────────────────────────────────────
do_push() {
    local device="$1" dry="${2:-false}"
    local src="$HERMES_BASE/$device"
    [[ -n "$device" ]] || die "缺少设备名。用法: $0 push <device>"
    [[ -d "$src" ]] || die "设备目录不存在: $src"

    echo "=== PUSH: 仓库 ($src) → 本机 Hermes ($HERMES_SRC) ==="
    echo "⚠  此操作将覆盖本机配置。建议先备份: cp -r \"$HERMES_SRC\" \"${HERMES_SRC}.bak.$(date +%Y%m%d)\""
    echo ""

    if [[ "$dry" != "true" ]]; then
        echo "确认继续？输入 yes 继续，其他取消:"
        read -r confirm
        [[ "$confirm" == "yes" ]] || die "已取消。"
    fi

    echo "[config]"
    safe_copy "$src/config.yaml" "$HERMES_SRC/config.yaml" "$dry"
    safe_copy "$src/SOUL.md" "$HERMES_SRC/SOUL.md" "$dry"
    echo "[memories]"
    safe_copy "$src/memories/MEMORY.md" "$HERMES_SRC/memories/MEMORY.md" "$dry"
    safe_copy "$src/memories/USER.md" "$HERMES_SRC/memories/USER.md" "$dry"
    echo "[cron]"
    safe_copy "$src/cron/jobs.json" "$HERMES_SRC/cron/jobs.json" "$dry"
    echo "[skills]"
    echo "  ⚠ push 不自动覆盖 skills 目录（结构复杂，请手动处理）"
    echo "  git 安装的 skill 请用 scripts/reinstall-skills.sh 恢复"
    echo "  自建 skill 可手动 cp -r $src/skills/* ~/.hermes/skills/"

    echo ""
    echo "=== push 完成 ==="
}

# 技能同步的共享入口
do_sync_skills() {
    local dst_skills="$1" dry="${2:-false}"
    echo "[skills]"
    sync_skills "$HERMES_SRC/skills" "$dst_skills" "$dry"
}

# ── status: 比较差异 ─────────────────────────────────────────────────────────
do_status() {
    local device="$1"
    local dst="$HERMES_BASE/$device"
    [[ -n "$device" ]] || die "缺少设备名。用法: $0 status <device>"

    echo "=== STATUS: 本机 ($HERMES_SRC) vs 仓库 ($dst) ==="
    echo ""
    echo "[config]"
    for f in config.yaml SOUL.md; do
        if [[ -f "$HERMES_SRC/$f" && -f "$dst/$f" ]]; then
            diff -q "$HERMES_SRC/$f" "$dst/$f" 2>&1 || true
        elif [[ -f "$HERMES_SRC/$f" ]]; then
            echo "  $f: 仅本机存在"
        elif [[ -f "$dst/$f" ]]; then
            echo "  $f: 仅仓库存在"
        fi
    done
    echo "[memories]"
    for f in MEMORY.md USER.md; do
        if [[ -f "$HERMES_SRC/memories/$f" && -f "$dst/memories/$f" ]]; then
            diff -q "$HERMES_SRC/memories/$f" "$dst/memories/$f" 2>&1 || true
        else
            echo "  $f: 一端缺失"
        fi
    done
    echo "[cron]"
    [[ -f "$HERMES_SRC/cron/jobs.json" ]] && [[ -f "$dst/cron/jobs.json" ]] \
        && diff -q "$HERMES_SRC/cron/jobs.json" "$dst/cron/jobs.json" 2>&1 || true
    echo "[skills] (diff -rq, 仅真实目录)"
    diff -rq "$HERMES_SRC/skills" "$dst/skills" 2>&1 | grep -v '\.skill-lock\.json' | head -30 || true
}

# ── list-devices ─────────────────────────────────────────────────────────────
do_list() {
    echo "已管理的设备目录:"
    if [[ ! -d "$HERMES_BASE" ]]; then
        echo "  (hermes/ 目录不存在)"
        return
    fi
    for d in "$HERMES_BASE"/*/; do
        [[ -d "$d" ]] || continue
        local name
        name=$(basename "$d")
        local last_pull="(无)"
        [[ -f "$d/.last_pull" ]] && last_pull=$(cat "$d/.last_pull")
        printf "  %-20s 最后同步: %s\n" "$name" "$last_pull"
    done
}

# ── 主入口 ───────────────────────────────────────────────────────────────────
main() {
    local cmd="${1:-}" device="${2:-}" dry="false"

    [[ -n "$cmd" ]] || { usage; exit 1; }

    case "$cmd" in
        pull|push|status)
            [[ -n "$device" ]] || die "缺少设备名。用法: $0 $cmd <device>"
            [[ "${3:-}" == "--dry" ]] && dry="true"
            ;;
        list-devices) ;;
        *) usage; exit 1 ;;
    esac

    case "$cmd" in
        pull)    do_pull "$device" "$dry" ;;
        push)    do_push "$device" "$dry" ;;
        status)  do_status "$device" ;;
        list-devices) do_list ;;
    esac
}

usage() {
    cat <<'EOF'
用法: sync-hermes-device.sh <command> <device> [options]

命令:
  pull <device> [--dry]     本机 → 仓库（默认安全方向）
  push <device> [--dry]     仓库 → 本机（需确认）
  status <device>           比较两端差异
  list-devices              列出已管理的设备目录

设备名: 自定义标识符（如 zcm6, pc, macbook 等）

示例:
  bash sync-hermes-device.sh pull zcm6
  bash sync-hermes-device.sh pull zcm6 --dry
  bash sync-hermes-device.sh status zcm6
EOF
}

main "$@"
