@echo off
setlocal

echo Updating NG from GitHub...
cd /d "%~dp0\.."

where git >nul 2>nul
if errorlevel 1 (
  echo ERROR: Git is not installed or not available in PATH.
  echo Install GitHub Desktop or Git for Windows, then try again.
  pause
  exit /b 1
)

git status --short
if not errorlevel 0 (
  echo ERROR: This folder does not look like a Git repository.
  pause
  exit /b 1
)

echo.
echo Pulling latest changes...
git pull --ff-only
if errorlevel 1 (
  echo.
  echo ERROR: Could not fast-forward update.
  echo You may have local changes. Open GitHub Desktop or ask ChatGPT for help.
  pause
  exit /b 1
)

echo.
echo Running data validation...
python tools\validate_project.py
if errorlevel 1 goto validation_failed
python tools\validate_character_creation.py
if errorlevel 1 goto validation_failed
python tools\validate_portraits.py
if errorlevel 1 goto validation_failed
python tools\validate_quest_seeds.py
if errorlevel 1 goto validation_failed
python tools\validate_asset_kits.py
if errorlevel 1 goto validation_failed

echo.
echo NG is updated and validation passed.
pause
exit /b 0

:validation_failed
echo.
echo WARNING: Update completed, but validation failed.
pause
exit /b 1
