@echo off

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo This script requires administrative privileges.
    echo Please run it as an administrator.
    timeout /t 5 >nul
    exit /b
)

:: Navigate to the directory where the batch file is located
pushd "%~dp0"
echo ==============================================================================
echo                          Mantella / xVASynth Launcher
echo ------------------------------------------------------------------------------
echo.
echo Administrator Mode.
echo Current Directory: %cd%

:: Check if xVASynth.exe is running
echo Checking for running xVASynth.exe process...
tasklist /FI "IMAGENAME eq xVASynth.exe" 2>NUL | find /I /N "xVASynth.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo xVASynth.exe is already running. Continuing to Mantella...
) else (
    echo xVASynth.exe is not running.
    echo Starting xVASynth...
    
    :: Start VASynth using PowerShell to avoid admin elevation
    powershell -Command ^
        Start-Process ".\xVASynth\xVASynth.exe" -WorkingDirectory ".\xVASynth" -NoNewWindow 
    timeout /t 1 >nul
)

:: Print running VASynth and main script
echo Running Mantella...
timeout /t 1 >nul

:: Run the main script
python .\main.py
echo Main script exited.

:: Wait 5 seconds 
echo.
echo 5 Seconds Until Self-Destruct!!
timeout /t 5 >nul
