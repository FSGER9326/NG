@echo off
setlocal

cd /d "%~dp0\.."
set DEBUG_DIR=%CD%\debug\latest

if not exist "%DEBUG_DIR%" mkdir "%DEBUG_DIR%"

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
  echo Validation still passed; no scenario test was run. > "%DEBUG_DIR%\scenario.log"
  pause
  exit /b 2
)

echo Running Godot scenario test...
set NG_DEBUG_DIR=%DEBUG_DIR%
"%GODOT_EXE%" --headless --path . --script res://tools/run_scenario_test.gd --scenario res://tests/scenarios/wolfpine_missing_caravan.json > "%DEBUG_DIR%\scenario.log" 2>&1
if errorlevel 1 (
  echo Scenario test failed. See debug\latest\scenario.log and debug\latest\game.log
  type "%DEBUG_DIR%\scenario.log"
  pause
  exit /b 1
)

echo Scenario test passed.
echo Debug logs written to: %DEBUG_DIR%
pause
