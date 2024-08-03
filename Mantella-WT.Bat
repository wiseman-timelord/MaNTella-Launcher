@echo off

:: Initialization
pushd "%~dp0"
setlocal EnableDelayedExpansion

:: Display has been reset...
cls
echo ==============================================================================
echo                     Mantella-xVASynth Optimizer/Launcher
echo ------------------------------------------------------------------------------
echo.

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo This script requires administrative privileges. 
    echo Right click and run as an administrator.
    echo This script exits in 15 seconds...
    timeout /t 15 >nul
    exit /b
)

:: Configuration file
echo Maintenance for config...
echo Auto-Cleaning .\config.ini
python .\scripts\clean_config.py
timeout /t 1 >nul
echo config.ini Location: %cd%
set configFile=.\config.ini
echo ...Maintenance Complete.
echo.
timeout /t 2 >nul

:: Check if xVASynth.exe is running
echo xVASynth Automation... 
echo Checking running processes...
tasklist /FI "IMAGENAME eq xVASynth.exe" 2>NUL | find /I /N "xVASynth.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo xVASynth.exe is already running. Continuing to Mantella...
) else (
    echo xVASynth.exe is not running.
    echo Starting xVASynth...
    
    :: Start VASynth using PowerShell to avoid admin elevation
	pushd .\xVASynth
    echo xVASynth Work Dir: %cd%
	powershell -Command ^
        Start-Process ".\xVASynth.exe" -NoNewWindow
    popd
    timeout /t 3 >nul
)
echo ...xVASynth Automated.
echo.
timeout /t 2 >nul

:: Running Mantella
echo Running Mantella...
timeout /t 1 >nul
echo Mantella Work Dir: %cd%
timeout /t 2 >nul
python .\main.py
echo Mantella Exited.
echo.
timeout /t 2 >nul

:: Wait 5 seconds 
echo.
echo 10 Seconds Until Self-Destruct!!
timeout /t 10 >nul