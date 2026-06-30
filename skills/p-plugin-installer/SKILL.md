---
name: p-plugin-installer
description: Install or repair a plugin marketplace for BOTH Codex and Claude Code on Windows, especially when `plugin marketplace add owner/repo` fails with EPERM or "Access is denied" during the clone-to-final rename. Use for third-party marketplace installs such as Ponytail, no-rename recovery, plugin cache/state consistency checks, and deciding whether to use the product CLI or edit known_marketplaces.json / installed_plugins.json / settings.json (Claude) or config.toml (Codex) after inspecting the live product state.
---

# P Plugin Installer

One skill, two products. The EPERM failure, the root cause, and the no-rename
recovery are shared; only the place where state is recorded differs between
Codex and Claude Code.

## Core principles (both products)

- A plugin install is **product-specific state repair**, not a generic file copy.
- Two products, **separate state**. Never assume Codex and Claude Code share
  plugin files or install records.
  - Claude Code: JSON files under the Claude plugin home
    (`known_marketplaces.json`, `installed_plugins.json`, `settings.json`)
    plus a marketplace checkout and a cache dir.
  - Codex: `~/.codex/config.toml` (`[marketplaces.*]`, `[plugins."x@y"]`)
    plus `~/.codex/marketplaces/<name>` and `~/.codex/plugins/cache/...`.
- Always **read the live product files** (or run the product's list command)
  before editing any state.
- The plugin repo is usually **multi-tool**: read the manifest for *your*
  product and do not cross them — `.claude-plugin/` for Claude Code,
  `.codex-plugin/` for Codex. The shared marketplace manifest is normally
  `.claude-plugin/marketplace.json` even in repos that also ship `.codex-plugin/`.

## Environment notes (this Windows box)

- `git` may not be on the PowerShell PATH. Use the Git Bash tool for git work
  (`clone`, `archive`, `rev-parse`, `remote -v`).
- Use a real JSON parser, never regex, for JSON state. PowerShell
  `ConvertFrom-Json` / `ConvertTo-Json` or `jq` work on the product state files.
  Exception: `.claude.json` itself can contain duplicate keys (case-variant
  paths) and `ConvertFrom-Json` then throws `DuplicateKeysInJsonString`; fall
  back to Python's `json` module if you must parse it. You normally do **not**
  need to touch `.claude.json` for plugin state.

## Why it fails and the shared fix

The CLI installs a marketplace by cloning to a staging name and then
**renaming** it to the final marketplace name. On Windows that rename can fail
with `EPERM` / "Access is denied" (transient AV / indexer / file lock). The
rolled-back attempt usually leaves nothing behind.

The fix for both products: **do the clone yourself, directly at the final path,
so there is no rename.** Then hand off to the product CLI (preferred) or record
state manually.

Do not just keep retrying the same failing `plugin marketplace add`.

## Shared no-rename recovery workflow

1. Capture the exact failing command and error; confirm the failure stage
   (clone / rename / cache / state record).
2. Discover real names from the cloned repo manifest — **do not hard-code**:
   - marketplace name + plugin list: `.claude-plugin/marketplace.json`; the
     `name` field is the final dir name the rename was targeting.
   - plugin name / version / hooks: `.claude-plugin/plugin.json` (Claude) or
     `.codex-plugin/plugin.json` (Codex).
   - revision: `git rev-parse HEAD`.
3. Clone **directly** into the product's final marketplace path (no staging,
   no rename). Keep it a **full clone** with an `origin` remote and an upstream
   tracking branch, so future updates run `git pull` in place — which avoids the
   rename and never re-hits EPERM.
4. Record state: prefer the product CLI (Codex), or write the state files
   manually (Claude). See the per-product sections.
5. Enable the plugin.
6. Run the validation checklist.
7. If the product loads plugins only at startup, tell the user to restart it.

## Codex recovery

Prefer the CLI so Codex owns its own state and cache:

1. Clone to a stable final path, e.g. `~/.codex/marketplaces/<name>`.
2. `codex plugin marketplace add <that-local-path>` → registers
   `[marketplaces.<name>]` with `source_type = "local"` and `source = <path>`
   (Windows may store it with a `\\?\` long-path prefix).
3. `codex plugin add <plugin>@<marketplace>`.
4. `codex plugin list` should show the plugin installed and enabled.

Codex's own install keeps `.git` inside
`~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/`. That is expected for
Codex — do not strip it.

If the codex CLI is not reachable, edit `~/.codex/config.toml` manually, only
after reading the current schema:

- add `[marketplaces.<name>]` (`last_updated`, `source_type`, `source`; git
  sources also carry `last_revision`),
- add `[plugins."<plugin>@<marketplace>"]` with `enabled = true`,
- preserve all existing marketplaces, plugins, hooks, and project settings.

## Claude Code recovery

There is no add-from-local-path CLI step here, so record state manually after
reading the live schema. Files under the Claude plugin home:

- `known_marketplaces.json` — `"<name>": { "source": { "source": "github",
  "repo": "owner/repo" }, "installLocation": ..., "lastUpdated": ... }`
- `installed_plugins.json` — `plugins["<plugin>@<marketplace>"] = [{ scope,
  installPath, version, installedAt, lastUpdated, gitCommitSha }]`
- `settings.json` — `enabledPlugins["<plugin>@<marketplace>"] = true`
- checkout: `marketplaces/<name>`; cache: `cache/<name>/<plugin>/<version>`

Steps:

1. Clone directly to `marketplaces/<name>` (full clone, keep `origin`).
2. Populate the cache with a clean tree:
   `git archive HEAD | tar -x -C cache/<name>/<plugin>/<version>` so the cache
   has **no** `.git`. This matches how Claude Code's CLI caches, and is the
   opposite of Codex, whose cache keeps `.git`.
3. Create the `.in_use` marker if other cache entries have one. It is a
   **directory** of per-PID files, and is optional — what actually protects the
   cache from the in-use GC sweep is the `installed_plugins.json` entry.
4. Register the marketplace, record the installed plugin, and enable it, using a
   JSON parser (not regex).

## Validation checklist

Run every check that applies to the target product:

1. Marketplace state points to the final, non-staging path.
2. Marketplace checkout exists and has the expected `origin` remote **and** an
   upstream tracking branch, so updates can `git pull`.
3. The manifest for the correct product exists; the recorded version matches it.
4. Cache path exists and has plugin files. Claude Code cache has **no** `.git`;
   the Codex CLI cache may keep `.git`.
5. Installed-plugin state records the expected id, version, and revision.
6. Enabled state contains the id and is true (Claude `settings.json` /
   Codex `config.toml`).
7. The product's list/status command shows the plugin installed and enabled,
   when such a command exists.
8. Hooks or commands that need Node are flagged as dependent on `node` being on
   `PATH`.

If a check fails, fix only that layer. Do not perform broad cleanup.

## Updates after recovery

Updates do **not** re-trigger the rename, so they are safer than the first add:

- Codex: `codex plugin marketplace update <name>` or startup refresh. A git
  source pulls itself; a **local** source re-reads the checkout, so `git pull`
  the checkout first.
- Claude Code: `/plugin marketplace update <name>` or startup refresh →
  `git pull` in the checkout, then re-cache the new version.

Removing and re-adding a marketplace **will** go through clone+rename again, so
avoid that path.

## Safety

- Do not bulk delete marketplace, cache, or plugin directories.
- If a stale directory must be removed, remove at most one explicit file path;
  otherwise stop and ask the user to delete it manually.
- Do not edit product state until after reading the current schema.
- Do not assume Codex and Claude Code share plugin files or install records.
- If the product schema looks changed, prefer the product CLI or hand back a
  precise report instead of guessing.
