---
name: vault-integration
title: Obsidian Vault Knowledge Integration
description: "Use when importing source Markdown into vault 10/20 dirs, batch-integrating multiple source projects via delegated subagents, collecting AI agent memories/configs into 00-inbox, or mining knowledge from raw calculation directories with no ai-guide."
tags: [vault, obsidian, archive, integration, provenance]
category: vault
---

# Obsidian Vault Knowledge Integration

Use when integrating knowledge from an external source-repo directory into the vault's archival layer (`10-sources/`, `20-projects/<slug>/`). Covers the full pipeline: inventory → merge-vs-new decision → frontmatter + rename → internal-link rewrite → MANIFEST.csv → LOG.md. This is a recurring class of work because the vault is populated from multiple read-only source repos.

The vault lives at `~/mysoft/pei/myobsidian` (or the session WORKSPACE PATH). Its conventions are defined in `AGENTS.md` (write-permission model) and `SCHEMA.md` (frontmatter / naming / MANIFEST format). Read both before any integration — see `references/vault-conventions.md` for the condensed rules.

## When to use

- "把 X 目录下的知识整合到 vault 的 20-projects/Y/ 中"
- "导入源项目的 ai-guide / docs / notes 到 vault"
- "合并 / 去重 / 归类源仓库文件到 vault"
- "收集 codex/claude code 的记忆/配置到 00-inbox/memories-*"
- "把这个项目的对应关系写在仓库的文件里"（创建 PROJECT-MAP.md）
- Any task that moves Markdown knowledge from a source repo into `10-sources/` or `20-projects/` while preserving provenance.
- Batch integration of multiple source projects in one session (use delegated subagents — see multi-project pattern below).

## When NOT to use

- Creating new synthesis / overview pages → that belongs in `30-wiki/` (creation layer), not the archival layer. The archival layer is raw-material only.
- Editing a single existing vault file for content → no integration pipeline needed.
- Importing PDF / binary / raw calculation data → register in `90-archive/INDEX.md`, do not copy into vault.

## Workflow

### 1. Inventory both sides

- List source directory tree (`find <src> -type f`).
- List vault target directory (`ls` / `find`).
- Read `_import/MANIFEST.csv` head + tail to know the source_repo slug convention and existing rows (avoid duplicates).

### 2. Read vault conventions

- `AGENTS.md` — three-tier write model (§1), source-repo read-only rule (§3), no-batch-delete (§3).
- `SCHEMA.md` — frontmatter minimal fields (§1), naming rules (§2), MANIFEST.csv columns + disposition values (§6).
- See `references/vault-conventions.md` for the condensed checklist.

### 3. Read existing vault files (topic map)

Read every existing `.md` in the target `notes/` dir. Goal: know which topics are already covered so source files can be classified as MERGE (same topic exists) or NEW (no vault equivalent).

### 4. Read source files (assess topics)

Read the head (~25-40 lines) of every source `.md` to extract: title, date, topic, cross-references to sibling files. If a source file references sibling files by name, record those — they'll need link rewriting in step 6.

### 5. Check for extra file types mentioned in the task

If the task mentions "manuscript", "figures", "config", etc., grep the source project root (`README.md`, `AGENTS.md`, `CLAUDE.md`, and the named subdirectories). Report explicitly if none found — do not silently skip.

### 6. Decision matrix: merge vs new

For each source file:

| Condition | Disposition | Action |
|---|---|---|
| Vault has a file on the SAME topic (same subject, same parameter, same bug) | **MERGE** | Append as new H2 section in the existing vault file (see step 7b). |
| Vault has no equivalent | **NEW** | Create new file in `notes/<subdir>/` preserving source structure (see step 7a). |
| PDF / binary / raw data | **ARCHIVED** | Register in `90-archive/INDEX.md`, do not copy. |
| Build artifacts, cache, editor config | **SKIPPED** | One row in MANIFEST with reason. |

Default: when in doubt, create NEW. Merging risks losing the existing file's structure; only merge when the topic overlap is unambiguous.

### 7a. Create new files

For each NEW file:

1. **Rename to kebab-case**: `stage0_1_param_scan_analysis.md` → `stage0-1-param-scan-analysis.md`. No underscores, no uppercase, no Chinese in filename.
2. **Preserve subdirectory structure**: if source has `gsfe/`, `hoec/`, `training/` subdirs, create matching `notes/gsfe/`, `notes/hoec/`, `notes/training/`.
3. **Prepend frontmatter**:
   ```yaml
   ---
   title: <Chinese or descriptive title from content H1>
   date: <from content, or file mtime>
   tags: [<project-slug>, <topic>, ...]
   source_repo: other/<project-slug>
   imported: <YYYY-MM-DD>
   ---
   ```
4. **Rewrite internal links**: replace old sibling filenames with new kebab-case names. Handle both `oldname.md` and bare `oldname` (stem-only, wikilink-style) forms. Use regex with word boundaries to avoid partial matches. See `references/link-rewrite-recipe.md`.
5. **Body**: copy source content verbatim after frontmatter. Do NOT edit, summarize, or restructure — archival layer is raw material.

### 7b. Merge into existing file

1. Read the source file body.
2. **Demote headings by one level** (H1→H2, H2→H3, etc.) so the merged content nests cleanly under the existing doc.
3. **Insert a merge separator** before the appended block:
   ```html
   <!-- MERGED <date> from source: <source_path> -->
   <!-- Reason: <why merged here, what it adds> -->
   ```
4. **Append** the demoted body at the end of the existing vault file.
5. **Rewrite internal links** in the merged block same as step 7a.4.
6. Do NOT delete or reword any existing content. No information loss.

### 8. Update `_import/MANIFEST.csv`

Append one row per source file:

```
source_repo,source_path,disposition,target_path,reason
```

- `source_repo`: the slug from the task (e.g. `other/au-nn-potential`).
- `source_path`: path relative to source repo root (e.g. `ai-guide/hoec/fcc_hoec_energy.md`).
- `disposition`: `imported` (new file) / `merged` / `archived` / `skipped`.
- `target_path`: vault-relative path of the created/merged file.
- `reason`: one-line why; mandatory for `merged` and `skipped`.

**Append-safe method**: read existing MANIFEST, collect existing `source_path` values into a set, skip any already-present source_path (dedup), csv-quote any field containing a comma, write back. Do NOT regenerate the whole file — preserve existing rows verbatim.

### 9. Update project `LOG.md`

If `20-projects/<slug>/LOG.md` is a stub (just `# <slug> — Log`), write the integration record under a dated `## YYYY-MM-DD — <action>` heading. Include: source dir, files created / merged / skipped counts, naming convention applied, MANIFEST rows added.

### 10. Verify

- `find notes/<subdirs> -name "*.md" | wc -l` matches expected count.
- Every new file starts with `---\ntitle:` frontmatter.
- `grep -rln "<old_filename>"` in new files returns nothing (all links rewritten).
- MANIFEST row count for this `source_repo` matches files processed.
- Merged file contains the `<!-- MERGED` separator.
- No existing vault file was deleted.

## Pitfalls

- **read_file false-empty / false-binary on valid UTF-8 Chinese files**: valid UTF-8 markdown with long lines or certain byte patterns is misreported by `read_file` in TWO ways — (a) `total_lines=0` with empty content, or (b) `is_binary: true` with a non-zero `file_size` and a "Binary file - cannot display as text" error. Both are false positives. Cross-check with `terminal` `file <path>` (should say "UTF-8 Unicode text") or `wc -l`; if those disagree with `read_file`, read via `terminal` (`head`, `cat`) or `execute_code` with `open(path, encoding="utf-8")`. Never treat either misreport as "empty" or "binary" without a `file`/`wc -l` cross-check — this hit BOTH the academic-writing work subagent and the review subagent on plain UTF-8 `.md` files during the 2026-08-06 wiki expansion.
- **Partial-match link rewriting**: a naive `str.replace("mode", "newmode")` corrupts prose. Always use word boundaries (`(?<![A-Za-z0-9_])` + `(?![A-Za-z0-9_])`) when replacing bare stems.
- **MANIFEST dedup**: re-running an integration must not create duplicate rows. Always check existing `source_path` values first.
- **source_repo slug mismatch**: existing vault files may use a slightly different slug suffix (e.g. `other/au-nn-potential-2025` vs task-specified `other/au-nn-potential`). Follow the task's specified slug for new files; note the discrepancy in LOG.md if it matters for traceability. Do not retroactively rewrite existing files' frontmatter unless asked.
- **Merging destroys structure**: only merge when the topic overlap is unambiguous and the existing file is a natural parent. When in doubt, create a new file and cross-link.
- **Headings in merged block**: always demote by one level so the merged H1 doesn't override the existing file's H1 title.
- **No batch deletes**: AGENTS.md forbids `rm -rf`. If a source file was merged and the vault copy of the source is now redundant, delete one explicit path at a time with a clear commit message. Never delete the original source-repo file (those repos are read-only).

## Pattern: extracting knowledge from raw calculation directories (no ai-guide)

When the source project has **no pre-written Markdown** (`ai-guide/` is empty — common for projects that started before AI usage), the task shifts from *importing existing knowledge* to *mining knowledge from raw computation files*. The vault's archive-layer rule (no fabrication / no new conclusions) still applies, but the extraction is legitimate because you are reading and recording what the files actually contain — not inventing results.

### What to mine from a VASP / DFT calculation directory

| File type | What to extract | How |
|---|---|---|
| `INCAR` | VASP parameters (ENCUT, ISIF, ISMEAR, NSW, IBRION, EDIFF, etc.) | `grep` or read representative INCAR per subdirectory; record in a parameter table |
| `KPOINTS` | k-mesh density, sampling method (Gamma/Monkhorst) | Read first few lines |
| `POSCAR` (head only) | Structure type, atom count, lattice constants | `head -8 POSCAR` — do NOT copy the full file |
| `*.py` (vasp_create, analysis scripts) | Structure generation logic, post-processing methodology | Read full script if <50KB; import to `scripts/` with frontmatter if reusable |
| `*.ipynb` | Workflow logic (cell-by-cell) | Use `execute_code` with `json.load` to extract cell sources; large notebooks (>100KB) summarize key cells only |
| `*.sh` | Workflow toolchain calls (pei_vasp_run_*, yin_vasp_univ_post, etc.) | Read to identify CLI tools used |
| `README.md` / `*.md` | Author-written documentation | Import directly with frontmatter |
| `*.log` | Run timestamps, parameter-change history | Read head for timestamp/parameters |

### Surveying strategy for large directories (>100k files)

**Do NOT** `find` + read every file — it will timeout. Use this tiered approach:

1. **Directory tree first**: `find <root> -maxdepth 2 -type d | sort` to understand structure.
2. **Filter to key files only**: `find` for `INCAR`, `KPOINTS`, `POSCAR`, `README*`, `*.py`, `*.ipynb`, `*.sh`, `*.md`, `*.txt` — exclude `OUTCAR`, `CONTCAR`, `CHGCAR`, `WAVECAR`, `DOSCAR`, `PROCAR`, `EIGENVAL`, `OSZICAR`, `IBZKPT`, `REPORT`, `PCDAT`, `XDATCAR`, `LOCPOT`.
3. **If find still returns >10k results** (common for parameter-sweep directories): pipe through `grep -vE` to exclude numbered subdirectories (`/[0-9]{2,}[-/]`), or limit to top-level scripts only.
4. **Batch INCAR parameter extraction**: use `execute_code` with Python — walk each major subdirectory, read the first INCAR found, parse key tags into a dict. Much faster than reading INCARs one-by-one via `read_file`.
5. **Read notebooks programmatically**: `execute_code` with `json.load(open(path))` + iterate `nb['cells']` to extract source code — avoids `read_file` overhead on large notebooks.

### Output structure for calculation-index.md

Create a single `notes/calculation-index.md` as the structured index:

```markdown
---
title: <project> 计算目录结构化索引
date: <YYYY-MM-DD>
tags: [<project-slug>, vasp, dft, calculation-index]
source_repo: other/<project-slug>
imported: <YYYY-MM-DD>
---

# <project> 计算目录结构化索引

## 0. 全局 VASP 参数基线
<table of common parameters across all INCARs>

## 1-N. 每个顶层子目录
### 子目录名 — 用途
- **路径**: `relative/path/`
- **结构**: <directory listing>
- **关键参数**: <from INCAR>
- **脚本/Notebook**: <what they do>
- **用途**: <inferred from filenames, INCAR, script content>
- **数据文件**: <key data outputs, not copied>

## 工具链依赖
<table of CLI tools, Python packages identified from scripts>

## 计算时间线
<from directory names with dates>

## 论文支撑关系
<mapping of calc dirs to paper sections>
```

### Importing scripts with provenance header

Reusable analysis scripts (<50KB) go to `scripts/` with provenance prepended as a header comment block (Python files cannot have YAML frontmatter — the `---` would be a syntax error in some interpreters):

```python
#!/usr/bin/env python3
# ---
# title: <descriptive title>
# date: <original date>
# tags: [<project-slug>, <topic>]
# source_repo: other/<project-slug>
# imported: <YYYY-MM-DD>
# ---

# 源路径: <relative/source/path.py>
# 用途: <one-line description>

<original script content verbatim>
```

> The `# ---` block is a comment-based provenance marker (grep-friendly, no Python syntax issues). The authoritative provenance lives in MANIFEST.csv. For `.md` files, use real YAML frontmatter instead.

### MANIFEST.csv for calculation directories

Record at directory level for raw data (not per-file — too many files):

```csv
other/<slug>,convergence/,skipped,,raw-calculation-data (2062 files: ENCUT/KPOINTS convergence test outputs)
other/<slug>,electronic_structure/vasp_create.py,imported,20-projects/<slug>/notes/calculation-index.md,methodology documented; script content summarized
other/<slug>,strain/.../add_extra_normal_modes.py,imported,20-projects/<slug>/scripts/hoec-add-extra-normal-modes.py,HOEC pure-normal mode generation; added provenance header
```

- Use `skipped` with directory-level path + file count in reason for raw calculation data.
- Use `imported` for scripts/READMEs that were actually copied (with frontmatter/header).
- Use `merged` for methodology that was summarized into `calculation-index.md` (script read but not copied verbatim — the knowledge was extracted, not the file).

### Pitfalls specific to calculation-directory mining

- **`find` on huge directories times out**: a VASP project with 400k+ files will timeout `find` at 60s. Use `timeout 90 find ... -name "INCAR" -o -name "*.py" ...` with explicit file-type filters, or split into per-subdirectory finds.
- **`execute_code` `os.walk` also times out** on 400k files — prefer `subprocess.run(["find", ...])` from within `execute_code` which is faster than Python's `os.walk`.
- **Notebooks with embedded output**: `.ipynb` files can be 1-2MB because of embedded output/images. Read only `nb['cells'][i]['source']` — skip `['outputs']` and `['metadata']`.
- **Multiple INCAR variants in one directory**: parameter-sweep directories have one INCAR per sweep point. Read only the first (or a representative middle point) — they differ only in the swept parameter.
- **Convergence difficulty history**: directory names like `5-36atoms-35kpoints-potim0.015-amin0.01-from4contcar` encode the debugging history. Record this in the index — it's valuable methodology knowledge (what was tried, what worked).
- **Non-git source directories**: if the source isn't a git repo, `source_commit` cannot be obtained. Omit it — MANIFEST's `source_repo` column is sufficient for traceability.
- **Python script provenance**: do NOT put YAML `---` frontmatter at the top of `.py` files — it's a syntax error. Use `# ---` comment blocks instead (see "Importing scripts" above).

## Pattern: multi-project batch integration (delegated)

When the task involves integrating **multiple source projects** into their respective `20-projects/` directories in one session, the orchestrator should NOT do all the work inline — context will overflow. Use delegation.

### 1. Write a PROJECT-MAP.md first

Create `20-projects/PROJECT-MAP.md` as the single entry point mapping each vault subdirectory to its actual server/local working directory:

```markdown
| Vault 目录 | 服务器/本地实际工作目录 | ai-guide 状态 |
|---|---|---|
| inplane-strain-general/ | /public3/home/.../20260227_cu_ag_al | 6 md + modeling/ |
| au-nn-potential/ | /public3/home/.../20250521_au_n2p2 | 18 md (gsfe/hoec/training) |
| au-phase-transition/ | /public3/home/.../20230907_au_dft | 空 (项目早于 AI 使用) |
```

Also document the `source_repo` slug convention (`other/<slug>`) for each project here. This file is the agent's cross-environment entry point for locating raw data.

### 2. Survey all source directories before dispatching

Batch the initial `ls`/`find`/`head` reads of ALL source project directories in one turn (parallel terminal calls). This gives the orchestrator enough context to write detailed delegation briefs without spending its own context budget on deep reads.

### 3. Dispatch one subagent per project (parallel)

Each subagent gets: the source directory path, the vault target directory, the existing vault files list, the source ai-guide file list, and the full constraints (frontmatter, naming, MANIFEST, no-delete, no-binary). The subagent does the merge-vs-new decision and file creation autonomously.

### 4. Dispatch review subagents after each work task completes

For each completed integration task, dispatch a **separate review subagent** that verifies: frontmatter compliance, content completeness (all source files have a vault counterpart), no original files lost, no binary files copied, MANIFEST registered, no fabricated content. If the review finds **major issues** (frontmatter missing, files lost, content fabricated), re-dispatch the work subagent with specific fix instructions. This work-then-review pattern is the user's explicit workflow requirement (#9, #10 in the original task list).

### 5. Manuscript handling

Check each source project for manuscript files (`*.docx`, `*.md`, `*.tex`). Manuscripts are the project's final deliverable and belong in `20-projects/<slug>/notes/` as a record. If the manuscript is `.md`, import with frontmatter. If `.docx`/`.tex`, register in `90-archive/INDEX.md`. If the manuscript lives in a *different* project directory (e.g. the DFT calculations are in `au_dft/` but the manuscript is in `cu_ag_al/manuscript/`), note the cross-project dependency in the calculation-index or LOG.md.

### 6. Unmanned / yolo-mode operation

When the user grants yolo permissions and leaves the session unmanned, file deletion must still be done cautiously — one explicit path at a time, never batch. If the session cannot complete all tasks before a deadline, write a delivery document to `ai-guide/` subdirectory documenting what was done and what remains.

## Pattern: collecting AI agent memories/configs

When the task asks to collect codex/claude-code/other AI agent memories and configs into `00-inbox/memories-*/`:

- **Direct copy, no secondary summarization**: the user explicitly does NOT want the memories reorganized or summarized into new syntheses. Keep the original file structure, just add a provenance annotation header.
- **Provenance header** (prepended to each file, before any frontmatter): `> 来源：原路径 X，采集于 YYYY-MM-DD`
- **Truncation**: files >100KB are truncated to 50KB, with a truncation note in the header.
- **Sensitive files skipped**: `auth.json`, `.credentials.json`, `.env`, sandbox-secrets directories. For `config.toml`/`settings.json`, replace API key/secret/token/password values with `[REDACTED]`.
- **Output structure**: mirror the source layout — `codex/` (global, memories, rollout-summaries, extensions) + `claude-code/` (global, plans, project-memories) + `shared-skills/` + `INDEX.md`.
- **INDEX.md**: record collection stats (file count, byte count, truncations, skipped files, directory structure).
- **Source file safety**: verify source files' mtime unchanged after collection (read-only copy).

Source locations on this server:
- Codex: `~/.codex/` (AGENTS.md, config.toml, memories/, history.jsonl)
- Claude Code: `~/.claude/` (CLAUDE.md, settings.json, plans/, projects/*/memory/)
- codex-config repo: `~/mysoft/pei/codex-config/` (shared skills)

## Pattern: backing up Hermes's own config

When the task asks to back up the *current host's* Hermes Agent configuration (`~/.hermes/`) into the vault — typically `00-inbox/memories-<hostname>/hermes/`, mirroring a reference backup like `memories/hermes/` from another host:

- **Scope**: `memories/` (MEMORY.md + USER.md), `config/` (config.yaml + SOUL.md), `skills/` (self-built dirs only), `cron/` (jobs.json if present), `scripts/sync_hermes_config.sh`.
- **Skill filtering is the critical step**: `~/.hermes/skills/` contains both real self-built directories AND symlinks to bundled/hub skills (`→ ../../.agents/skills/<name>`). Only copy real directories with `SKILL.md` or `DESCRIPTION.md`. See the detection command in `references/hermes-config-backup.md`.
- **Security**: verify `config.yaml` uses `key_env` / `${VAR}` references (not plaintext) before copying. Never copy `.env`, `auth.json`, `state.db`, `sessions/`, `cache/`, `logs/`.
- **Cross-platform sync script**: the PC version of `sync_hermes_config.sh` auto-detects `~/.hermes` on Linux; copy it verbatim.
- **README**: record `source_host`, self-built skill count + list, and a cross-host diff table (cron status, skill count, unique/missing skills vs reference host).
- **Delegation**: this is a good delegation candidate — dispatch a work subagent for the file operations, then a review subagent to diff source vs backup and verify no sensitive files leaked. See `references/hermes-config-backup.md` for the full pattern including the skill-filtering command, security pre-check, and review checklist.

## Pattern: merging multi-device memory snapshots into memories_core/

When two or more already-collected memory snapshots (e.g. `00-inbox/memories-zcm6/` and `00-inbox/memories/`) need to be unified into a single `00-inbox/memories_core/` directory with device-prefixed filenames and an INDEX.md, see `references/multi-device-memories-merge.md` for the complete pattern:

- **Merge decision matrix**: same-name-different-content → device-prefixed (`.zcm6.` / `.pc.`); identical content → one copy; device-unique → direct copy; same-dir-different-content → split by device.
- **Per-subtree rules**: claude-code (global prefixed, project-memories split), codex (global/memories prefixed, rollout-summaries merged), hermes (config/memories prefixed, skills PC-base+zcm6-supplement), shared-skills (merged), repo-instructions (PC-only direct copy).
- **INDEX.md output**: header + integration rules + per-subdir file listing + count summary + source mapping.
- **Verification**: per-subdir file counts, no empty dirs, source mtimes unchanged, INDEX total matches `find -type f | wc -l`.

## Pattern: 30-wiki synthesis & coverage audit

When the task is "更新 wiki" / "把新内容综合进 30-wiki" / "检查 wiki 覆盖度", the work has two phases: (1) **coverage audit** to find which source files are NOT yet synthesized into any wiki page, then (2) **delegated synthesis** of new wiki pages for the gaps. See `references/wiki-synthesis-workflow.md` for the reproduce-able technique (wikilink-extraction script, process-doc filter rules, the table-cell verification pattern that catches silent data-transcription errors).

### Phase 1 — Coverage audit (orchestrator does this inline, do NOT delegate)

1. **Collect all source stems**: glob `10-sources/**/*.md` + `20-projects/**/*.md`, exclude `LOG.md`/`PLAN.md`/`PROJECT-MAP.md`, key by stem (basename without extension).
2. **Extract wiki→source references**: for each `30-wiki/*.md`, regex `(?<!\!)\[\[([^\]#|]+)\]\]` (excludes image embeds `![[...]]` and alias/heading suffixes), strip path prefixes, match against the source-stem set.
3. **Orphans = source stems not referenced by ANY wiki page**. Group by directory to see the gap shape.
4. **Filter out process documents** — they look like orphans but are NOT synthesis candidates:
   - `prb-20260721-polishing-decisions-*` (revision decision logs)
   - `prb-transfer-*` (manuscript-transfer handoffs)
   - `stage-*-handoff.md` (already summarized in stage-status / wiki)
   - `manuscript-*-self-check*`, `*-evaluation-*`, `*-cover-letter*`
   - `codex-ppt-*`, `workbuddy-*`, `topic-research-prompt.md` (presentation instructions)
   - Anything named `*-codex.md` / `*-claude.md` paired with a non-suffixed twin (the twin is the canonical one)
   The rule of thumb: **process docs are "how we got here", knowledge docs are "what is true"**. Only the latter belongs in 30-wiki.
5. **Decide new wiki pages** from what remains: group orphan knowledge docs by topic; one wiki page per coherent topic cluster (typically 3-25 source files per page). Cross-reference against existing wiki pages to avoid duplication — if an existing wiki page already covers the topic, the new page must do a cross-reference (`见 [[existing]] 第X节`) not a copy.

### Phase 2 — Delegated synthesis (work subagent + review subagent)

Per the user's work-then-review requirement, NEVER write wiki pages inline in the orchestrator — context will overflow and there is no review gate.

1. **One work subagent per wiki page** (parallel if independent). Each gets: the source file list, the AGENTS.md/SCHEMA.md rules, the `vasp.md` template reference, explicit instruction to cross-reference existing wiki pages (list them), frontmatter spec (`source_repo: native`), the check_links.py verification command, and the "no fabrication" constraint.
2. **One review subagent** (after all work subagents finish) that verifies: structure (topic-organized not source-by-source), dedup vs existing wiki, wikilink resolution (run check_links.py), source-page list at end, "未采纳候选" section, frontmatter, AND **cell-by-cell numeric verification of any data tables** the work subagent transcribed from source files (see pitfall below).
3. **Orchestrator fixes** any NEEDS_FIX issues directly (small, targeted patches) — do NOT re-dispatch a work subagent for a 4-cell table fix; that wastes a round-trip.
4. **Commit at key nodes** via the `p-git-commit` skill — for unmanned/yolo sessions this can itself be delegated, but the orchestrator must confirm the repo boundary and verify `git diff --cached --check` passes.

### Pitfall: silent data-transcription errors in synthesized tables

A work subagent writing a summary table from a source file will silently transpose or invent numbers — in the 2026-08-06 expansion, 4 of 8 rows in a subpackage-coverage table had wrong "公开 API 数" values (the subagent conflated the source's "函数数" column with a "公开 API 数" label and miscounted several). **Eyeballing the table will not catch this.** The verification pattern:

1. After the work subagent reports done, read BOTH the source table and the wiki table programmatically via `execute_code` (regex the markdown rows into dicts).
2. Compare each numeric cell; print a mismatch table.
3. If mismatches exist, fix them via `patch` with explicit old/new cell values, then re-run the comparison to confirm 0 mismatches.

This cell-by-cell check is mandatory whenever a wiki page transcribes a multi-row data table from a source file. Add it to the review subagent's brief.

### Coverage-audit script (run via execute_code)

The core audit is a ~25-line Python script — collect source stems, regex-extract wikilinks from each wiki page, report orphans grouped by directory. See `references/wiki-synthesis-workflow.md` for the full reproduce-able script and the table-cell verification snippet.

## Support files

- `references/vault-conventions.md` — condensed AGENTS.md + SCHEMA.md rules (write tiers, frontmatter fields, MANIFEST format, naming).
- `references/link-rewrite-recipe.md` — working Python regex pattern for internal-link rewriting during kebab-case rename.
- `references/calc-dir-survey-recipe.md` — ready-to-run bash/Python snippets for surveying large VASP/DFT calculation directories (find filters, batch INCAR extraction, notebook source extraction).
- `references/hermes-config-backup.md` — pattern for backing up `~/.hermes/` into `00-inbox/memories-<hostname>/hermes/`: skill-filtering command (real dirs vs symlinks), security pre-check for config.yaml, output structure, README essentials, delegation checklist.
- `references/backup-verification-checklist.md` — concrete 6-point audit checklist (file completeness, security, README quality, sync script, timestamp, directory structure) for review subagents verifying a `00-inbox/memories-<host>/hermes/` backup snapshot. Proven on the zcm6 review (2026-08-06).
- `references/multi-device-memories-merge.md` — pattern for merging two `00-inbox/memories-<host>/` snapshots into a unified `memories_core/` with device-prefixed filenames, per-subtree merge rules, INDEX.md generation, and verification checklist. Proven on the zcm6+PC merge (2026-08-06).
- `references/memories-merge-audit-checklist.md` — review-side PASS/FAIL audit checklist for the work-then-review pattern: 5 sections (core files, device-specific files, INDEX.md, source integrity, subdir structure) with concrete commands. Proven on the zcm6+PC merge review (2026-08-06); includes the child-skill-granularity dedup check that caught the dropped `vault/vault-source-integration/` and the 3-way INDEX count-drift check.
- `references/memories-merge-delegation-pattern.md` — orchestrator-level 4-subagent delegation plan for a multi-device memories merge session (work-then-review-then-fix-then-commit): which phase to delegate vs do inline, timing, and pitfalls observed in production. Proven on the zcm6+PC merge (2026-08-06).
- `references/synthesize-device-memory-files.md` — pattern for authoring the two synthetic `MEMORY.<device>.md` files in `memories_core/` after the mechanical merge: required section template, source files to read per device, zcm6-vs-PC difference table, writing method, and verification. Proven on the 2026-08-06 synthesis.
- `references/wiki-synthesis-workflow.md` — the 30-wiki coverage-audit + delegated-synthesis pipeline: the wikilink-extraction script (finds orphan source files not referenced by any wiki page), process-document filter rules, and the table-cell verification pattern that caught silent data-transcription errors during the 2026-08-06 expansion. Proven on the pjvasp-package.md + academic-writing.md wiki expansion.
