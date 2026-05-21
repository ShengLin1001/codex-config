# Task Group: Codex local version management and folder continuity

scope: updating Codex binaries under the local versioned directory, documenting the shift to npm-managed versions, and preserving the folder as a continuity/history anchor
applies_to: cwd=/public3/home/scg6928/mysoft/tools/codex; reuse_rule=reuse for follow-up work in this Codex tool directory, but verify the active binary path and whether npm now controls the live version before changing files

## Task 1: Update Codex to 0.131.0 in the versioned local install, success

### rollout_summary_files

- rollout_summaries/2026-05-19T06-19-22-SUKJ-codex_version_updates_and_readme_for_npm_managed_versions.md (cwd=/public3/home/scg6928/mysoft/tools/codex, rollout_path=/public3/home/scg6928/.codex/sessions/2026/05/19/rollout-2026-05-19T14-19-22-019e3ee3-9426-7a93-bd4a-738d52b05251.jsonl, updated_at=2026-05-20T14:04:48+00:00, thread_id=019e3ee3-9426-7a93-bd4a-738d52b05251, validated direct binary refresh with proxy and live-binary replacement gotchas)

### keywords

- codex, codex-cli 0.131.0, versioned directories, rust-v0.131.0, codex-x86_64-unknown-linux-musl.tar.gz, Text file busy, require_escalated

## Task 2: Update Codex to 0.132.0 in a new versioned directory, success

### rollout_summary_files

- rollout_summaries/2026-05-19T06-19-22-SUKJ-codex_version_updates_and_readme_for_npm_managed_versions.md (cwd=/public3/home/scg6928/mysoft/tools/codex, rollout_path=/public3/home/scg6928/.codex/sessions/2026/05/19/rollout-2026-05-19T14-19-22-019e3ee3-9426-7a93-bd4a-738d52b05251.jsonl, updated_at=2026-05-20T14:04:48+00:00, thread_id=019e3ee3-9426-7a93-bd4a-738d52b05251, captures the isolated new-version workflow that preserved 0.131.0)

### keywords

- codex, codex-cli 0.132.0, rust-v0.132.0, sha256sum, 8b64432ee4ef5b1d7d197aad4535a276bc85223f4e4163769c0e1015cda883b2, versioned install

## Task 3: Create Readme.md for npm-managed Codex versions while preserving the folder, success

### rollout_summary_files

- rollout_summaries/2026-05-19T06-19-22-SUKJ-codex_version_updates_and_readme_for_npm_managed_versions.md (cwd=/public3/home/scg6928/mysoft/tools/codex, rollout_path=/public3/home/scg6928/.codex/sessions/2026/05/19/rollout-2026-05-19T14-19-22-019e3ee3-9426-7a93-bd4a-738d52b05251.jsonl, updated_at=2026-05-20T14:04:48+00:00, thread_id=019e3ee3-9426-7a93-bd4a-738d52b05251, documents the npm-era meaning of the folder)

### keywords

- Readme.md, npm, codex version control, historical continuity, preserve folder, manual update no longer default

## User preferences

- when the user said `更新codex到0.131.0` and later `更新到0.132.0` -> for similar Codex upgrade requests, verify the existing local versioned layout first and then do the narrow version update the user asked for, not broader environment work [Task 1][Task 2]
- when the user corrected `不需要你配置PATH` -> do not edit shell startup files or PATH during Codex version updates unless the user explicitly asks [Task 1][Task 2]
- when the user asked `生成一个Readme.md, 现在codex用npm安装来控制版本，而不再使用之前手动update的方式，但是为了强调codex的重要性，及以前session的连续性，仍旧保留这个文件夹` -> treat npm as the preferred Codex version-management path now, but preserve this folder for history and session continuity rather than cleaning it up [Task 3]

## Reusable knowledge

- The local layout already used per-version directories under `/public3/home/scg6928/mysoft/tools/codex/<version>/` with a single `codex` binary inside each version directory; `which codex` initially resolved to `/public3/home/scg6928/mysoft/tools/codex/0.130.0/codex` and `codex --version` returned `codex-cli 0.130.0` [Task 1]
- The Linux x86_64 musl release tarballs used successfully were `rust-v0.131.0/codex-x86_64-unknown-linux-musl.tar.gz` and `rust-v0.132.0/codex-x86_64-unknown-linux-musl.tar.gz`; each archive contained one binary named `codex-x86_64-unknown-linux-musl`, which then had to be renamed to `codex` [Task 1][Task 2]
- For `0.132.0`, the isolated-directory workflow preserved the previous version cleanly: `0.132.0/codex --version` returned `codex-cli 0.132.0` while `0.131.0/codex --version` still returned `codex-cli 0.131.0` [Task 2]
- The created `/public3/home/scg6928/mysoft/tools/codex/Readme.md` intentionally says Codex versions are now managed by npm instead of manual download/extract/replace updates, while the folder remains as a continuity/history anchor [Task 3]

## Failures and how to do differently

- Symptom: `curl` to GitHub releases fails with `couldn't connect to proxy at 127.0.0.1:37897`. Cause: sandboxed network path is blocked. Fix: use the network-enabled path earlier when fetching release artifacts instead of retrying plain `curl` repeatedly [Task 1]
- Symptom: replacing the live binary in-place fails with `cp: cannot create regular file ...: Text file busy`. Cause: the currently used binary is still open. Fix: write to a temp file and atomically `mv -f` it into place [Task 1]
- Symptom: temptation to keep doing manual version refreshes in this directory. Cause: older workflow inertia. Fix: remember the newer validated guidance: npm controls Codex versioning now; only keep the old folder for history/continuity unless the user explicitly wants manual binary work there again [Task 3]

# Task Group: HPC user-space nvm and Node installation

scope: installing and repairing nvm plus a working Node/npm/npx stack without root on this old CentOS-like HPC host, including the final standard nvm layout and shell-loading gotchas
applies_to: cwd=/public3/home/scg6928/mysoft/tools/nvm; reuse_rule=reuse for similar no-root Node setup on this host, but re-check glibc/libstdc++ compatibility, proxy behavior, and the current nvm directory layout before applying exact paths

## Task 1: Install nvm 0.40.4 and a compatible Node version for npm/npx, success

### rollout_summary_files

- rollout_summaries/2026-05-19T08-51-31-FxpH-nvm_user_space_install_and_relayout.md (cwd=/public3/home/scg6928/mysoft/tools/nvm, rollout_path=/public3/home/scg6928/.codex/sessions/2026/05/19/rollout-2026-05-19T16-51-31-019e3f6e-e0ed-7ca1-8383-a98f91e971c5.jsonl, updated_at=2026-05-20T13:48:11+00:00, thread_id=019e3f6e-e0ed-7ca1-8383-a98f91e971c5, validated Node compatibility and no-root install path)

### keywords

- nvm, node, npm, npx, glibc 2.17, GLIBC_2.27 not found, GLIBCXX_3.4.20 not found, NVM_NODEJS_ORG_MIRROR, node v16.20.2

## Task 2: Reorganize and reinstall using the standard nvm layout rooted at `nvm/0.40.4/`, success

### rollout_summary_files

- rollout_summaries/2026-05-19T08-51-31-FxpH-nvm_user_space_install_and_relayout.md (cwd=/public3/home/scg6928/mysoft/tools/nvm, rollout_path=/public3/home/scg6928/.codex/sessions/2026/05/19/rollout-2026-05-19T16-51-31-019e3f6e-e0ed-7ca1-8383-a98f91e971c5.jsonl, updated_at=2026-05-20T13:48:11+00:00, thread_id=019e3f6e-e0ed-7ca1-8383-a98f91e971c5, final stable layout after reversing the earlier custom Node relocation)

### keywords

- 0.40.4, versions/node/v16.20.2, load-nvm.sh, NVM_DIR, source ~/.bashrc, non-interactive shell, downloads, standard nvm layout

## User preferences

- when the user said “我想使用npx安装skills，但是我没有管理员权限安装node.js,gpt推荐我安装nvm” -> default to a user-space Node solution, not sudo or system-package instructions, for similar HPC tooling tasks [Task 1]
- when the user objected that files were “非常的乱” -> separate install archives and temporary build artifacts from the installed tool tree instead of leaving files scattered in the tool root [Task 2]
- when the user corrected the earlier custom relocation and said “不要把node移出原本的目录，这是我的失误，我希望按照原本的目录格式组织。nvm/0.40.4/作为根目录” -> use the standard nvm layout by default on follow-up work here, not a custom sibling `tools/node` layout [Task 2]
- when the user accepted persistent shell integration, treat automatic availability in future shells as part of the job, not an optional extra [Task 1][Task 2]

## Reusable knowledge

- This host is old enough that modern official Node binaries can install but not run: the validated compatibility check was `ldd (GNU libc) 2.17`, and Node `v24.15.0` failed on missing `GLIBC_2.25+`, `GLIBC_2.27+`, and `GLIBCXX_3.4.20+` symbols [Task 1]
- Node `v16.20.2` is a known-good version here and produced working `npm 8.19.4` and `npx 8.19.4` through nvm [Task 1]
- `http://nodejs.org/dist/` was reachable when HTTPS/proxying was flaky; the validated install path was `NVM_NODEJS_ORG_MIRROR=http://nodejs.org/dist nvm install 16.20.2` [Task 1]
- The final stable layout is `/public3/home/scg6928/mysoft/tools/nvm/0.40.4/` as the nvm root, `/public3/home/scg6928/mysoft/tools/nvm/0.40.4/versions/node/v16.20.2/` as the Node version path, `/public3/home/scg6928/mysoft/tools/nvm/downloads/nvm-0.40.4.tar.gz` as the saved archive, and `/public3/home/scg6928/mysoft/tools/nvm/load-nvm.sh` as the loader [Task 2]
- `load-nvm.sh` should set `NVM_DIR=/public3/home/scg6928/mysoft/tools/nvm/0.40.4`; `readlink -f $(which node)` should resolve into `.../tools/nvm/0.40.4/versions/node/v16.20.2/bin/node` when the loader is active [Task 1][Task 2]

## Failures and how to do differently

- Symptom: latest Node installs but `node` fails immediately with `GLIBC_*` or `GLIBCXX_*` missing. Cause: host ABI is too old for current official binaries. Fix: do the runtime compatibility check first and pick a version already validated on `glibc 2.17`; here `16.20.2` worked [Task 1]
- Symptom: `source ~/.bashrc` returns successfully but `npm` is still missing. Cause: `.bashrc` exits early in non-interactive shells, so the nvm loader never runs. Fix: source the actual loader or test in an interactive shell instead of assuming `.bashrc` is enough [Task 2]
- Symptom: commands start failing with `No such file or directory` after the user deletes the working tree mid-run. Cause: the bound cwd no longer exists. Fix: switch to a valid cwd such as `/tmp` before continuing recovery work [Task 2]
- Symptom: drift toward a custom `tools/node` relocation. Cause: an earlier experimental reorg. Fix: preserve the user-corrected standard nvm tree unless they explicitly request a nonstandard layout again [Task 2]

# Task Group: Codex bubblewrap compatibility and workspace-relative path debugging

scope: building a compatible bubblewrap for Codex on this CentOS 7 host, fixing PATH placement, and explaining the directory-dependent warning behavior
applies_to: cwd=/public3/home/scg6928/mysoft/tools/bubblewrap and Codex launches from sibling workspaces; reuse_rule=reuse for Codex sandbox troubleshooting on this host, but re-check Codex version requirements and the actual location of the chosen `bwrap` binary

## Task 1: Install and validate bubblewrap 0.11.0 for Codex, success

### rollout_summary_files

- rollout_summaries/2026-05-19T02-08-17-crke-codex_bubblewrap_path_root_cause_and_github_comment.md (cwd=/public3/home/scg6928/mysoft/tools/bubblewrap, rollout_path=/public3/home/scg6928/.codex/sessions/2026/05/19/rollout-2026-05-19T10-08-17-019e3dfd-b62a-7610-aeea-9f05fb2fe7c2.jsonl, updated_at=2026-05-20T07:32:35+00:00, thread_id=019e3dfd-b62a-7610-aeea-9f05fb2fe7c2, validated build path and PATH placement for a supported `bwrap`)

### keywords

- bubblewrap, bwrap, --argv0, bubblewrap 0.11.0, CentOS 7, libcap-devel, meson, ninja, .bash_soft_env, digest mismatch

## Task 2: Explain directory-dependent Codex warning behavior and post the root cause to GitHub issue `#15282`, success

### rollout_summary_files

- rollout_summaries/2026-05-19T02-08-17-crke-codex_bubblewrap_path_root_cause_and_github_comment.md (cwd=/public3/home/scg6928/mysoft/tools/bubblewrap, rollout_path=/public3/home/scg6928/.codex/sessions/2026/05/19/rollout-2026-05-19T10-08-17-019e3dfd-b62a-7610-aeea-9f05fb2fe7c2.jsonl, updated_at=2026-05-20T07:32:35+00:00, thread_id=019e3dfd-b62a-7610-aeea-9f05fb2fe7c2, root-cause explanation was shared externally)

### keywords

- openai/codex#15282, workspace-local bwrap, PATH, launch directory, ~/.local/bin/bwrap, comment ID 4495738175

## User preferences

- when the user kept steering away from wrapper-script-only fixes and pointed to `.bash_soft_env` -> prefer a durable PATH/startup-file fix over ad-hoc launch wrappers for shell-visible tooling problems [Task 1]
- when the user asked for the final reason “用英文描述一下，或者帮我发布在这里” on the GitHub issue -> after root cause is clear, provide a concise reusable explanation suitable for external sharing instead of only local workaround notes [Task 2]

## Reusable knowledge

- On this CentOS 7 host, the EPEL `bubblewrap-0.3.0` package was too old for Codex 0.130.0; `bubblewrap 0.11.0` was sufficient and `bwrap --help | grep argv0` was the useful compatibility check because Codex needed `--argv0` support [Task 1]
- Building `0.11.0` worked with locally installed `meson` and `ninja` plus a locally unpacked `libcap-devel` RPM used as the header/library source; creating `deps/libcap-devel/usr/lib64/libcap.so.2 -> /lib64/libcap.so.2` unblocked linking [Task 1]
- The validated local install path was `/public3/home/scg6928/mysoft/tools/bubblewrap/0.11.0/bin/bwrap`, and the shell config file that actually mattered was `/public3/home/scg6928/.bash_soft_env` [Task 1]
- The key diagnostic result was directory-dependent startup: the warning did not appear from `/public3/home/scg6928/mysoft/tools/codex`, but did appear from `/public3/home/scg6928/mysoft`, even though `bwrap --version` reported `bubblewrap 0.11.0` in both places [Task 2]
- The best current explanation is that Codex rejects a `bwrap` binary located inside the current workspace/sandbox root; placing `bwrap` outside the workspace, such as `~/.local/bin/bwrap`, avoids the warning [Task 2]

## Failures and how to do differently

- Symptom: Codex still warns after `bwrap` is installed and on PATH. Cause: package presence or plain PATH visibility is not enough. Fix: verify required flags like `--argv0` and ensure the usable `bwrap` is outside the current workspace root [Task 1][Task 2]
- Symptom: trying to replace Codex’s bundled `codex-resources/bwrap` causes a digest mismatch. Cause: Codex checks a hard-coded bundled-bwrap SHA256. Fix: do not substitute the bundled file; use an external `bwrap` on PATH instead [Task 1]
- Symptom: wrapper scripts appear to help but the warning remains directory-dependent. Cause: the real rule is workspace-relative helper rejection, not simple shell resolution. Fix: investigate launch context and helper placement before inventing more wrappers [Task 2]

# Task Group: Local Git v2.54.0 build on old HPC toolchain

scope: attempting to compile Git v2.54.0 under the current working directory and add its bin path to `.bash_soft_env`, including the validated blockers from old headers and old libcurl
applies_to: cwd=/public3/home/scg6928/mysoft/tools/git; reuse_rule=reuse for follow-up work in this Git source tree or similar local builds on the same host, but re-validate module state and whether the interrupted install ever completed

## Task 1: Local Git v2.54.0 install and `.bash_soft_env` update, partial

### rollout_summary_files

- rollout_summaries/2026-05-19T08-21-35-pNJO-git_v2_54_0_local_install_bash_soft_env.md (cwd=/public3/home/scg6928/mysoft/tools/git, rollout_path=/public3/home/scg6928/.codex/sessions/2026/05/19/rollout-2026-05-19T16-21-35-019e3f53-7780-7d02-8fa7-3b264ec092a4.jsonl, updated_at=2026-05-19T08:29:58+00:00, thread_id=019e3f53-7780-7d02-8fa7-3b264ec092a4, partial run with validated blockers and next step)

### keywords

- git v2.54.0, .bash_soft_env, curl 7.61.0, libcurl 7.29.0, sys/random.h, CSPRNG_METHOD=openssl, module load curl, local install

## Task 2: Interrupted continuation state, uncertain

### rollout_summary_files

- rollout_summaries/2026-05-19T08-21-35-pNJO-git_v2_54_0_local_install_bash_soft_env.md (cwd=/public3/home/scg6928/mysoft/tools/git, rollout_path=/public3/home/scg6928/.codex/sessions/2026/05/19/rollout-2026-05-19T16-21-35-019e3f53-7780-7d02-8fa7-3b264ec092a4.jsonl, updated_at=2026-05-19T08:29:58+00:00, thread_id=019e3f53-7780-7d02-8fa7-3b264ec092a4, interrupted before final rebuild and validation)

### keywords

- turn_aborted, pending continuation, verify final artifacts, local prefix, git source tree, partial build

## User preferences

- when the user said “在当前目录下安装一个git” -> similar install tasks should default to a local prefix inside the working directory rather than a system-wide install [Task 1]
- when the user said “将其的bin文件添加到.bash_soft_env中，按照文件内容的格式” -> inspect the existing `.bash_soft_env` style and add PATH lines in the same export format instead of appending arbitrary shell syntax [Task 1]
- when the user pinned GitHub release `v2.54.0` -> treat the version as fixed unless the user asks to change it [Task 1]
- because the previous rollout was intentionally interrupted, do not assume completion on a follow-up run; re-check the prefix, binary presence, and `.bash_soft_env` state before reporting success [Task 2]

## Reusable knowledge

- `rg` is not installed in this environment; use `find`, `grep`, and `sed` as the default text/file discovery tools on this host [Task 1]
- The baseline toolchain was old: system `git 1.8.3.1`, `gcc 4.8.5`, `make 3.82`, `curl 7.29.0`, `perl 5.16.3`. That mattered because Git 2.54.0 ran into both header and libcurl API age issues [Task 1]
- Git 2.54.0 first failed at `compat/posix.h:159` because `sys/random.h` was missing; rebuilding with `CSPRNG_METHOD=openssl` got past that host-header problem [Task 1]
- The next validated blocker was old system `libcurl 7.29.0`: compile errors in `http.c` referenced `CURLOPT_PROXYHEADER`, `CURL_HTTP_VERSION_2`, `CURLOPT_PINNEDPUBLICKEY`, `CURLSSLSET_*`, and `CURLE_SSL_PINNEDPUBKEYNOTMATCH` [Task 1]
- `module avail curl` exposed `curl/7.61.0`, and after loading it the host reported `libcurl/7.61.0 OpenSSL/1.0.2k`; that module is the validated next step for any continuation build [Task 1]
- `.bash_soft_env` lives at `/public3/home/scg6928/.bash_soft_env` and already uses direct `export PATH=...:$PATH` lines in its software section; any Git bin export should match that shape [Task 1]

## Failures and how to do differently

- Symptom: source download fails through proxy `127.0.0.1:37897`. Cause: default proxy path is unreachable. Fix: switch quickly to a path with working network access or have the user provide the tarball instead of assuming a source/version problem [Task 1]
- Symptom: build stops with `fatal error: sys/random.h: No such file or directory`. Cause: this old Linux header set does not support the default getrandom-based CSPRNG path. Fix: rebuild with `CSPRNG_METHOD=openssl` [Task 1]
- Symptom: build later fails in `http.c` on missing `CURLOPT_*`, `CURL_HTTP_VERSION_2`, or `curl_ssl_backend`. Cause: the system `libcurl 7.29.0` is too old for Git 2.54.0. Fix: load `module load curl/7.61.0` before rebuilding so compile and link use newer curl headers and libraries [Task 1]
- Symptom: uncertain end state after interruption. Cause: the rollout was aborted mid-investigation. Fix: before resuming, validate whether `/public3/home/scg6928/mysoft/tools/git/2.54.0/bin/git` exists and whether `.bash_soft_env` was updated; only then decide whether to rebuild or just finalize PATH wiring [Task 2]

# Task Group: Codex session artifact restore

scope: restoring archived Codex rollout JSONL files back into the active sessions tree with exact-path validation
applies_to: cwd=/public3/home/scg6928/mywork and `/public3/home/scg6928/.codex`; reuse_rule=reuse for similar archived-session recovery tasks, but always confirm the exact archive filename and date-based destination path first

## Task 1: Restore archived session JSONL into the active sessions tree, success

### rollout_summary_files

- rollout_summaries/2026-05-19T06-56-30-0Yov-restore_archived_codex_session_jsonl.md (cwd=/public3/home/scg6928/mywork, rollout_path=/public3/home/scg6928/.codex/archived_sessions/rollout-2026-05-19T14-56-30-019e3f05-9403-70c0-9b61-b0e3b2cdbf8f.jsonl, updated_at=2026-05-19T07:01:18+00:00, thread_id=019e3f05-9403-70c0-9b61-b0e3b2cdbf8f, validated exact-file restore with byte-for-byte verification)

### keywords

- archived_sessions, sessions, jsonl, session_index.jsonl, history.jsonl, Read-only file system, cp, cmp -s, restore archived session

## User preferences

- when the user said “帮我把归档的对话复原，他的位置在 ...” -> treat similar requests as exact file-recovery tasks and identify the precise active destination before writing anything [Task 1]
- when the task is a direct Codex artifact restore, avoid drifting into unrelated environment setup or PATH work [Task 1]

## Reusable knowledge

- The active session file path should mirror the archived filename under `/public3/home/scg6928/.codex/sessions/YYYY/MM/DD/` [Task 1]
- `session_index.jsonl` and `history.jsonl` are useful for confirming the session is still referenced and for locating the restoration target [Task 1]
- Cheap validation that worked here was `ls -l` for existence, `wc -l` for size parity, and `cmp -s` for byte-for-byte identity [Task 1]

## Failures and how to do differently

- Symptom: `cp` into `.codex/sessions` fails with `Read-only file system`. Cause: the active sessions tree may be mounted read-only for ordinary writes. Fix: retry the same exact-file copy with elevated write permissions; no content rewrite is needed [Task 1]

# Task Group: Codex skill install blocked by missing Node tooling

scope: installing a Codex skill from GitHub when the user requests an `npx skills add ...` flow, but the host lacks Node/npm/npx and modern Git partial-clone support
applies_to: cwd=/public3/home/scg6928 and Codex skill installation workflows on this host; reuse_rule=reuse when the user asks for skill installation on this machine, but re-check whether Node/npm/npx or newer Git have been installed since this rollout

## Task 1: Attempt to install `K-Dense-AI/scientific-agent-skills`, partial

### rollout_summary_files

- rollout_summaries/2026-05-19T08-11-27-MbxC-install_codex_skill_github_fallback_node_missing.md (cwd=/public3/home/scg6928, rollout_path=/public3/home/scg6928/.codex/archived_sessions/rollout-2026-05-19T16-11-27-019e3f4a-2fbe-7d82-a450-4d4eb1b68060.jsonl, updated_at=2026-05-19T08:19:03+00:00, thread_id=019e3f4a-2fbe-7d82-a450-4d4eb1b68060, partial run with clear environment blockers and fallback directions)

### keywords

- npx skills add, K-Dense-AI/scientific-agent-skills, node, npm, npx: command not found, skill-installer, install-skill-from-github.py, filter=blob:none

## User preferences

- when the user asks for a specific install command like `npx skills add K-Dense-AI/scientific-agent-skills` -> try the requested install shape first and only pivot when the environment blocks it [Task 1]
- when the user frames it as a direct install request rather than a discussion -> optimize for getting the skill installed instead of spending time over-explaining first [Task 1]

## Reusable knowledge

- `npx` is not available here unless Node tooling is installed or loaded first; `command -v node`, `command -v npm`, and `command -v npx` all returned nothing in this rollout [Task 1]
- `.bash_soft_env` already added Codex CLI to PATH (`/public3/home/scg6928/mysoft/tools/codex/0.131.0`) but did not provide Node/npm/npx [Task 1]
- The local skill installer docs at `/public3/home/scg6928/.codex/skills/.system/skill-installer/SKILL.md` and script `/public3/home/scg6928/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py` were the authoritative local references for GitHub-repo skill installation and `SKILL.md` validation [Task 1]
- The installed Git on this host was too old for `git clone --filter=blob:none ...`, so future fallbacks should use plain clone, a GitHub zip download, or another non-partial path [Task 1]

## Failures and how to do differently

- Symptom: `npx skills add ...` fails immediately with `/usr/bin/bash: npx: command not found`. Cause: Node tooling is absent from PATH. Fix: check `node/npm/npx` availability first on this host and install or load Node before retrying the `npx` path [Task 1]
- Symptom: a Git fallback fails with `error: unknown option \`filter=blob:none\``. Cause: the host Git is too old for partial-clone flags. Fix: avoid partial-clone assumptions and use a plain clone or zip-download fallback instead [Task 1]
- Symptom: install remains incomplete after environment diagnosis. Cause: the turn was interrupted before the manual-download fallback ran. Fix: on a continuation, skip straight to a compatible fallback path after confirming whether Node has since been installed [Task 1]
