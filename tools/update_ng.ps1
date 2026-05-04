$ErrorActionPreference = 'Stop'

Write-Host 'Updating NG from GitHub...'
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $repoRoot

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host 'ERROR: Git is not installed or not available in PATH.'
    Write-Host 'Install GitHub Desktop or Git for Windows, then try again.'
    Read-Host 'Press Enter to exit'
    exit 1
}

try {
    git status --short | Out-Host
} catch {
    Write-Host 'ERROR: This folder does not look like a Git repository.'
    Read-Host 'Press Enter to exit'
    exit 1
}

Write-Host ''
Write-Host 'Pulling latest changes...'
git pull --ff-only
if ($LASTEXITCODE -ne 0) {
    Write-Host ''
    Write-Host 'ERROR: Could not fast-forward update.'
    Write-Host 'You may have local changes. Open GitHub Desktop or ask ChatGPT for help.'
    Read-Host 'Press Enter to exit'
    exit 1
}

Write-Host ''
Write-Host 'Running data validation...'
python tools/validate_project.py
if ($LASTEXITCODE -ne 0) {
    Write-Host ''
    Write-Host 'WARNING: Update completed, but validation failed.'
    Read-Host 'Press Enter to exit'
    exit 1
}

Write-Host ''
Write-Host 'NG is updated and validation passed.'
Read-Host 'Press Enter to exit'
