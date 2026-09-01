# Multi-Device Memories Merge — Audit Checklist

Review subagent checklist for auditing a `memories_core/` merge once the
work subagent claims completion. Each item returns PASS or FAIL; FAIL items
get a concrete problem statement + suggested fix. Lead the report with the
PASS/FAIL table, then expand the FAILs.

This is the review-side counterpart to `multi-device-memories-merge.md`
(the work-side pattern). Proven on the zcm6+PC merge review (2026-08-06).

## 1. Core files (device-agnostic)

Files: `SOUL.md`, `MEMORY.md`, `USER.md`, `AGENTS.md` at the `memories_core/`
root — these are the hand-authored "通用" integrations, so they must contain
NO device-specific hardcoded paths.

- **No hardcoded paths** — grep each of the 4 files for device markers and
  confirm zero hits:
  ```bash
  grep -nE 'public3|/Users/louis|C:|F:|BaiduSyncdisk|/public3/home' \
    SOUL.md MEMORY.md USER.md AGENTS.md
  ```
  Expected: no match in any file.
- **No missing common knowledge** — the 4 files should preserve all
  cross-device shared facts (user identity, vault tier model, Zotero key
  alphabet, shared skill list, HOEC workflow constraints, Codex rollout
  overview). Cross-check against the two source `MEMORY.md` / `USER.md` /
  `AGENTS.md` files for any common content that vanished.
- **No contradictions** — e.g. `MEMORY.md` and `USER.md` should agree on
  the user's identity; `MEMORY.md` and `AGENTS.md` should agree on the shared
  skill list. Mild duplication across these files is acceptable (different
  reader entry points); outright contradiction is not.

## 2. Device-specific files

Files: `MEMORY.zcm6.md`, `MEMORY.pc.md` at the root.

- **Key paths present** — `MEMORY.zcm6.md` must carry Home path
  (`/public3/home/scg6928/`), pjvasp source, codex-config, venv root, git
  binary, hermes config source. `MEMORY.pc.md` must carry user path
  (`C:\Users\louis\`), data drive (`F:\BaiduSyncdisk\...`), pjvasp repo,
  myobsidian vault, Git Bash path, Zotero install path, hermes config source.
- **Key configs present** — venvs, SSH forwarding chain, proxy ports,
  Hermes provider format, Codex `[features]` block, etc. Spot-check ~3
  categories per device against the source `INDEX.md` / `INDEX.<device>.md`.
- **No obvious omission** — if a section in the source `memory_summary.md`
  or `MEMORY.md` carried a device-specific fact, that fact should appear in
  the synthetic `MEMORY.<device>.md`.

## 3. INDEX.md

- **File count matches reality** — three numbers must agree:
  1. Header line `> 总文件数：N`
  2. Bottom summary table `合计` cell
  3. Actual `find . -type f | wc -l` run from the `memories_core/` root

  A 3-way mismatch is a real failure mode (observed: 442 / 443 / 445).
  If they disagree, recompute (3) and update (1) + (2) + every per-area row.
- **Per-area counts match** — for each row in the summary table, run
  `find <subdir> -type f | wc -l` and confirm the number matches the cell.
- **Source mapping accurate** — each file's claimed source (zcm6 / PC /
  integrated) matches where the file actually came from. Spot-check by
  diffing the memories_core file against the corresponding source file.

## 4. Source integrity

- **Source dirs unmodified** — both source directories are typically
  untracked in git (the whole `00-inbox/` tree is untracked), so
  `git status` will NOT show modifications. Verify via mtime instead:
  every file in `memories-zcm6/` and `memories/` should have an mtime
  ≤ the collection date (no post-collection writes).
  ```bash
  find memories-zcm6/ memories/ -type f -newer <cutoff_marker> -printf '%T+ %p\n'
  ```
  where `<cutoff_marker>` is a file known to be at the collection boundary
  (e.g. `memories_core/INDEX.md`). Expected: no source files newer than the
  cutoff.
- **File count conservation** — for merged subtrees,
  `count(memories_core/<subdir>)` should equal `count(src_a/<subdir>)` +
  `count(src_b/<subdir>)` (minus identical-content dedup, plus synthesized
  files if any). For split subtrees (e.g. `project-memories-zcm6/` +
  `project-memories-pc/`), each side's count should equal its source's count.

## 5. Subdirectory structure

For each of `claude-code/`, `codex/`, `hermes/`, `shared-skills/`,
`repo-instructions/`:

- **Files reasonably archived** — top-level subdirs match the per-subtree
  rules in `multi-device-memories-merge.md`. No stray files at the wrong
  level.
- **No same-name conflicts** — same-basename files in different subdirs are
  NOT conflicts (legitimate, e.g. `SKILL.md` per skill). A real conflict is
  two files at the SAME path. Use:
  ```bash
  find <subdir> -type f | sort | uniq -d   # should be empty
  ```
- **No silently-dropped device-unique content** — this is the high-stakes
  check. For shared-parent directories (especially `hermes/skills/`),
  enumerate the child-skill inventory of EACH device source, then confirm
  every device-unique child appears in memories_core:
  ```bash
  # zcm6-only child skills under a shared parent
  comm -23 \
    <(find memories-zcm6/hermes/skills/<parent>/ -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort) \
    <(find memories/hermes/skills/<parent>/ -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort)
  ```
  Every name printed by `comm -23` (zcm6-only) and `comm -13` (PC-only)
  MUST exist under `memories_core/hermes/skills/<parent>/`. A missing
  device-unique child skill is a FAIL — this exact bug dropped zcm6's
  `vault/vault-source-integration/` (2 files) when PC's
  `vault/vault-source-import/` was kept as the "base".

## Output format

Lead with a PASS/FAIL table, then expand each FAIL with:
- **Problem**: one-sentence description
- **Evidence**: the command output / count mismatch that exposed it
- **Suggested fix**: the concrete edit (file to copy, line to update, etc.)

Keep the report tight — the orchestrator consumes it as a summary, so do
not replay every command's full output.
