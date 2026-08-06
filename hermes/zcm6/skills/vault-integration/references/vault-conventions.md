# Vault Conventions Condensed Reference

Condensed rules from `AGENTS.md` + `SCHEMA.md` of the vault at `~/mysoft/pei/myobsidian`. Read the originals for edge cases; this is the working checklist.

## Three-tier write model

| Dir | Tier | Agent may |
|---|---|---|
| `10-sources/`, `20-projects/` | **Archive layer** | Carry, sort, reformat, merge/dedup, add missing images, fix format errors, integrate PPT-extracted notes into same-topic source files. **NO synthesizing new conclusions / overviews / inferences** — synthesis only in `30-wiki/`. |
| `30-wiki/` | **Creation layer** | Cross-source synthesis, dedup, interlink, infer, restructure. New synthesis pages only here. Must list source pages at the end. |
| `00-inbox/` | **Feed/triage** | Classify and move into the two layers above; not permanent storage. |

### Unlock condition for 10/20 writes

Agent may write to `10-sources/` / `20-projects/` ONLY when ALL hold:

1. File is registered as `imported` in `MANIFEST.csv` (or this op is the registration).
2. No information loss — merges preserve a traceable link or git history.
3. No batch delete — merged originals deleted one explicit path at a time, with a commit message naming the merge target.
4. Source repos (myhexo / Being-a-phd-student / pjvasp work projects) remain read-only. The unlock applies only to the vault's own copies.

## Provenance frontmatter (minimal)

Imported file:

```yaml
---
title: <Chinese or descriptive title>
date: <original creation date; priority: original frontmatter > git log first commit > file mtime>
tags: [<topic>, ...]
source_repo: <myhexo | phd | other/<slug> | native>
imported: <YYYY-MM-DD>
---
```

Vault-original (`30-wiki/`, agent synthesis):

```yaml
---
title: ...
date: <creation date>
tags: [...]
source_repo: native
imported: <YYYY-MM-DD>
---
```

### Deprecated (NOT in file frontmatter — only in MANIFEST.csv)

- `source_path` — query MANIFEST.csv's `source_path` column.
- `source_commit` — query MANIFEST.csv (the `source_repo` column locates the repo; commit history is in the repo's git log).

Reason: MANIFEST.csv already records `source_repo, source_path, disposition, target_path, reason` per file; duplicating in file headers is redundant and these fields are rarely used post-migration. `source_repo` stays in the header because it's lightweight and answers "which repo is this from" without a MANIFEST lookup.

### Migration cleanup order

When cleaning frontmatter of a historical file: confirm it is already `imported` in MANIFEST with complete `source_path` BEFORE deleting the file's `source_path` / `source_commit` fields. If not yet in MANIFEST, register first, then strip — order cannot reverse.

## Naming

- Filenames: lowercase-hyphen only (`vasp-compile-notes.md`). No Chinese, no spaces, no uppercase.
- Chinese title goes in frontmatter `title`, not the filename.

## Double-link conventions

- Doc-to-doc: `[[filename]]` (no extension; Obsidian resolves).
- Image embed: `![[images/<subdir>/x.png]]` (global from vault root; not relative path; not Markdown image syntax).
- Images live in `images/<source-article-or-topic>/`, not scattered next to articles.

## One file, one topic

If a source file mixes unrelated topics, split into multiple files and cross-link. Don't stuff multiple topics in one file.

## `30-wiki/` extra

Synthesis pages must list the source pages they integrate (`10-sources/`, `20-projects/` specific files) at the end — traceability.

## MANIFEST.csv format

```csv
source_repo,source_path,disposition,target_path,reason
```

`disposition` is one of:

- `imported` — copied/converted into vault as-is.
- `merged` — content folded into another target file.
- `archived` — registered in `90-archive/INDEX.md`, body not copied.
- `skipped` — not imported (reason mandatory).
- `pending` — stage-1 triage temporary state; must be cleared later.

**Acceptance rule**: total source files == MANIFEST-covered files. Directory-level rows (e.g. `themes/,skipped,,hexo-infra (89 files)`) count by the N declared in `reason`; no per-file expansion needed. Mismatch = omission, must be found.

## Forbidden

- **Three source repos fully read-only**: don't modify/move/delete/`git pull` (beyond read) in:
  - `F:/BaiduSyncdisk/version20240608/main_code_space/myhexo`
  - `F:/BaiduSyncdisk/version20240608/main_code_space/Being-a-phd-student`
  - `Being_a_phd_student_baiducloud` and `pjvasp_package` work project sources
- **No batch delete**. One explicit path at a time; for batch, stop and ask the user.
- **No PDF / binary / raw calculation data in vault**. Vault must be greppable, `git diff`-able, LLM-context-friendly. Unconvertible materials go to `90-archive/INDEX.md`, body stays in place.

## Environment

- All file IO UTF-8 (`encoding="utf-8"`).
- Windows: `python` not `python3`. Set `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` before running Python (avoid Chinese mojibake).
