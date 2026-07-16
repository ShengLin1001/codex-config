---
name: p-pdf-nature-downloader
description: Use when the user wants to download PDFs from a DOI list through the nature-downloader skill, a logged-in Chrome library/CARSI session, and the web-access CDP proxy, especially when they explicitly say not to use scansci-pdf.
---

# P PDF Nature Downloader

## Overview

This is PJ's thin, practical wrapper around `nature-downloader` for authorized PDF downloading from DOI lists. It preserves the user's `dois_row.txt` layout, uses the user's logged-in Chrome/CARSI session through `web-access`, records partial failures, and verifies every downloaded PDF before reporting success.

Use this skill when the user says they want to use `nature-downloader`, `nature downloader 插件`, Chrome/CARSI, or `web-access` to download PDFs. Do not use `scansci-pdf` in this workflow unless the user explicitly changes the tool boundary.

## Boundaries

- Use only legitimate open-access or institution-authorized routes.
- Never ask for, inspect, export, or store passwords, cookies, tokens, Chrome profiles, local storage, OTPs, or recovery codes.
- Do not bypass CAPTCHA, Cloudflare, "Are you a robot?", publisher bot checks, DRM, paywalls, or two-factor authentication.
- If an institutional login, CARSI handoff, CAPTCHA, Cloudflare, or publisher verification appears, stop and let the user complete it in Chrome.
- Keep batches small. For ordinary use, 5-10 DOIs is the comfortable range.
- Download main PDFs by default. Do not download supporting information unless the user asks for SI/supplementary files.

## Inputs

Default input is a DOI file, usually named:

```text
dois_row.txt
```

Supported row formats:

```text
10.xxxx/yyyy
10.xxxx/yyyy<TAB>paper_folder_name
10.xxxx/yyyy    paper_folder_name
```

Treat the first whitespace-separated token as the DOI. Treat the remaining text, if present, as the target subfolder name. Use the directory containing `dois_row.txt` as the project root unless the user explicitly gives another output path.

## Preconditions

Before downloading, verify these items:

1. Read the installed `nature-downloader` skill instructions if available:

```powershell
Get-Content -LiteralPath "$env:USERPROFILE\.agents\skills\nature-downloader\SKILL.md" -Encoding UTF8
```

2. Confirm the school config exists:

```powershell
$nd = "$env:USERPROFILE\.agents\skills\nature-downloader"
python "$nd\scripts\configure_school.py" show
```

If missing, configure the user's real library resource URL first. Do not invent a school preset when the user has provided a live library resource entry.

3. Confirm Chrome is logged in by the user through the library/CARSI route and can reach Web of Science or the target publisher with a full-text route.

4. Confirm Chrome remote debugging is enabled for the current browser instance at:

```text
chrome://inspect/#remote-debugging
```

5. Confirm the `web-access` CDP proxy is running:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:3456/health" -TimeoutSec 10
Invoke-RestMethod -Uri "http://127.0.0.1:3456/targets" -TimeoutSec 10
```

If the proxy is not running, start it from an available `web-access` checkout:

```powershell
$node = "node"
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
  $node = "$env:LOCALAPPDATA\OpenAI\Codex\bin\node.exe"
}

$checkDepsCandidates = @(
  "$env:USERPROFILE\.agents\skills\web-access\scripts\check-deps.mjs",
  "$env:USERPROFILE\.agents\skills\web-access-main\scripts\check-deps.mjs",
  "$env:USERPROFILE\.claude\skills\web-access-main\scripts\check-deps.mjs",
  "$env:USERPROFILE\.codex\skills\web-access-main\scripts\check-deps.mjs",
  "$PWD\work\web-access-tree\scripts\check-deps.mjs"
)
$checkDeps = $checkDepsCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $checkDeps) {
  throw "web-access check-deps.mjs not found; install/clone eze-is/web-access, then rerun from its scripts/check-deps.mjs"
}
& $node $checkDeps --browser chrome
```

The `skills` CLI may install only `web-access/SKILL.md` without scripts. That is not enough to start the proxy; use an existing checkout or clone `eze-is/web-access` into a work directory, then run its `scripts/check-deps.mjs`.

## Batch Download

Parse the DOI list and run the `nature-downloader` batch script:

```powershell
$doiFile = "D:\path\to\dois_row.txt"
$root = Split-Path -Parent $doiFile
$rows = Get-Content -LiteralPath $doiFile -Encoding UTF8 |
  Where-Object { $_.Trim() -and -not $_.TrimStart().StartsWith("#") }
$dois = ($rows | ForEach-Object { ($_.Trim() -split "\s+")[0] }) -join ","

$node = "node"
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
  $node = "$env:LOCALAPPDATA\OpenAI\Codex\bin\node.exe"
}
$nd = "$env:USERPROFILE\.agents\skills\nature-downloader"

$json = & $node "$nd\scripts\batch_download.mjs" `
  --dois $dois `
  --out $root `
  --proxy "http://127.0.0.1:3456" `
  --debug 2> "$root\nature_downloader_stderr.log"

$json | Set-Content -LiteralPath "$root\nature_downloader_results.json" -Encoding UTF8
```

Important: `batch_download.mjs` may exit nonzero when some papers still need user verification. Do not treat that as total failure. Inspect `nature_downloader_results.json` and count `downloaded` statuses.

The script normally saves files to:

```text
<root>\PDFs\
```

## Folder Preservation

If the input file has `DOI<TAB>subfolder` or `DOI subfolder`, keep both copies:

```text
<root>\PDFs\<safe-doi>.pdf
<root>\<subfolder>\<safe-doi>.pdf
```

Create missing subfolders with `New-Item -ItemType Directory -Force`. Copy each PDF with an explicit `Copy-Item -LiteralPath ... -Destination ...` command. Do not delete the central `PDFs` cache unless the user explicitly asks.

Use a DOI-safe filename by replacing `/` with `_`:

```text
10.1038/s41598-017-03877-5 -> 10.1038_s41598-017-03877-5.pdf
```

## Verification Handoff

Use these statuses from `nature_downloader_results.json` as user handoff states, not final failures:

```text
carsi_waiting_user
publisher_verification_waiting_user
sciencedirect_robot_check
publisher_blocked_waiting_user
retry_after_user_verification
```

For each handoff paper:

1. Record it in `publisher_verification.tsv` or `carsi_retry.tsv`.
2. Tell the user the exact paper/DOI and the visible Chrome tab/page that needs manual action.
3. Stop automation on CAPTCHA, Cloudflare, bot-check, QR, SMS/OTP, and login pages.
4. After the user says it is verified, reuse the same tab when possible.

If the page is now a PDF viewer or official PDF URL in Chrome, download through the browser context:

```powershell
& $node "$nd\scripts\browser_pdf_downloader.mjs" `
  --target "<chrome-target-id>" `
  --out "$root\PDFs\10.xxxx_yyyy.pdf" `
  --proxy "http://127.0.0.1:3456"
```

Use `--target` when the verified article/PDF tab is already open. Use `--url` only when opening a fresh official PDF URL is safer. After a successful retry, update `nature_downloader_results.json` and the TSV status to `downloaded`.

## PDF Verification

Verify each downloaded PDF before declaring the batch complete:

```powershell
$py = "C:\Users\louis\mysoft\env\pyenv\codex\Scripts\python.exe"
Get-ChildItem -LiteralPath "$root\PDFs" -Filter "*.pdf" | ForEach-Object {
  & $py -c "from pathlib import Path; from pypdf import PdfReader; import sys; p=Path(sys.argv[1]); print(p.name, p.read_bytes()[:4] == b'%PDF', len(PdfReader(str(p)).pages))" $_.FullName
}
```

Minimum success criteria:

- File exists in `<root>\PDFs`.
- If a subfolder was requested, the copied PDF exists there too.
- First bytes are `%PDF`.
- Page count is nonzero.
- The manifest reports the paper as `downloaded`, `open_access_downloaded`, or another accurate final status.

Some valid PDFs emit harmless parser warnings. If the `%PDF` header and page count are valid, report the warning separately rather than redownloading in a loop.

## Output Artifacts

For each project root, keep these artifacts when applicable:

```text
PDFs\
<paper-subfolders>\
nature_downloader_results.json
nature_downloader_stderr.log
publisher_verification.tsv
carsi_retry.tsv
```

Final response should include:

- total DOI count and downloaded count;
- path to the root and central `PDFs` directory;
- any papers still waiting for CARSI or publisher verification;
- whether supporting information was downloaded or intentionally skipped;
- verification result, including page counts when available.

## Failure Rules

- Do not silently switch to `scansci-pdf`.
- Do not use unauthorized mirrors.
- Do not retry publisher checks in loops.
- Do not label a browser/login/security challenge as permanent failure.
- Do not claim success from HTTP status alone; verify `%PDF` bytes.
- Do not paste large DOMs, PDF bytes, or full target JSON into chat. Keep large data in scripts/logs and report compact statuses.
