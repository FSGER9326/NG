@echo off
setlocal

cd /d "%~dp0\.."

echo ============================================================
echo NG one-click update, test, and upload logs
echo ============================================================
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo Git was not found on PATH.
  echo Install Git for Windows or open this from Git Bash/Developer tools.
  pause
  exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found on PATH.
  echo Install Python or add it to PATH.
  pause
  exit /b 1
)

echo Checking current git branch...
for /f "delims=" %%B in ('git branch --show-current') do set CURRENT_BRANCH=%%B
if "%CURRENT_BRANCH%"=="" set CURRENT_BRANCH=main
echo Branch: %CURRENT_BRANCH%
echo.

echo Pulling latest changes from GitHub...
git pull --ff-only
if errorlevel 1 (
  echo.
  echo Could not auto-update because git pull failed.
  echo This usually means there are local changes or a merge conflict.
  echo Commit/stash local changes or ask ChatGPT to help from the git status output.
  git status --short
  pause
  exit /b 1
)

echo.
echo Running tests and collecting debug bundle...
set NG_NO_PAUSE=1
call tools\run_debug_tests.bat
set TEST_EXIT=%ERRORLEVEL%
set NG_NO_PAUSE=

set REPORT_DIR=%CD%\debug_reports\latest
if exist "%REPORT_DIR%" rmdir /s /q "%REPORT_DIR%"
mkdir "%REPORT_DIR%"

if exist "%CD%\debug\latest\validation.log" copy "%CD%\debug\latest\validation.log" "%REPORT_DIR%\validation.log" >nul
if exist "%CD%\debug\latest\scenario.log" copy "%CD%\debug\latest\scenario.log" "%REPORT_DIR%\scenario.log" >nul
if exist "%CD%\debug\latest\game.log" copy "%CD%\debug\latest\game.log" "%REPORT_DIR%\game.log" >nul
if exist "%CD%\debug\latest\actions.jsonl" copy "%CD%\debug\latest\actions.jsonl" "%REPORT_DIR%\actions.jsonl" >nul
if exist "%CD%\debug\latest\state_initial.json" copy "%CD%\debug\latest\state_initial.json" "%REPORT_DIR%\state_initial.json" >nul
if exist "%CD%\debug\latest\state_latest.json" copy "%CD%\debug\latest\state_latest.json" "%REPORT_DIR%\state_latest.json" >nul
if exist "%CD%\debug\latest\state_after_scenario.json" copy "%CD%\debug\latest\state_after_scenario.json" "%REPORT_DIR%\state_after_scenario.json" >nul

git rev-parse HEAD > "%REPORT_DIR%\git_commit.txt" 2>nul
git status --short > "%REPORT_DIR%\git_status.txt" 2>nul

powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format o" > "%REPORT_DIR%\timestamp.txt"
echo %TEST_EXIT% > "%REPORT_DIR%\test_exit_code.txt"

echo.
echo Staging debug report files...
git add debug_reports/latest

git diff --cached --quiet
if not errorlevel 1 (
  echo No debug report changes to commit.
) else (
  echo Committing debug report...
  git commit -m "Upload latest local debug report"
  if errorlevel 1 (
    echo.
    echo Could not commit debug report.
    echo Check git user config or local repo state.
    git status --short
    pause
    exit /b 1
  )

  echo Pushing debug report to GitHub...
  git push origin %CURRENT_BRANCH%
  if errorlevel 1 (
    echo.
    echo Could not push debug report.
    echo You may need to sign into GitHub or resolve remote changes.
    git status --short
    pause
    exit /b 1
  )
)

echo.
if "%TEST_EXIT%"=="0" (
  echo DONE: local files updated, tests passed, logs uploaded.
) else (
  echo DONE: local files updated, tests failed or Godot was missing, logs uploaded.
  echo I can inspect debug_reports/latest in GitHub now.
)
echo.
pause
exit /b %TEST_EXIT%
