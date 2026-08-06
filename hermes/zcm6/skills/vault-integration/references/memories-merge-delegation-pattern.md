# Multi-Device Memories Merge — Orchestrator Delegation Pattern

Proven delegation plan for a multi-device memories merge session (zcm6+PC →
memories_core, 2026-08-06). The orchestrator stays lean; context-heavy work
goes to subagents. Total wall-clock ~30 min for 447 output files + 638-file
git commit.

## Task shape

User asks to unify two `00-inbox/memories-<host>/` snapshots into
`00-inbox/memories_core/`, outputting device-agnostic core files
(SOUL/MEMORY/USER/AGENTS) + device-specific files (MEMORY.zcm6.md,
MEMORY.pc.md) + a consolidated INDEX.md.

## Delegation plan (4 subagents, work-then-review)

| Phase | Who | Does what | Context needed |
|-------|-----|-----------|----------------|
| 0 (orchestrator) | inline | Create `memories_core/` dir tree. Write the 4 core files (SOUL/MEMORY/USER/AGENTS) — these are device-agnostic synthesis the orchestrator can do quickly from source reads done before dispatch. | All source INDEX.md + hermes MEMORY.md/USER.md + codex memory_summary.md (2 files per device) |
| 1 (subagent A) | leaf | Write `MEMORY.zcm6.md` and `MEMORY.pc.md` — device-specific synthesis with hardcoded paths. Read source files via `terminal cat` (read_file rejects BOM). | Full source file listing + paths to the ~10 key files per device |
| 1 (subagent B) | leaf, parallel with A | Mechanical merge: copy all source files to `memories_core/` subdirs with device prefixes. Create INDEX.md. Report per-subdir file counts. | Per-subtree merge rules (see multi-device-memories-merge.md) |
| 2 (subagent C) | leaf, after A+B | Audit: 5-section PASS/FAIL checklist (core files / device files / INDEX / source integrity / subdir structure). Lead with PASS/FAIL table. | memories-merge-audit-checklist.md reference |
| 2b (orchestrator) | inline | Fix any FAIL items from C's report. Typical: INDEX count drift (3-way mismatch), dropped device-unique child skill (vault-source-integration/). | C's report |
| 3 (subagent D) | leaf | git commit + push via p-git-commit skill. Stage the two new dirs, commit, pull --ff-only, push. | p-git-commit skill loaded |

## Key decisions

- **Core files written by orchestrator, not delegated**: the 4 device-agnostic
  files require cross-device synthesis — reading both devices' sources and
  extracting shared knowledge. This is ~4 write_file calls and keeps the
  orchestrator in control of the "what is device-agnostic" boundary.
- **Device-specific files delegated**: MEMORY.zcm6.md and MEMORY.pc.md each
  require reading 10+ source files from one device — context-heavy, perfect
  for a leaf subagent.
- **Mechanical merge delegated in parallel**: the file-copy-and-rename work
  is independent of the device-specific synthesis, so subagents A and B run
  concurrently.
- **Audit is mandatory**: subagent C's checklist caught 2 FAILs in production
  (INDEX 3-way count drift + dropped vault-source-integration/). Without the
  audit, both bugs would have shipped.
- **Fixes done by orchestrator**: the 2 FAIL fixes were small (1 cp command +
  4 patch calls to INDEX.md). Not worth a subagent round-trip.

## Timing (observed)

| Phase | Duration |
|-------|----------|
| Orchestrator source reads + core file writes | ~5 min |
| Subagent A (device files) | ~12 min |
| Subagent B (mechanical merge) | ~7 min (finishes first) |
| Subagent C (audit) | ~15 min |
| Orchestrator fixes | ~2 min |
| Subagent D (git commit+push) | ~4 min |
| Total | ~30 min (with parallelism) |

## Pitfalls observed

- **Subagent B may create an empty `skills/skills/` phantom dir** from
  `cp -r` of shared-skills. Check and clean: `find <target> -type d -empty`.
- **Subagent A's summary may be truncated** in the live transcript log at
  ~500 chars. The full result is in
  `~/.hermes/cache/delegation/subagent-summary-0-<timestamp>.txt`.
- **Subagent C's audit report** is also truncated in the log; read it from
  the subagent-summary file, not the live transcript.
- **INDEX count drift**: the header (`> 总文件数：N`) is written first against
  a plan, the table is written against partial reality, and synthesized
  device files land last. Always reconcile header + table + actual
  `find | wc -l` as the final step.
- **Dropped child skill**: when one device has `skills/vault/vault-source-integration/`
  and the other has `skills/vault/vault-source-import/`, "use PC as base"
  drops the zcm6-only child. Always compare child-skill inventories at the
  leaf level.
