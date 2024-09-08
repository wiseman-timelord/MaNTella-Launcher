:: Script: Mantella-Vanilla.Bat

:: Initialization
@echo off
setlocal EnableDelayedExpansion

:: Global Variables
set "PYTHON_EXE_TO_USE="
set "CONFIG_INI_PATH="

:: Display Is Reset
cls
echo ========================================================================================================================
echo     Mantella-Vanilla
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo Working Folder: %ScriptDirectoryMantella%
timeout /t 1 >nul

:: ADMIN AND DP0, BLOCK, DO NOT MODIFY: START
net session >nul 2>&1 || (
    echo Error: Admin privileges required. Right-click and select "Run as administrator".
    timeout /t 3 >nul
    goto :end_of_script
)
echo Status: Administrator
timeout /t 1 >nul
set "SCRIPT_DIRECTORY_PATH=%~dp0"
set "SCRIPT_DIRECTORY_PATH=%SCRIPT_DIRECTORY_PATH:~0,-1%"
pushd "%SCRIPT_DIRECTORY_PATH%"
echo Path Dp0'd To Script.
timeout /t 1 >nul
:: ...ADMIN AND DP0, BLOCK, DO NOT MODIFY: END

:: Find Python 3.11
for %%I in (
    "C:\Program Files\Python311\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
) do (
    if exist "%%~I" (
        set "PYTHON_EXE_TO_USE=%%~I"
        goto :found_python311
    )
)
:found_python311
if not defined PYTHON_EXE_TO_USE (
    echo Error: Python 3.11 not found. Please install it before running this script.
    timeout /t 3 >nul
    goto :end_of_script
)
echo Python 3.11 Found
timeout /t 1 >nul

:: First run check
for /f "usebackq tokens=3*" %%A in (`reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Personal`) do (
    set "CONFIG_INI_PATH=%%A\My Games\Mantella\config.ini"
)
set "CONFIG_INI_PATH=%CONFIG_INI_PATH:/=\%"
if not exist "%CONFIG_INI_PATH%" (
    echo First Run Detected. Please run Install-Setup.Bat first!
    timeout /t 3 >nul
    goto :end_of_script
)
echo Found Config File.

:: Running Mantella
echo Running Mantella...
timeout /t 1 >nul
"%PYTHON_EXE_TO_USE%" .\main.py
if errorlevel 1 (
    echo Error occurred while running Mantella.
    goto :end_of_script
)
echo Mantella Exited.
timeout /t 2 >nul

:end_of_script
:: Exit Program
echo Closing in 5 seconds...
timeout /t 5 >nul
exit /b
