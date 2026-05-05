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
$validators = @(
    'tools/validate_project.py',
    'tools/validate_character_creation.py',
    'tools/validate_portraits.py',
    'tools/validate_quest_seeds.py',
    'tools/validate_gdscript_helpers.py',
    'tools/validate_issue_13_patcher.py',
    'tools/validate_asset_kits.py'
)
foreach ($validator in $validators) {
    python $validator
    if ($LASTEXITCODE -ne 0) {
        Write-Host ''
        Write-Host "WARNING: Update completed, but validation failed while running $validator."
        Read-Host 'Press Enter to exit'
        exit 1
    }
}

Write-Host ''
Write-Host 'NG is updated and validation passed.'
Read-Host 'Press Enter to exit'
