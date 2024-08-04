@echo off

:: Initialization
pushd "%~dp0"
setlocal EnableDelayedExpansion

:: Display has been reset...
cls
echo ========================================================================================================================
echo                                           Mantella-xVASynth Optimizer/Launcher
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo dp0 was used.
timeout /t 1 >nul

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo This script requires administrative privileges. 
    echo Right click and run as an administrator.
    echo This script exits in 15 seconds...
    timeout /t 15 >nul
    exit /b
)

:: Run the Python script for config cleaning and menu
echo Running Mantella xVASynth Optimizer...
python main-wt.py

:: Read the output values from main-wt.txt
set "exit_code="
set "xvasynth_path="

for /f "tokens=1,2 delims==" %%i in (main-wt.txt) do (
    if "%%i"=="exit_code" set exit_code=%%j
    if "%%i"=="xvasynth_path" set xvasynth_path=%%j
)

if "%exit_code%" equ "1" (
    echo User chose to exit. Closing in 5 seconds...
    timeout /t 5 >nul
    exit /b
)

:: Display has been reset...
cls
echo ========================================================================================================================
echo                                          Mantella-xVASynth Optimizer/Launcher
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo. Launcher-Optimizer Exited.
timeout /t 1 >nul

:: Check if xVASynth.exe is running
echo xVASynth Automation... 
echo Checking running processes...
tasklist /FI "IMAGENAME eq xVASynth.exe" 2>NUL | find /I /N "xVASynth.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo xVASynth.exe is already running. Continuing to Mantella...
) else (
    echo xVASynth.exe is not running.
    echo Starting xVASynth...
	CD %xvasynth_path%
    if exist "%xvasynth_path%\xVASynth.exe" (
		powershell -Command ^ Start-Process "%xvasynth_path%\xVASynth.exe" -NoNewWindow
    ) else (
        echo Error: xVASynth.exe not found at %xvasynth_path%
        echo Please check your config.ini file and ensure the xvasynth_folder path is correct.
        timeout /t 10 >nul
        exit /b
    )
    timeout /t 3 >nul
)
pushd "%~dp0"

:: Display has been reset...
cls
echo ========================================================================================================================
echo                                          Mantella-xVASynth Optimizer/Launcher
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo dp0 was used.
timeout /t 1 >nul

:: Continue xVASynth
echo ...xVASynth Automated.
echo.
timeout /t 2 >nul

:: Running Mantella
echo Running Mantella...
timeout /t 1 >nul
python .\main.py
echo Mantella Exited.
echo.
timeout /t 2 >nul

:: Wait 10 seconds 
echo.
echo 10 Seconds Until Self-Destruct!!
timeout /t 10 >nul
