@echo off
setlocal

cd /d "%~dp0\.."
set REPO_DIR=%CD%
set DESKTOP_DIR=%USERPROFILE%\Desktop
set PLAY_SCRIPT=%REPO_DIR%\tools\one_click_play_upload.bat
set TEST_SCRIPT=%REPO_DIR%\tools\one_click_update_test_upload.bat
set PLAY_SHORTCUT=%DESKTOP_DIR%\NG Play + Upload.lnk
set TEST_SHORTCUT=%DESKTOP_DIR%\NG Test + Upload.lnk
set ICON_FILE=%REPO_DIR%\Godot.exe

if not exist "%ICON_FILE%" (
  for %%G in ("%REPO_DIR%\Godot_v*-stable_win64.exe") do if exist "%%~fG" set ICON_FILE=%%~fG
)

if not exist "%PLAY_SCRIPT%" (
  echo Missing script: %PLAY_SCRIPT%
  pause
  exit /b 1
)

if not exist "%TEST_SCRIPT%" (
  echo Missing script: %TEST_SCRIPT%
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "$shell = New-Object -ComObject WScript.Shell; $shortcut = $shell.CreateShortcut('%PLAY_SHORTCUT%'); $shortcut.TargetPath = $env:ComSpec; $shortcut.Arguments = '/c ""%PLAY_SCRIPT%""'; $shortcut.WorkingDirectory = '%REPO_DIR%'; if (Test-Path '%ICON_FILE%') { $shortcut.IconLocation = '%ICON_FILE%,0' }; $shortcut.Save()"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$shell = New-Object -ComObject WScript.Shell; $shortcut = $shell.CreateShortcut('%TEST_SHORTCUT%'); $shortcut.TargetPath = $env:ComSpec; $shortcut.Arguments = '/c ""%TEST_SCRIPT%""'; $shortcut.WorkingDirectory = '%REPO_DIR%'; if (Test-Path '%ICON_FILE%') { $shortcut.IconLocation = '%ICON_FILE%,0' }; $shortcut.Save()"

echo.
echo Desktop shortcuts created:
echo   %PLAY_SHORTCUT%
echo   %TEST_SHORTCUT%
echo.
echo Use "NG Play + Upload" to play the game and upload logs after exit/crash.
echo Use "NG Test + Upload" to run automated validation/scenario tests and upload logs.
echo.
pause
