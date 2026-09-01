# Synthesize Device-Specific MEMORY.<device>.md Files

After two device memory snapshots are merged into `memories_core/` (see
`multi-device-memories-merge.md`), the orchestrator often asks a subagent to
**write two new synthetic files** — `MEMORY.zcm6.md` and `MEMORY.pc.md` — that
distill device-specific knowledge (hardcoded paths, venv paths, software
versions, network config) from across many source files into one per-device
reference. This is distinct from the mechanical merge: the sources already
exist in `memories-<device>/`; the output is newly authored synthesis.

## When to use

- "编写 MEMORY.zcm6.md 和 MEMORY.pc.md 两个设备特定记忆文件"
- "整合 zcm6 和 PC 两台设备的硬编码路径、venv 路径、软件版本、网络配置"
- Any task that asks for a per-device synthesized memory file in
  `memories_core/` covering paths/config/versions that don't belong in the
  cross-device MEMORY.md / USER.md / AGENTS.md / SOUL.md.

## Inputs

| Role | Example |
|------|---------|
| zcm6 source | `00-inbox/memories-zcm6/` (codex/, claude-code/, hermes/) |
| PC source   | `00-inbox/memories/` (codex/, claude-code/, hermes/) |
| Output     | `00-inbox/memories_core/MEMORY.zcm6.md`, `MEMORY.pc.md` |

## Required section template (both files symmetric)

Each file should carry these sections, in Chinese, in this order:

1. 设备基本信息（OS、内核/glibc、角色、主要用途、home 路径）
2. Python 环境（codex venv 路径、scansci-pdf venv 路径、其他 venvs）
3. Git 环境（PATH/LD_LIBRARY_PATH 或 Git Bash 路径、信任项目清单）
4. Hermes 配置要点（model provider 格式、reasoning_effort、特殊设置）
5. Claude Code / Codex 全局约束中的设备特定部分
6. 项目记忆摘要（claude-code/project-memories/ 下的关键知识点，按项目分类）
7. Codex memory_summary 中的设备特定知识点
8. 网络与代理配置（如有）
9. 其他设备特定软件版本
10. Hermes hermes/memories/MEMORY.md 摘要
11. 采集信息（源目录、采集时间、原始路径）

Symmetry matters: the two files should have parallel section numbering so a
reader can diff them side-by-side.

## Source files to read per device

For each device's `memories-<device>/` directory, read these files (skip any
that don't exist):

| Source file | What to extract |
|-------------|-----------------|
| `codex/memories/memory_summary.md` | User profile, preferences, general tips, per-cwd memory points |
| `codex/memories/MEMORY.md` (may be >100KB, truncated to 50KB) | Task-group reusable knowledge, failures, preferences |
| `codex/memories/raw_memories.md` (may be >100KB) | Per-thread raw detail; scan head only |
| `codex/global/AGENTS.md` | Git env, Python env, platform constraints |
| `codex/global/config.toml` | model, reasoning_effort, sandbox, features, plugins, projects trust list, MCP servers |
| `claude-code/global/CLAUDE.md` | Python env, file encoding, deletion safety, platform env |
| `claude-code/global/settings.json` | model, permissions, plugins, env.PATH, PYTHONUTF8 |
| `hermes/config/config.yaml` | model provider format, reasoning_effort, terminal, memory, compression |
| `hermes/memories/MEMORY.md` | Host-specific work conventions, skill overlap notes |
| `claude-code/project-memories/*/MEMORY.md` | Per-project knowledge index (one line per linked file) |
| `codex/rollout-summaries/*.md` (selected, not all) | Network/proxy/install details — grep for "proxy", "ssh", "install", "xray", "v2rayN" |

## Security

- **Never read**: `.env`, `auth.json`, `credentials.json`, `.openclaw/agents/`,
  `state.db`, `sessions/`, `cache/`, `logs/`.
- For `config.toml` / `settings.json` / `config.yaml`: the source snapshots
  should already have secrets redacted (collection step did this). If you see a
  plaintext key/token/password, replace with `[REDACTED]` in your output and
  note it.
- `openclaw models status --json` once emitted a full Claude credential in tool
  output — treat any such emission as compromised; never repeat it.

## Key differences to capture (zcm6 vs PC)

These differences recurred in the 2026-08-06 synthesis and are likely to recur:

| Dimension | zcm6 | PC |
|-----------|------|-----|
| OS | CentOS 7.9, glibc 2.17 | Windows 10 |
| Path prefix | `/public3/home/scg6928/` | `C:/Users/louis/` or `F:/BaiduSyncdisk/` |
| codex venv python | `.../env/pyenv/codex/bin/python` | `.../env/pyenv/codex/Scripts/python` |
| Hermes provider format | `provider: custom` + `custom_providers:` list (old) | `provider: custom:paratera` + `providers:` dict (new) |
| Hermes reasoning_effort | `medium` | `max` |
| Claude model | `opus` | `sonnet` |
| Codex MCP servers | all disabled (commented) | scansci-pdf enabled, node_repl, openaiDeveloperDocs |
| Codex personality | (commented out) | `pragmatic` |
| Codex features | network_proxy=true, apps=false | remote_connections=true, js_repl=false |
| Claude enabledPlugins | `{}` (none) | claude-hud, ponytail |
| Git env | `PATH=.../tools/git/2.43.7/bin:$PATH` + `LD_LIBRARY_PATH=/public3/soft/curl/lib` | Git Bash at `D:\Program Files\Git\usr\bin\bash.exe` |
| Proxy | SSH RemoteForward 37897 ← Windows 7897 | v2rayN/Clash on 127.0.0.1:7897 |
| OpenClaw | installed, no Gateway | WSL2 Ubuntu-24.04 Gateway on 18789 |
| WSL | n/a | Ubuntu-24.04 at `D:\software\wsl\` |

## Writing method

1. **Read all source files first** (batch parallel `terminal cat` calls per
   device). Do not write incrementally — you need the full picture to keep
   sections symmetric.
2. **Preserve all hardcoded paths verbatim** — do not relativize, do not
   abbreviate. `C:\Users\louis\mysoft\env\pyenv\codex\Scripts\python.exe` stays
   as-is.
3. **Use Chinese for prose**, keep technical terms (PATH, LD_LIBRARY_PATH,
   reasoning_effort, venv, etc.) in English.
4. **UTF-8 encoding** — `write_file` handles this; verify with
   `file <path>` returning "UTF-8 Unicode text".
5. **Symmetric section numbering** — both files should have the same H2
   section list, so a side-by-side diff is meaningful.
6. **Diff table** — include a "zcm6 vs PC differences" table in whichever file
   is written second (or in both, under section 4 Hermes config), so the
   reader can see the key contrasts without opening both files.
7. **Port/path tables** — for network config, a table mapping port → meaning is
   far more readable than prose.

## Verification

After writing both files:

```bash
# 1. Both files exist and are UTF-8
ls -la memories_core/MEMORY.*.md
file memories_core/MEMORY.zcm6.md memories_core/MEMORY.pc.md
# expect: UTF-8 Unicode text

# 2. Section structure is symmetric
grep -E "^## " memories_core/MEMORY.zcm6.md
grep -E "^## " memories_core/MEMORY.pc.md
# expect: same section count and titles

# 3. Path prefixes are correct
grep -c "/public3/home/scg6928/" memories_core/MEMORY.zcm6.md  # zcm6 paths
grep -c "C:/Users/louis/\|F:/BaiduSyncdisk/" memories_core/MEMORY.pc.md  # PC paths
# expect: zcm6 file has many zcm6 paths, PC file has many PC paths
```

## Pitfalls

- **`read_file` rejects BOM .md files**: zcm6's INDEX.md and some files may be
  detected as binary. Use `terminal cat` instead of `read_file` for those.
- **codex MEMORY.md is huge (292KB+)**: it will be truncated to 50KB on read.
  The head usually has the most recent task groups — that's enough for
  device-specific synthesis. Do not try to page through the whole file.
- **raw_memories.md is huge (490KB+)**: same — head only. Don't page.
- **rollout-summaries are numerous (100+ per device)**: do NOT read all. Grep
  the directory listing for keywords (`proxy`, `ssh`, `install`, `xray`,
  `v2rayN`, `openclaw`, `wsl`) and read only the 5-10 most relevant.
- **Symmetric sections don't mean symmetric content**: zcm6 has no WSL section;
  PC has no module/gcc section. Keep the section heading but write "n/a" or
  omit the subsection.
- **Don't invent paths**: if a source file doesn't mention a venv path, don't
  guess it from the pattern. Only write paths that appear in the source files.
- **Secrets in config.toml**: the collection step should have redacted them,
  but verify before copying any config snippet into the output. Replace
  `${VAR}` references verbatim (they're safe), but never copy a literal key
  value.
