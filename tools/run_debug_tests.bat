@echo off
setlocal

cd /d "%~dp0\.."
set DEBUG_DIR=%CD%\debug\latest

if exist "%DEBUG_DIR%" rmdir /s /q "%DEBUG_DIR%"
mkdir "%DEBUG_DIR%"

echo Running NG validation...
python tools\validate_project.py > "%DEBUG_DIR%\validation.log" 2>&1
if errorlevel 1 (
  echo Validation failed. See debug\latest\validation.log
  type "%DEBUG_DIR%\validation.log"
  pause
  exit /b 1
)

echo Validation passed.

set GODOT_EXE=
where godot >nul 2>nul
if not errorlevel 1 set GODOT_EXE=godot

if "%GODOT_EXE%"=="" if exist "%CD%\Godot_v4.3-stable_win64.exe" set GODOT_EXE=%CD%\Godot_v4.3-stable_win64.exe
if "%GODOT_EXE%"=="" if exist "%CD%\Godot.exe" set GODOT_EXE=%CD%\Godot.exe

if "%GODOT_EXE%"=="" (
  echo Could not find Godot on PATH or in repo root.
  echo Put Godot.exe in this folder or add Godot to PATH, then retry.
  echo Validation still passed; no scenario tests were run. > "%DEBUG_DIR%\scenario.log"
  pause
  exit /b 2
)

set NG_DEBUG_DIR=%DEBUG_DIR%
set SCENARIO_LOG=%DEBUG_DIR%\scenario.log
if exist "%SCENARIO_LOG%" del "%SCENARIO_LOG%"

for %%S in (tests\scenarios\*.json) do (
  echo Running scenario %%~nS...
  echo ===== Scenario: %%~nS ===== >> "%SCENARIO_LOG%"
  "%GODOT_EXE%" --headless --path . --script res://tools/run_scenario_test.gd --scenario res://%%S >> "%SCENARIO_LOG%" 2>&1
  if errorlevel 1 (
    echo Scenario %%~nS failed. See debug\latest\scenario.log and debug\latest\game.log
    type "%SCENARIO_LOG%"
    pause
    exit /b 1
  )
  echo. >> "%SCENARIO_LOG%"
)

echo Scenario tests passed.
echo Debug logs written to: %DEBUG_DIR%
pause
