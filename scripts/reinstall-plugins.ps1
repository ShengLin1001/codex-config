$ErrorActionPreference = "Stop"

# Codex plugin marketplaces to register.
$Marketplaces = @(
    @{
        Name = "ponytail"
        Source = "DietrichGebert/ponytail"
        GitUrl = "https://github.com/DietrichGebert/ponytail.git"
    }
)

# Codex plugins to install from configured marketplaces.
$Plugins = @(
    "ponytail@ponytail"
)

function Require-Command {
    param([Parameter(Mandatory = $true)][string]$Name)

    if (Get-Command $Name -ErrorAction SilentlyContinue) {
        return
    }

    if (Get-Command module -ErrorAction SilentlyContinue) {
        module avail $Name 2>&1 | Out-Host
    }

    throw "$Name was not found. Load or install it first, then rerun."
}

function Test-MarketplaceRegistered {
    param([Parameter(Mandatory = $true)][string]$Name)

    return [bool](Get-MarketplaceRoot $Name)
}

function Get-MarketplaceRoot {
    param([Parameter(Mandatory = $true)][string]$Name)

    $marketplaces = codex plugin marketplace list
    foreach ($line in $marketplaces | Select-Object -Skip 1) {
        if ($line -match "^\s*(\S+)\s+(.+)$" -and $Matches[1] -eq $Name) {
            return $Matches[2]
        }
    }

    return $null
}

function Test-PluginInstalled {
    param([Parameter(Mandatory = $true)][string]$Plugin)

    $pattern = "^\s*$([regex]::Escape($Plugin))\s+installed,"
    foreach ($line in codex plugin list) {
        if ($line -match $pattern) {
            return $true
        }
    }

    return $false
}

function Invoke-CheckedNativeCommand {
    param(
        [Parameter(Mandatory = $true)][string]$Command,
        [Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments
    )

    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Command $($Arguments -join ' ') failed with exit code $LASTEXITCODE."
    }
}

function Add-LocalMarketplaceFallback {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$GitUrl
    )

    Require-Command git

    $codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
    $fallbackRoot = if ($env:CODEX_MARKETPLACE_HOME) { $env:CODEX_MARKETPLACE_HOME } else { Join-Path $codexHome "marketplaces" }
    $fallbackDir = Join-Path $fallbackRoot $Name

    New-Item -ItemType Directory -Force -Path $fallbackRoot | Out-Null

    if (Test-Path (Join-Path $fallbackDir ".git")) {
        Invoke-CheckedNativeCommand git -C $fallbackDir pull --ff-only
    } elseif (Test-Path $fallbackDir) {
        throw "$fallbackDir exists but is not a Git checkout; move it aside or set CODEX_MARKETPLACE_HOME."
    } else {
        Invoke-CheckedNativeCommand git clone --depth 1 $GitUrl $fallbackDir
    }

    Invoke-CheckedNativeCommand codex plugin marketplace add $fallbackDir
}

function Register-Marketplace {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$GitUrl
    )

    $root = Get-MarketplaceRoot $Name
    if ($root) {
        if ($root -match "[/\\]\.staging[/\\]") {
            Write-Warning "Marketplace $Name uses staging checkout $root; re-registering with a stable local clone."
            Invoke-CheckedNativeCommand codex plugin marketplace remove $Name
            Add-LocalMarketplaceFallback -Name $Name -GitUrl $GitUrl
            return
        }

        Write-Host "Marketplace $Name is already configured."
        return
    }

    codex plugin marketplace add $Source
    if ($LASTEXITCODE -eq 0) {
        return
    }

    Write-Warning "Git marketplace add failed for $Source; falling back to a stable local clone."
    Add-LocalMarketplaceFallback -Name $Name -GitUrl $GitUrl
}

Require-Command codex

foreach ($marketplace in $Marketplaces) {
    Register-Marketplace -Name $marketplace.Name -Source $marketplace.Source -GitUrl $marketplace.GitUrl
}

foreach ($plugin in $Plugins) {
    if (Test-PluginInstalled $plugin) {
        Write-Host "Plugin $plugin is already installed."
    } else {
        Invoke-CheckedNativeCommand codex plugin add $plugin
    }
}

codex plugin marketplace list
codex plugin list
