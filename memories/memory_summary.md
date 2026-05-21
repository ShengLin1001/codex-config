v1

## User Profile

The user works on a CentOS-like HPC environment without root and uses Codex heavily for local tooling, environment repair, and Codex-specific maintenance under `/public3/home/scg6928/mysoft/tools` and `/public3/home/scg6928/.codex`. They prefer direct execution over discussion when the request is operational: install the tool, restore the file, update the version, or trace the root cause. They repeatedly push for durable fixes that match existing shell conventions, especially edits through `/public3/home/scg6928/.bash_soft_env` rather than ad-hoc wrappers.

They care about exact versions, exact paths, and filesystem hygiene. Repeated signals: keep installs local to the requested directory, preserve prior continuity/history when asked, separate downloads/build artifacts from installed software, and validate the real end state instead of assuming success. They also expect environment-aware behavior on this host: no sudo assumptions, `module avail` checks when tooling is missing or too old, and fast pivots when proxies, old glibc/libcurl, or read-only paths block the first approach.

## User preferences

- For install/update requests, do the requested operation directly first; avoid plan-heavy discussion unless blocked.
- When the user says `不需要你配置PATH`, do not touch shell startup files or PATH for that task family unless asked again.
- For local software installs “在当前目录下”, prefer a local prefix in the working directory, not a system-wide install.
- When editing `/public3/home/scg6928/.bash_soft_env`, preserve its existing export/source style instead of inventing new shell patterns.
- On this HPC host, default to user-space installers and runnable local toolchains, not sudo or OS-package instructions.
- If the user provides or can provide local artifacts, pivot early to offline/local-package workflows instead of burning time on flaky network access.
- Keep tool directories tidy: separate downloads and temporary build artifacts from the installed runtime.
- For this nvm workspace, prefer the standard layout the user corrected to: `nvm/0.40.4/` as root with Node under `versions/node/...`.
- For exact file-recovery tasks, identify the precise destination first and avoid unrelated environment work.
- When a previous run was interrupted, re-check the actual filesystem state before claiming anything finished.

## General Tips

- This host may lack `rg`; use `find`, `grep`, and `sed`, and check `module avail` before assuming a toolchain dead end.
- Runtime ABI is a frequent blocker. Check `ldd --version` and relevant `GLIBC`/`GLIBCXX` requirements before choosing Node or similar binaries.
- Proxy/network failures are common. Good fallback order here: local artifact, cluster module, alternate mirror/protocol, then broader workaround.
- Verification should be concrete and tool-specific: `node -v`/`npm -v`/`npx -v`, `codex --version`, exact file presence plus `cmp -s`, or targeted binary/path checks.
- Avoid broad cluster-wide filesystem scans unless necessary; narrow the search path early to reduce permission noise and wasted time.
- For Codex sandbox issues, ordinary PATH visibility is not enough; launch context and whether helper binaries live inside the workspace can matter.

## What's in Memory

### /public3/home/scg6928/mysoft/tools/codex

#### 2026-05-20

- Codex versioned binary updates and npm-era README: codex-cli 0.131.0, codex-cli 0.132.0, Readme.md, rust-v0.132.0, Text file busy
  - desc: Search this first for follow-up work in `cwd=/public3/home/scg6928/mysoft/tools/codex`, especially version refreshes, manual tarball installs, or questions about why the folder still exists now that npm manages versions.
  - learnings: Manual binary refreshes worked through per-version directories, but the durable guidance changed: npm now controls Codex versions; preserve the folder for continuity/history and avoid PATH edits unless asked.

### /public3/home/scg6928/mysoft/tools/nvm

#### 2026-05-20

- nvm + Node user-space install on old glibc host: nvm, node v16.20.2, npm, npx, glibc 2.17, NVM_NODEJS_ORG_MIRROR
  - desc: Covers no-root Node setup in `cwd=/public3/home/scg6928/mysoft/tools/nvm`, including version compatibility, flaky proxy behavior, and the final working install path.
  - learnings: Node 24 was too new for this host ABI; `16.20.2` is the validated fallback. `source ~/.bashrc` is not a reliable validation step in non-interactive shells because `.bashrc` returns early.

### /public3/home/scg6928/mysoft/tools/bubblewrap

#### 2026-05-20

- Codex bubblewrap warning root cause and external explanation: bubblewrap 0.11.0, --argv0, workspace-local bwrap, openai/codex#15282, ~/.local/bin/bwrap
  - desc: Covers building a supported `bwrap`, wiring PATH through `.bash_soft_env`, and diagnosing why Codex still warned in some launch directories.
  - learnings: The critical behavior was workspace-relative helper rejection, not plain PATH failure. Keep the accepted `bwrap` outside the active workspace and verify `--argv0` support.

### Older Memory Topics

#### /public3/home/scg6928/mysoft/tools/git

- Local Git v2.54.0 build blockers: git v2.54.0, CSPRNG_METHOD=openssl, libcurl 7.29.0, curl/7.61.0, .bash_soft_env
  - desc: Partial local build memory for `cwd=/public3/home/scg6928/mysoft/tools/git`; use it when resuming the Git install or diagnosing why Git 2.54.0 would not compile on this host.

#### /public3/home/scg6928/mywork and /public3/home/scg6928/.codex

- Restore archived Codex session JSONL: archived_sessions, sessions, session_index.jsonl, history.jsonl, cmp -s
  - desc: Exact-file recovery workflow for restoring archived rollout JSONL files back into `.codex/sessions/YYYY/MM/DD/`, including the read-only write failure and byte-for-byte verification path.

#### /public3/home/scg6928

- Codex skill install blocked by missing Node tooling: npx skills add, K-Dense-AI/scientific-agent-skills, npx: command not found, filter=blob:none
  - desc: Search this when the user asks to install a Codex skill on this host and the requested `npx` flow or modern Git sparse-clone flow fails because Node or newer Git is missing.
