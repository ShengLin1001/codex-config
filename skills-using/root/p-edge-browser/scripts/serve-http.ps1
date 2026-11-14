# Serve Playwright MCP (extension mode, user's Edge) over HTTP on 127.0.0.1 for remote agents (zcm6 via SSH).
# Must run in the interactive desktop session: extension mode connects by launching msedge.exe, and a
# launch from an sshd/service session cannot reach the Edge already open on the user's desktop.
# Token, env and base args are read from ~/.claude.json (mcpServers.playwright) so they live in one place.
param(
    [int]$port = 8931,
    [string]$path_output = "$env:USERPROFILE\.claude\playwright-output-remote"
)
$ErrorActionPreference = 'Stop'
$path_log = Join-Path $env:USERPROFILE '.claude\playwright-serve-http.log'

function fail($msg) { Write-Output "❌ ERROR: $msg"; exit 1 }

### check
$path_cfg = Join-Path $env:USERPROFILE '.claude.json'
if (-not (Test-Path $path_cfg)) { fail "$path_cfg not found" }
# PS 5.1 ConvertFrom-Json rejects keys differing only in case (~/.claude.json has such project paths), so let node slice it
$json_mcp = & node -e "const c=require(process.argv[1]);process.stdout.write(JSON.stringify(c.mcpServers&&c.mcpServers.playwright||null))" $path_cfg
$dict_mcp = $json_mcp | ConvertFrom-Json
if ($null -eq $dict_mcp) { fail 'mcpServers.playwright missing in ~/.claude.json' }
if (Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue) { fail "port $port already in use" }
### to here

### prepare
foreach ($prop in $dict_mcp.env.PSObject.Properties) { Set-Item -Path ("env:" + $prop.Name) -Value $prop.Value }
# Drop the local --output-dir so remote downloads land in their own folder
$largs = @()
$lbase = @($dict_mcp.args)
for ($i = 0; $i -lt $lbase.Count; $i++) {
    if ($lbase[$i] -eq '--output-dir') { $i++; continue }
    $largs += $lbase[$i]
}
$largs += '--output-dir', $path_output, '--host', '127.0.0.1', '--port', "$port"
New-Item -ItemType Directory -Path $path_output -Force | Out-Null
### to here

### main
# npx prints "npm notice" on stderr; under 'Stop' PS 5.1 turns that into a terminating NativeCommandError
$ErrorActionPreference = 'Continue'
Write-Output ("▶️ " + $dict_mcp.command + ' ' + ($largs -join ' ')) | Tee-Object -FilePath $path_log
& $dict_mcp.command @largs *>> $path_log
### to here
