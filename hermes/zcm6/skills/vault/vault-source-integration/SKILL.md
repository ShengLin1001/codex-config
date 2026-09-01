---
name: vault-source-integration
description: "Merge external project knowledge into the Obsidian vault."
metadata:
  version: "1.0.0"
  created: 2026-08-04
---

# vault-source-integration

Integrate knowledge from external project directories into the Obsidian vault without
blindly copying — deduplicate against existing vault content, add provenance frontmatter,
and track every import in MANIFEST.csv + LOG.md.

## When to use

- User provides a source directory (e.g. `mywork/20260227_cu_ag_al/ai-guide/`) and a
  vault target (e.g. `20-projects/inplane-strain-general/`).
- User says "整合", "导入", "merge", "migrate", "归档" from a project into the vault.
- AGENTS.md governs the vault: 10-sources/ and 20-projects/ are archive layers —
  you may transport, classify, format-convert, merge/dedup, supplement missing images,
  and fix format errors. You may NOT fabricate summaries or infer new conclusions.

## Core workflow

1. **Scan both sides in parallel** — list source files and existing vault files together.
   Read the vault's `LOG.md`, `PLAN.md`, and any `_import/MANIFEST.csv` for prior
   import history. Batch independent reads.

2. **Read source files** — read each source `.md` file. For binary-detected files (UTF-8
   with CJK that read_file flags as binary), fall back to `terminal` with `iconv` or `cat`
   to read them.

3. **Dedup against existing vault content** — for each source file, search the vault's
   `notes/` directory using `search_files` with topic keywords. Compare titles, headers,
   and content. Three possible outcomes per file:
   - **Already exists (identical)** — content verified via `diff` (ignoring frontmatter).
     Skip; record as `already-exists` in MANIFEST.
   - **Already exists (partial)** — merge new information into the existing file via
     `patch`. Do NOT overwrite or delete existing content.
   - **New content** — create a new file with provenance frontmatter.

4. **Create new files** — write to `notes/` with provenance frontmatter:
   ```yaml
   ---
   title: <descriptive title>
   date: <source file date>
   tags: [<project-slug>, <topic>, ...]
   source_repo: other/<project-name>
   imported: <YYYY-MM-DD>
   ---
   ```
   - File names: lowercase, hyphenated (e.g. `prb-transfer-modeling-hcp-static-vs-relax-mode-zh.md`).
   - Follow existing naming conventions in the target `notes/` directory.

5. **Import key images** — copy manuscript-critical figures (Fig 5, Fig S6, etc.) to
   `images/<subdir>/`. Embed in notes with `![[images/subdir/file.png]]` wikilinks.
   - Do NOT copy PDFs, binary data, `.pptx`, `.pkl`, `.pyc`, or raw calculation data.
   - `.py` scripts are knowledge artifacts but typically remain at source path (executable
     tool code, not vault documentation). Import only if the user explicitly asks.

6. **Check manuscript directories** — if the source project has manuscript `.md` files:
   - If `.md` → check if already imported; if not, import to `notes/`.
   - If `.docx` → do NOT import; register in `90-archive/INDEX.md` as "not imported".
   - Working revisions superseded by a later version already in vault → skip, document
     in MANIFEST with reason.

7. **Register in MANIFEST.csv** — append rows to `_import/MANIFEST.csv` (vault root):
   ```
   source_repo,source_path,disposition,target_path,reason
   ```
   Dispositions: `imported`, `already-exists`, `skipped`, `merged`, `archived`.
   Include a reason for every non-trivial decision.

8. **Update LOG.md** — write/update `<project-dir>/LOG.md` with:
   - Date of integration
   - Table of new files created (source → vault target → content summary)
   - Files already in vault (verified identical)
   - Skipped files with reasons
   - Images imported
   - MANIFEST reference

## Pitfalls

- **Binary detection false positive**: `read_file` may flag UTF-8 files with CJK as
  binary. Always try `terminal` with `cat` or `iconv -f UTF-8 -t UTF-8` as fallback.
- **Frontmatter offset**: when comparing vault (with frontmatter) vs source (without),
  use `tail -n +<N>` to skip frontmatter lines before `diff`. Vault files typically have
  7-8 lines of frontmatter + one blank line.
- **Naming conventions vary per project**: check existing vault files in the target
  `notes/` dir before naming new files. `prb-transfer-*`, `prb-20260721-*`, `assessment-*`
  are all conventions used in different batches.
- **MANIFEST lives at vault root**: `_import/MANIFEST.csv` is at the vault root, NOT
  inside `20-projects/<slug>/`. The vault root is `/public3/home/scg6928/mysoft/pei/myobsidian/`.
- **source_repo naming**: use `other/<project-name>` (the slug from the source path).
  Prior batches may use `other/<project-name>-<year>` — check existing MANIFEST entries
  for the same project to stay consistent, but follow the user's explicit instruction
  if they specify a different source_repo string.
- **Don't delete or overwrite**: merging means adding to existing files, never replacing.
  Use `patch` for targeted additions.

## Verification

After integration, verify:
- All new `.md` files have valid frontmatter (`source_repo`, `imported` fields present).
- Image files exist at the paths referenced in notes.
- MANIFEST.csv has no duplicate entries for the same source file.
- LOG.md updated with the integration record.
- Total notes count increased by the expected number.

## Reference files

- `references/vault-structure.md` — vault directory layout, AGENTS.md rules, and
  provenance frontmatter template.
