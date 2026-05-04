@echo off
setlocal
cd /d "%~dp0\.."

echo ============================================================
echo NG one-click update, play, and upload logs
echo ============================================================

where git >nul 2>nul || (echo Git was not found on PATH.& pause& exit /b 1)
where python >nul 2>nul || (echo Python was not found on PATH.& pause& exit /b 1)

for /f "delims=" %%B in ('git branch --show-current') do set CURRENT_BRANCH=%%B
if "%CURRENT_BRANCH%"=="" set CURRENT_BRANCH=main
for /f "delims=" %%T in ('powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set RUN_ID=%%T

echo Pulling latest changes from GitHub...
git pull --ff-only || (echo Could not auto-update.& git status --short& pause& exit /b 1)

set DEBUG_DIR=%CD%\debug\latest
set REPORT_DIR=%CD%\debug_reports\latest
set RUN_REPORT_DIR=%CD%\debug_reports\runs\%RUN_ID%_play
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
  start "NG" /wait "%GODOT_EXE%" --path .
  set GAME_EXIT=%ERRORLEVEL%
)
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format o" > "%DEBUG_DIR%\exit_timestamp.txt"

:upload_report
if exist "%REPORT_DIR%" rmdir /s /q "%REPORT_DIR%"
mkdir "%REPORT_DIR%"
mkdir "%RUN_REPORT_DIR%"

for %%F in (validation.log manual_play_stdout.log game.log actions.jsonl state_initial.json state_latest.json state_after_scenario.json launch_timestamp.txt exit_timestamp.txt) do if exist "%DEBUG_DIR%\%%F" copy "%DEBUG_DIR%\%%F" "%REPORT_DIR%\%%F" >nul

git rev-parse HEAD > "%REPORT_DIR%\git_commit.txt" 2>nul
git status --short > "%REPORT_DIR%\git_status.txt" 2>nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format o" > "%REPORT_DIR%\timestamp.txt"
echo %VALIDATION_EXIT% > "%REPORT_DIR%\validation_exit_code.txt"
echo %GAME_EXIT% > "%REPORT_DIR%\game_exit_code.txt"
echo manual_play > "%REPORT_DIR%\report_type.txt"
echo %RUN_ID% > "%REPORT_DIR%\run_id.txt"
xcopy "%REPORT_DIR%" "%RUN_REPORT_DIR%" /E /I /Y >nul

echo Uploading latest play report to GitHub...
git add -f debug_reports/latest debug_reports/runs/%RUN_ID%_play
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "Upload local play report %RUN_ID%" || (git status --short& pause& exit /b 1)
  git push origin %CURRENT_BRANCH% || (git status --short& pause& exit /b 1)
) else (
  echo No debug report changes to commit.
)

echo.
echo DONE: play report uploaded to debug_reports/latest.
echo Archived report: debug_reports/runs/%RUN_ID%_play
echo Tell ChatGPT: I ran NG Launcher option 1.
pause
exit /b %GAME_EXIT%
