# Backup/Snapshot Verification Checklist

Concrete checklist for a **review subagent** validating a vault backup integration
(e.g. `00-inbox/memories-<host>/hermes/` collected from a remote server's `~/.hermes/`).
Proven on the zcm6 Hermes config backup review (2026-08-06).

The goal is a structured PASS/FAIL/WARN report across six dimensions, ending
with an overall verdict (PASS or NEEDS_FIX). Run every check with real tool
output — never report a check as passing from assumption.

## 0. Inputs

Before starting, confirm three paths from the task context:

| Role | Example |
|------|---------|
| Source dir | `/public3/home/<user>/.hermes/` (the live config on the remote host) |
| Backup dir | `00-inbox/memories-<host>/hermes/` (the vault snapshot under review) |
| Reference dir | `00-inbox/memories/hermes/` (an already-validated snapshot, usually the PC version) |

If any of the three is missing, report FAIL immediately — the review cannot
proceed without a source to diff against.

## 1. File completeness — PASS/FAIL

For every file class the backup should contain, `diff` source vs backup and
confirm IDENTICAL. Typical classes for a Hermes config backup:

- `memories/MEMORY.md`, `memories/USER.md`
- `config/config.yaml`, `config/SOUL.md`
- Each self-built skill directory: `diff -rq <src>/skills/<name> <dst>/skills/<name>`
  for every expected skill. Report a per-skill PASS line and the file count
  from each side (they must match).
- `scripts/sync_hermes_config.sh`

```bash
# Per-skill diff with file-count cross-check
SRC=/path/to/source/skills
DST=/path/to/backup/skills
for s in apple autonomous-ai-agents creative email github media mlops \
         note-taking productivity research smart-home social-media vault \
         vault-integration; do
  sc=$(find "$SRC/$s" -type f 2>/dev/null | wc -l)
  dc=$(find "$DST/$s" -type f 2>/dev/null | wc -l)
  diff -rq "$SRC/$s" "$DST/$s" >/dev/null 2>&1 \
    && echo "PASS: $s ($sc=$dc files)" \
    || echo "FAIL: $s differs (src=$sc dst=$dc)"
done
```

Also verify no **extra** skill dirs exist in the backup that aren't in the
expected list — that catches accidental inclusion of symlink/bundled skills.

## 2. Security — PASS/FAIL

`find` the backup directory for every sensitive file class that must NOT be
present. Report each as PASS (zero matches) or FAIL (with the leaked path).

```bash
DST=/path/to/backup
for pattern in ".env" ".env.*" "auth.json" "auth.json.bak" "auth.json.bak.*" \
               "*.lock" "*.bak" "*.bak.*" "state.db" "state.db-*" \
               "sessions" "cache" "logs"; do
  hits=$(find "$DST" \( -name "$pattern" \) 2>/dev/null)
  [ -z "$hits" ] && echo "PASS: no $pattern" || echo "FAIL: leaked $pattern -> $hits"
done

# Symlinks must be absent (symlink skills are bundled, not self-built)
find "$DST" -type l 2>/dev/null | grep -q . \
  && echo "FAIL: symlinks present" || echo "PASS: no symlinks"

# Bundled/symlink skill dirs must not have been copied
find "$DST" -type d \( -name "nature-*" -o -name "p-*" -o -name "vercel-*" \
  -o -name "web-*" -o -name "writing-*" -o -name "find-skills" \
  -o -name "agent-browser" -o -name "academic-*" -o -name "deploy-*" \
  -o -name "researchwrite" \) 2>/dev/null | grep -q . \
  && echo "FAIL: bundled skill dirs present" || echo "PASS: no bundled skills"
```

The only hidden files that SHOULD appear are `.last_pull` (timestamp) and
`cron/.gitkeep` (empty-dir placeholder).

## 3. README.md quality — PASS/FAIL

Read the README and confirm:

- **Frontmatter** has `title`, `date`, `tags`, `source_repo` (all four required).
- **Source attribution**: the host name (e.g. `zcm6`) appears in frontmatter
  `source_repo`/`source_host` AND in the body.
- **Skill inventory**: a table listing every self-built skill with its file
  count; the row count must equal the actual skill-dir count.
- **Diff vs reference**: documents the differences from the reference (PC)
  version — at minimum: cron empty/Populated, skill count, OS path style
  (Linux vs Windows).
- **Security note**: explicitly lists which sensitive files are excluded.

```bash
README=/path/to/backup/README.md
for f in title date tags source_repo; do
  grep -q "^$f:" "$README" && echo "PASS: frontmatter $f" || echo "FAIL: missing $f"
done
grep -c "zcm6" "$README" >/dev/null && echo "PASS: source mentioned"
# skill table rows (lines starting with "| `")
grep -c "^| \`[a-z]" "$README"
```

## 4. Sync script & timestamp — PASS/FAIL

- `scripts/sync_hermes_config.sh` exists and `diff`s IDENTICAL to the
  reference (PC) version — the script is cross-platform, so content should
  match.
- `.last_pull` exists and contains a parseable timestamp
  (`YYYY-MM-DD HH:MM:SS ±HHMM`).

```bash
diff <backup>/scripts/sync_hermes_config.sh <ref>/scripts/sync_hermes_config.sh \
  && echo "PASS: script identical to ref" || echo "FAIL: script differs"
cat <backup>/.last_pull  # must be non-empty, valid date
```

## 5. Directory structure — PASS/FAIL

Compare the backup's directory tree (depth 2) to the reference. Top-level
must contain: `memories/`, `config/`, `skills/`, `scripts/`, `cron/`,
`.last_pull`, `README.md`. `cron/` may be empty (with `.gitkeep`) if the
source host has no cron jobs — that is expected, not a failure.

```bash
find <backup> -maxdepth 2 -type d | sort
find <ref>   -maxdepth 2 -type d | sort
# diff the two listings structurally (skill count differs by host — that's OK)
```

## 6. Report format

Output a structured report:

- One section per dimension (1–5 above), each with PASS/FAIL/WARN per item.
- For any FAIL, give the exact missing path or diff detail.
- For any WARN, give a recommendation.
- End with an overall verdict: **PASS** or **NEEDS_FIX**.
- If NEEDS_FIX, list the specific fixes required so a work subagent can be
  re-dispatched with precise instructions.

## Pitfalls

- **Don't assume a check passes.** Every PASS must be backed by a real
  `diff`/`find`/`grep` result in the report. A review that says "looks good"
  without tool output is worthless.
- **File-count equality is necessary but not sufficient.** Two dirs with the
  same file count can still differ in content — always pair the count with a
  `diff -rq`.
- **Symlink skills look like directories in `ls`.** Use `find -type l` to
  catch them; `ls -la` shows the `->` arrow but a quick `find` is less
  error-prone.
- **`.bak` files sneak in.** Source `memories/` often has
  `MEMORY.md.<timestamp>.bak` and `*.lock` files — confirm the backup has
  neither.
- **cron empty is not a failure.** If the source host has no cron jobs, an
  empty `cron/` with `.gitkeep` is correct. Only flag it if the source HAS
  jobs and they're missing from the backup.
- **README skill-table count must match actual dirs.** A README claiming
  "14 skills" with only 13 directories on disk is a FAIL even if every
  present directory is correct.
