@echo off
setlocal EnableDelayedExpansion

:: Remove trailing backslash from ScriptDirectoryWt
set "ScriptDirectoryWt=%~dp0"
set "ScriptDirectoryWt=%ScriptDirectoryWt:~0,-1%"

:: Change to the script's directory
pushd "%ScriptDirectoryWt%"

:: Display Is Reset
cls
echo ========================================================================================================================
echo                                           Mantella-xVASynth Optimizer/Launcher
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo Working Dir: %ScriptDirectoryWt%
timeout /t 1 >nul

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo This script requires administrative privileges. 
    echo Right click and run as an administrator.
    echo This script exits in 15 seconds...
    timeout /t 15 >nul
    popd
    exit /b
)

:: Run the Python script for config cleaning and menu
echo Running Mantella/xVASynth Optimizer-Launcher...
python main-wt.py
echo ...Mantella/xVASynth Optimizer-Launcher Closed...
timeout /t 1 >nul


:: Read the output values from main-wt.txt
for /f "tokens=1,2 delims==" %%i in (main-wt.txt) do (
    if "%%i"=="exit_code" set exit_code=%%j
    if "%%i"=="xvasynth_path" set xvasynth_path=%%j
)

if "%exit_code%" equ "1" (
    echo User chose to exit. Closing in 5 seconds...
    timeout /t 5 >nul
    popd
    exit /b
)

:: Check if xVASynth.exe is running and start if necessary
echo Checking for xVASynth...
tasklist /FI "IMAGENAME eq xVASynth.exe" 2>NUL | find /I /N "xVASynth.exe">NUL
if "%ERRORLEVEL%" NEQ "0" (
    echo xVASynth.exe is not running. Starting xVASynth...
    if exist "%xvasynth_path%\xVASynth.exe" (
        pushd "%xvasynth_path%"
        powershell -Command "Start-Process '%xvasynth_path%\xVASynth.exe' -NoNewWindow"
        popd
    ) else (
        echo Error: xVASynth.exe not found at %xvasynth_path%
        echo Please check your config.ini file and ensure the xvasynth_folder path is correct.
        timeout /t 10 >nul
        popd
        exit /b
    )
    timeout /t 3 >nul
)
timeout /t 1 >nul

:: Running Mantella
echo Running Mantella...
timeout /t 1 >nul
python .\main.py

:: Cleanup and exit
echo Mantella Exited.
timeout /t 10 >nul

:: Return to the original directory
popd
exit /b