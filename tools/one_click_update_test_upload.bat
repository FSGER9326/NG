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

for /f "delims=" %%B in ('git branch --show-current') do set CURRENT_BRANCH=%%B
if "%CURRENT_BRANCH%"=="" set CURRENT_BRANCH=main

for /f "delims=" %%T in ('powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set RUN_ID=%%T

echo Branch: %CURRENT_BRANCH%
echo Run: %RUN_ID%
echo.

echo Pulling latest changes from GitHub...
git pull --ff-only
if errorlevel 1 (
  echo.
  echo Could not auto-update because git pull failed.
  echo This usually means there are local changes or a merge conflict.
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
set RUN_REPORT_DIR=%CD%\debug_reports\runs\%RUN_ID%_test
if exist "%REPORT_DIR%" rmdir /s /q "%REPORT_DIR%"
mkdir "%REPORT_DIR%"
mkdir "%RUN_REPORT_DIR%"

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
echo automated_test > "%REPORT_DIR%\report_type.txt"
echo %RUN_ID% > "%REPORT_DIR%\run_id.txt"
python tools\analyze_debug_report.py "%REPORT_DIR%" > "%REPORT_DIR%\analysis_summary.txt" 2>&1

xcopy "%REPORT_DIR%" "%RUN_REPORT_DIR%" /E /I /Y >nul

echo.
echo Staging debug report files...
git add -f debug_reports/latest debug_reports/runs/%RUN_ID%_test

git diff --cached --quiet
if not errorlevel 1 (
  echo No debug report changes to commit.
) else (
  echo Committing debug report...
  git commit -m "Upload local test report %RUN_ID%"
  if errorlevel 1 (
    echo.
    echo Could not commit debug report.
    git status --short
    pause
    exit /b 1
  )

  echo Pushing debug report to GitHub...
  git push origin %CURRENT_BRANCH%
  if errorlevel 1 (
    echo.
    echo Could not push debug report.
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
)
echo Latest report: debug_reports/latest
echo Archived report: debug_reports/runs/%RUN_ID%_test
echo.
pause
exit /b %TEST_EXIT%
