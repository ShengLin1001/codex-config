# Multi-Device Memories Merge Pattern

Merge two or more already-collected memory snapshots (from different devices)
into a single unified `memories_core/` directory with device-prefixed filenames
and an INDEX.md. This is distinct from *collecting* memories from a live host
(that's the collecting pattern in SKILL.md) — here both source snapshots already
exist in `00-inbox/memories-<host>/` and need to be unified.

## When to use

- "把 zcm6 和 PC 的 memories 整合到 memories_core/"
- "合并两台设备的 memories 源目录"
- Any task that unifies two `00-inbox/memories-*/` snapshots into one canonical
  `memories_core/` with traceability.

## Inputs

| Role | Example |
|------|---------|
| Source A | `00-inbox/memories-zcm6/` (CentOS HPC snapshot) |
| Source B | `00-inbox/memories/` (PC / Windows snapshot) |
| Target | `00-inbox/memories_core/` (merged output) |

Both sources may already contain an `INDEX.md` from the collection step.

## Merge decision matrix

For every file or subdirectory encountered in either source:

| Condition | Disposition | Naming |
|-----------|-------------|--------|
| Same filename, different content | **DEVICE-PREFIXED** | `MEMORY.zcm6.md` + `MEMORY.pc.md` |
| Same filename, identical content (incl. trailing-newline-only diff) | **ONE COPY** | keep the more complete version (usually PC) |
| File exists only in one source | **DIRECT COPY** | original name, no prefix |
| Subdirectory with same name but different file content | **SPLIT BY DEVICE** | `project-memories-zcm6/` + `project-memories-pc/` |
| Subdirectory with same name, unique filenames inside | **MERGE** | one directory, files from both sources |
| Skills directory (one source more complete) | **BASE + SUPPLEMENT** | use complete source as base, copy unique dirs from other |

### Identical-content check

Use `diff` — a file that differs only in trailing newline is safe to keep as
one copy. Always check; do not assume.

```bash
diff <src_a>/file.md <src_b>/file.md && echo "IDENTICAL" || echo "DIFFERENT"
```

### Filename collision check (for merge directories)

Before merging two directories that should have unique filenames, verify no
collisions:

```bash
comm -12 \
  <(find <src_a>/dir/ -type f -exec basename {} \; | sort) \
  <(find <src_b>/dir/ -type f -exec basename {} \; | sort)
# empty output = no collisions, safe to merge
```

## Per-subtree merge rules

The memories snapshots typically share this structure. Here is the merge rule
for each subtree:

### Root-level files

- `INDEX.md` → `INDEX.zcm6.md` + `INDEX.pc.md` (device-prefixed)
- `AGENTS.md`, `MEMORY.md`, `SOUL.md`, `USER.md` → if already integrated by the
  orchestrator into a unified version, leave those in root; the device-specific
  copies go into subdirectories with prefixes.

### claude-code/

- `global/CLAUDE.md` → `CLAUDE.zcm6.md` + `CLAUDE.pc.md` (device paths differ)
- `global/settings.json` → `settings.zcm6.json` + `settings.pc.json`
- `plans/` → merge (filenames are unique per device)
- `project-memories/` → split: `project-memories-zcm6/` + `project-memories-pc/`
  (content differs, same subdir names like `fluent/`, `au-dft/`)

### codex/

- `global/AGENTS.md` → zcm6 as primary `AGENTS.md`, PC as `AGENTS.pc.md`
- `global/config.toml` → `config.zcm6.toml` + `config.pc.toml` (paths differ)
- `global/default.rules` → PC-only, direct copy
- `memories/MEMORY.md` → `MEMORY.zcm6.md` + `MEMORY.pc.md`
- `memories/memory_summary.md` → `memory_summary.zcm6.md` + `memory_summary.pc.md`
- `memories/raw_memories.md` → `raw_memories.zcm6.md` + `raw_memories.pc.md`
- `memories/` device-unique files (e.g. `ad_hoc-instructions.md`, `M-task-group.md`) → direct copy
- `rollout-summaries/` → merge into one dir (timestamped filenames, no collisions)
- `memory-skills/` → merge (usually one source only)
- `extensions/` → merge (usually one source only)

### hermes/

- `config/config.yaml` → `config.zcm6.yaml` + `config.pc.yaml` (paths differ)
- `config/SOUL.md` → one copy if identical (trailing-newline-only diff is OK)
- `memories/MEMORY.md` → `MEMORY.zcm6.md` + `MEMORY.pc.md`
- `memories/USER.md` → `USER.zcm6.md` + `USER.pc.md`
- `skills/` → PC (more complete) as base, copy zcm6-unique dirs (e.g. `vault-integration/`). **Dedup at child-skill granularity, not parent** — see the matching pitfall below: if both devices share a parent like `skills/vault/` but each carries a *different* child skill (`vault-source-integration/` on zcm6 vs `vault-source-import/` on PC), copy BOTH child dirs; do not let "use PC as base" silently drop the zcm6-only child.
- `cron/jobs.json` → `jobs.zcm6.json` + `jobs.pc.json` (zcm6 may have only `.gitkeep`)
- `scripts/sync_hermes_config.sh` → one copy if identical
- `README.md` → PC version (more detailed)

### shared-skills/

- Merge both sources. zcm6 may have `codex-config/` (original structure with
  `skills/` subdir), PC may have `codex-config-repo/` + `codex-config-skills/`
  (refactored structure). Both are preserved — they represent different
  organizational stages of the same content.

### repo-instructions/

- Usually PC-only. Direct copy.

## INDEX.md (output)

Create `memories_core/INDEX.md` at the target root with:

1. **Header**: source directories, collection date, total file count.
2. **Integration rules table**: how same-name / identical / device-unique files
   were handled.
3. **Per-subdirectory file listing**: each subtree with its files, source
   attribution, and one-line description.
4. **File count summary table**: per-area counts + grand total.
5. **Source mapping**: which device each file/dir came from.
6. **Safety note**: confirm source files unmodified (read-only copy).

## Verification checklist

After the merge:

1. **File count per subdirectory** — `find <dir> -type f | wc -l` for each
   subtree; compare against source sums (merged dirs = src_a + src_b;
   split dirs = src_a count + src_b count in respective `-zcm6/`/`-pc/` dirs).
2. **No empty directories** — `find <target> -type d -empty` should return nothing.
3. **Source files unmodified** — `stat -c '%Y' <src_file>` mtime unchanged.
4. **INDEX.md total matches** — grand total in INDEX.md equals
   `find <target> -type f | wc -l` (remember INDEX.md itself adds +1).
5. **Device-prefixed pairs exist** — for every file that should be split,
   both `.zcm6.` and `.pc.` versions exist.

## Pitfalls

- **`find` phantom `skills` dir**: `find <dir> -maxdepth 1 -type d` can list
  a `skills` entry that doesn't actually exist when the path contains a
  `skills/` subdirectory elsewhere in the tree. Cross-check with
  `ls -d <dir>/skills` before acting on it.
- **`cp -rn` (no-clobber) for shared-skills merge**: use `cp -rn` for the
  second source so PC files don't overwrite zcm6 files where paths overlap.
  But if you WANT PC to be primary (overwrite zcm6), use plain `cp -r` for PC
  first, then `cp -rn` for zcm6.
- **Trailing newline differences**: `diff` reports these as DIFFERENT, but the
  content is functionally identical. For SOUL.md and sync scripts, treat
  trailing-newline-only diffs as "identical, keep one copy."
- **INDEX.md self-count**: after creating INDEX.md, the total file count
  increases by 1. Update the summary table to include INDEX.md in the root
  count, or the numbers won't match.
- **INDEX count drift across header / table / actual**: the header line
  (`> 总文件数：N`), the bottom summary table's `合计` cell, and the real
  `find <target> -type f | wc -l` can disagree — especially after adding
  device-specific synthetic files (`MEMORY.zcm6.md`, `MEMORY.pc.md`) that
  the original per-subdir planning didn't account for. The header is often
  written first against a plan, then the table is written against partial
  reality, and the synthesized `<device>.md` files land last. **Reconcile all
  three numbers as the final step** — recompute `find ... | wc -l`, then update
  the header total AND every per-area row to match. A 3-way mismatch
  (442 / 443 / 445) is a real failure mode observed in production.
- **Same-parent-dir-different-child-skill drops content**: when both devices
  share a parent directory like `skills/vault/` but each carries a *different*
  child skill inside it (`vault-source-integration/` on zcm6 vs
  `vault-source-import/` on PC), applying "use device-A as base" at the parent
  level silently drops the device-B-only child skill. The collision check
  (`comm -12` of basenames) reports no collision because the child names
  differ — but a naive "copy PC first, then `cp -rn` zcm6" still works IF you
  let it recurse into the shared parent. The bug appears when an agent
  special-cases "skills is the same dir, keep PC's version" without recursing.
  Always compare child-skill inventories at the leaf-SKILL level, not the
  top-level category dir, before deciding "one copy suffices".
- **BOM-encoded files**: some tools detect zcm6's INDEX.md as binary (BOM).
  Use `cp` directly — do not attempt to read+rewrite, which may strip or
  corrupt the BOM.
- **Large rollout-summaries merge**: zcm6 (116) + PC (138) = 254 files. Use
  `cp <src>/*.md <target>/` (glob) rather than `cp -r` to avoid copying the
  source directory itself as a subdirectory.
