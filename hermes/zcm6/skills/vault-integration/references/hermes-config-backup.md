# Hermes Agent Config Backup Pattern

Back up the current host's Hermes Agent configuration (`~/.hermes/`) into the vault's `00-inbox/memories-<hostname>/hermes/` directory. This is distinct from collecting *other* AI agents' memories (Codex / Claude Code) — here the agent backs up its own config.

## When to use

- "把当前服务器中 hermes 需要备份的内容也备份到这个仓库里"
- "参考本地 PC 的备份目录 memories/hermes 同步 hermes 配置"
- Any task that snapshots `~/.hermes/` into the vault for cross-machine alignment or disaster recovery.

## Source layout (`~/.hermes/`)

```
~/.hermes/
├── memories/         MEMORY.md, USER.md (+ *.lock, *.bak — skip)
├── config.yaml       main config (key_env refs, no plaintext secrets)
├── SOUL.md           system prompt override
├── skills/           mix of real dirs + symlinks → ../../.agents/skills/
├── cron/             jobs.json (may be empty)
├── .env              SECRETS — never copy
├── auth.json         SECRETS — never copy
├── state.db          binary — never copy
├── sessions/         transient — never copy
├── cache/ logs/      transient — never copy
└── ...
```

## Backup scope

| Category | Copy | Skip |
|----------|------|------|
| memories | `MEMORY.md`, `USER.md` | `*.lock`, `*.bak` |
| config | `config.yaml`, `SOUL.md` | `.env`, `auth.json`, `*.bak`, `config.yaml.bak.*` |
| skills | Real (non-symlink) dirs containing `SKILL.md` or `DESCRIPTION.md` | symlink skills, `.bundled_manifest`, `.lock`, `.curator_state`, `.usage.json`, `.hub/` |
| cron | `jobs.json` (if exists) | `executions.db`, `output/`, `*.lock` |
| scripts | `sync_hermes_config.sh` (cross-platform, copy from PC ref if available) | — |

## Skill filtering (critical step)

The `~/.hermes/skills/` directory contains both real self-built skill directories AND symlinks to bundled/hub-installed skills. Only the real directories should be backed up.

Detection command:
```bash
cd ~/.hermes/skills
for d in */; do
  d="${d%/}"
  [[ "$d" == .* ]] && continue
  [[ -L "$d" ]] && continue
  if [[ -f "$d/SKILL.md" ]] || [[ -f "$d/DESCRIPTION.md" ]] || \
     find "$d" \( -name "SKILL.md" -o -name "DESCRIPTION.md" \) | grep -q .; then
    echo "$d"
  fi
done
```

Symlinks typically point to `../../.agents/skills/<name>` — these are bundled/hub skills that ship with Hermes and are reinstalled automatically. Skip them all.

## Security pre-check

Before copying `config.yaml`, verify it has no plaintext secrets:
```bash
grep -nE '(api_key|apikey|secret|token|password)\s*[:=]' config.yaml
grep -n 'key_env' config.yaml
```
Hermes config uses `key_env: VAR_NAME` references and `${VAR_NAME}` interpolation — no plaintext. If the grep returns actual secret values (not variable references), do NOT copy the file.

## Output structure

```
00-inbox/memories-<hostname>/hermes/
├── memories/          MEMORY.md + USER.md
├── config/            config.yaml + SOUL.md
├── skills/            14+ self-built skill dirs (recursive)
├── scripts/            sync_hermes_config.sh
├── cron/              jobs.json or .gitkeep (empty placeholder)
├── .last_pull         timestamp "YYYY-MM-DD HH:MM:SS +ZZZZ"
└── README.md          source_host, skill list, cross-host diff table
```

## README.md essentials

- frontmatter: `source_repo: <hostname>`, `source_host: <hostname> (Linux x86_64)`, tags include `hermes, config-snapshot, sync, <hostname>, inbox`
- Self-built skill count and directory list
- Cross-host diff table (cron status, skill count, config paths, unique/missing skills vs reference host)
- Safety notes (what was excluded and why)

## sync_hermes_config.sh

The PC version at `memories/hermes/scripts/sync_hermes_config.sh` is cross-platform (auto-detects `~/.hermes` on Linux, `~/AppData/Local/hermes` on Windows). Copy it verbatim to the target. It provides `pull` (local → vault), `push` (vault → local, needs `yes` confirmation), and `status` (diff) subcommands.

## Delegation pattern

This task is a good delegation candidate — it involves many file operations that would flood the orchestrator's context. Dispatch:
1. **Work subagent**: inventory source, filter skills, copy files, write README + .last_pull, output summary.
2. **Review subagent**: diff each file pair (source vs backup), verify no sensitive files leaked, check README quality, confirm sync script integrity, validate directory structure. Output PASS/FAIL/WARN report.
3. If review finds FAIL items, re-dispatch work subagent with fix instructions.
