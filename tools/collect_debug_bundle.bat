@echo off
setlocal

cd /d "%~dp0\.."
set DEBUG_DIR=%CD%\debug\latest
set BUNDLE_DIR=%CD%\debug\bundle
set ZIP_PATH=%CD%\debug\NG_debug_latest.zip

call tools\run_debug_tests.bat
set TEST_EXIT=%ERRORLEVEL%

if exist "%BUNDLE_DIR%" rmdir /s /q "%BUNDLE_DIR%"
mkdir "%BUNDLE_DIR%"

if exist "%DEBUG_DIR%" xcopy "%DEBUG_DIR%" "%BUNDLE_DIR%" /E /I /Y >nul

git rev-parse HEAD > "%BUNDLE_DIR%\git_commit.txt" 2>nul
git status --short > "%BUNDLE_DIR%\git_status.txt" 2>nul

powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path '%BUNDLE_DIR%\*' -DestinationPath '%ZIP_PATH%' -Force"

if exist "%ZIP_PATH%" (
  echo.
  echo Debug bundle created:
  echo %ZIP_PATH%
  echo.
  echo Upload this zip to ChatGPT for analysis.
) else (
  echo Failed to create debug bundle zip. The raw bundle folder is:
  echo %BUNDLE_DIR%
)

pause
exit /b %TEST_EXIT%
