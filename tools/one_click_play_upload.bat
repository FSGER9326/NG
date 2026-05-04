@echo off
setlocal

cd /d "%~dp0\.."

echo ============================================================
echo NG one-click update, play, and upload logs
echo ============================================================
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo Git was not found on PATH.
  pause
  exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found on PATH.
  pause
  exit /b 1
)

for /f "delims=" %%B in ('git branch --show-current') do set CURRENT_BRANCH=%%B
if "%CURRENT_BRANCH%"=="" set CURRENT_BRANCH=main

echo Pulling latest changes from GitHub...
git pull --ff-only
if errorlevel 1 (
  echo.
  echo Could not auto-update because git pull failed.
  echo This usually means local files changed or a merge conflict exists.
  git status --short
  pause
  exit /b 1
)

set DEBUG_DIR=%CD%\debug\latest
set REPORT_DIR=%CD%\debug_reports\latest
if exist "%DEBUG_DIR%" rmdir /s /q "%DEBUG_DIR%"
mkdir "%DEBUG_DIR%"

echo Running validation before launch...
python tools\validate_project.py > "%DEBUG_DIR%\validation.log" 2>&1
set VALIDATION_EXIT=%ERRORLEVEL%
if not "%VALIDATION_EXIT%"=="0" (
  echo Validation failed. The game will not launch.
  type "%DEBUG_DIR%\validation.log"
  set GAME_EXIT=1
  goto upload_report
)

set GODOT_EXE=
set GODOT_CONSOLE_EXE=
where godot >nul 2>nul
if not errorlevel 1 set GODOT_EXE=godot

if exist "%CD%\Godot.exe" set GODOT_EXE=%CD%\Godot.exe
for %%G in ("%CD%\Godot_v*-stable_win64.exe") do if exist "%%~fG" set GODOT_EXE=%%~fG
for %%G in ("%CD%\Godot_*_win64.exe") do if exist "%%~fG" set GODOT_EXE=%%~fG
for %%G in ("%CD%\Godot*_console.exe" "%CD%\Godot_*_console.exe") do if exist "%%~fG" set GODOT_CONSOLE_EXE=%%~fG

if "%GODOT_EXE%"=="" if "%GODOT_CONSOLE_EXE%"=="" (
  echo Could not find Godot on PATH or in repo root.
  echo Put Godot_v*-stable_win64.exe or Godot.exe in this folder, then retry.
  echo Godot missing. > "%DEBUG_DIR%\manual_play_stdout.log"
  set GAME_EXIT=2
  goto upload_report
)

set NG_DEBUG_DIR=%DEBUG_DIR%
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format o" > "%DEBUG_DIR%\launch_timestamp.txt"

if not "%GODOT_CONSOLE_EXE%"=="" (
  echo Launching game with console executable so this script waits for exit:
  echo %GODOT_CONSOLE_EXE%
  "%GODOT_CONSOLE_EXE%" --path . > "%DEBUG_DIR%\manual_play_stdout.log" 2>&1
  set GAME_EXIT=%ERRORLEVEL%
) else (
  echo Launching game:
  echo %GODOT_EXE%
  echo If this script continues immediately, use the Godot console executable for best auto-upload behavior.
  start "NG" /wait "%GODOT_EXE%" --path .
  set GAME_EXIT=%ERRORLEVEL%
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format o" > "%DEBUG_DIR%\exit_timestamp.txt"

:upload_report
if exist "%REPORT_DIR%" rmdir /s /q "%REPORT_DIR%"
mkdir "%REPORT_DIR%"

if exist "%DEBUG_DIR%\validation.log" copy "%DEBUG_DIR%\validation.log" "%REPORT_DIR%\validation.log" >nul
if exist "%DEBUG_DIR%\manual_play_stdout.log" copy "%DEBUG_DIR%\manual_play_stdout.log" "%REPORT_DIR%\manual_play_stdout.log" >nul
if exist "%DEBUG_DIR%\game.log" copy "%DEBUG_DIR%\game.log" "%REPORT_DIR%\game.log" >nul
if exist "%DEBUG_DIR%\actions.jsonl" copy "%DEBUG_DIR%\actions.jsonl" "%REPORT_DIR%\actions.jsonl" >nul
if exist "%DEBUG_DIR%\state_initial.json" copy "%DEBUG_DIR%\state_initial.json" "%REPORT_DIR%\state_initial.json" >nul
if exist "%DEBUG_DIR%\state_latest.json" copy "%DEBUG_DIR%\state_latest.json" "%REPORT_DIR%\state_latest.json" >nul
if exist "%DEBUG_DIR%\state_after_scenario.json" copy "%DEBUG_DIR%\state_after_scenario.json" "%REPORT_DIR%\state_after_scenario.json" >nul
if exist "%DEBUG_DIR%\launch_timestamp.txt" copy "%DEBUG_DIR%\launch_timestamp.txt" "%REPORT_DIR%\launch_timestamp.txt" >nul
if exist "%DEBUG_DIR%\exit_timestamp.txt" copy "%DEBUG_DIR%\exit_timestamp.txt" "%REPORT_DIR%\exit_timestamp.txt" >nul

git rev-parse HEAD > "%REPORT_DIR%\git_commit.txt" 2>nul
git status --short > "%REPORT_DIR%\git_status.txt" 2>nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format o" > "%REPORT_DIR%\timestamp.txt"
echo %VALIDATION_EXIT% > "%REPORT_DIR%\validation_exit_code.txt"
echo %GAME_EXIT% > "%REPORT_DIR%\game_exit_code.txt"

echo.
echo Uploading latest play report to GitHub...
git add debug_reports/latest

git diff --cached --quiet
if not errorlevel 1 (
  echo No debug report changes to commit.
) else (
  git commit -m "Upload latest local play report"
  if errorlevel 1 (
    echo Could not commit report.
    git status --short
    pause
    exit /b 1
  )

  git push origin %CURRENT_BRANCH%
  if errorlevel 1 (
    echo Could not push report.
    git status --short
    pause
    exit /b 1
  )
)

echo.
echo DONE: play report uploaded to debug_reports/latest.
echo Tell ChatGPT: I ran one_click_play_upload.
echo.
pause
exit /b %GAME_EXIT%
