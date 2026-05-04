@echo off
setlocal

cd /d "%~dp0\.."

:menu
cls
echo ============================================================
echo NG Launcher
echo ============================================================
echo.
echo 1. Play game, then upload logs after exit/crash
echo 2. Run automated tests, then upload logs
echo 3. Create/update desktop shortcut
echo 4. Exit
echo.
choice /C 1234 /N /M "Choose an option [1-4]: "
set CHOICE=%ERRORLEVEL%

if "%CHOICE%"=="1" goto play
if "%CHOICE%"=="2" goto test
if "%CHOICE%"=="3" goto shortcut
if "%CHOICE%"=="4" exit /b 0

goto menu

:play
call tools\one_click_play_upload.bat
goto end

:test
call tools\one_click_update_test_upload.bat
goto end

:shortcut
call tools\create_desktop_shortcuts.bat
goto end

:end
echo.
echo NG Launcher finished.
pause
exit /b %ERRORLEVEL%
