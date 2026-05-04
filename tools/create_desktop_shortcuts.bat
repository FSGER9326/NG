@echo off
setlocal

cd /d "%~dp0\.."
set REPO_DIR=%CD%
set DESKTOP_DIR=%USERPROFILE%\Desktop
set LAUNCHER_SCRIPT=%REPO_DIR%\tools\ng_launcher.bat
set LAUNCHER_SHORTCUT=%DESKTOP_DIR%\NG Launcher.lnk
set OLD_PLAY_SHORTCUT=%DESKTOP_DIR%\NG Play + Upload.lnk
set OLD_TEST_SHORTCUT=%DESKTOP_DIR%\NG Test + Upload.lnk
set ICON_FILE=%REPO_DIR%\Godot.exe

if not exist "%ICON_FILE%" (
  for %%G in ("%REPO_DIR%\Godot_v*-stable_win64.exe") do if exist "%%~fG" set ICON_FILE=%%~fG
)

if not exist "%LAUNCHER_SCRIPT%" (
  echo Missing script: %LAUNCHER_SCRIPT%
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "$shell = New-Object -ComObject WScript.Shell; $shortcut = $shell.CreateShortcut('%LAUNCHER_SHORTCUT%'); $shortcut.TargetPath = $env:ComSpec; $shortcut.Arguments = '/c ""%LAUNCHER_SCRIPT%""'; $shortcut.WorkingDirectory = '%REPO_DIR%'; if (Test-Path '%ICON_FILE%') { $shortcut.IconLocation = '%ICON_FILE%,0' }; $shortcut.Save()"

if exist "%OLD_PLAY_SHORTCUT%" del "%OLD_PLAY_SHORTCUT%"
if exist "%OLD_TEST_SHORTCUT%" del "%OLD_TEST_SHORTCUT%"

echo.
echo Desktop shortcut created:
echo   %LAUNCHER_SHORTCUT%
echo.
echo Use "NG Launcher" for play, automated tests, and log upload.
echo.
pause
