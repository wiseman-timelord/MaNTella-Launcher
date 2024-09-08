@echo off
setlocal EnableDelayedExpansion

:: Global Variables
set "PIP_EXE_TO_USE="
set "PYTHON_EXE_TO_USE="

:: ADMIN AND DP0, BLOCK, DO NOT MODIFY: START
net session >nul 2>&1 || (
    echo Error: Admin privileges required. Right-click and select "Run as administrator".
    timeout /t 3 >nul
    exit /b 1
)
echo Status: Administrator
timeout /t 1 >nul
set "SCRIPT_DIRECTORY_PATH=%~dp0"
set "SCRIPT_DIRECTORY_PATH=%SCRIPT_DIRECTORY_PATH:~0,-1%"
pushd "%SCRIPT_DIRECTORY_PATH%"
echo Path Dp0'd To Script.
timeout /t 1 >nul
:: ...ADMIN AND DP0, BLOCK, DO NOT MODIFY: END

:: Display Is Reset
cls
echo ========================================================================================================================
echo     Mantella
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo Working Folder: %ScriptDirectoryMantella%
timeout /t 1 >nul

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
    goto :eof
)
echo Python Found: %PYTHON_EXE_TO_USE%
timeout /t 1 >nul

:: First run check and requirement installation
if not exist "%USERPROFILE%\Documents\My Games\Mantella\config.bak" (
    echo First Run, Fool-Proofing Mantella...
    timeout /t 1 >nul
    "%PIP_EXE_TO_USE%" install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install requirements. Check Python and pip installation.
        goto eof
    )
    echo ..Requirements Installed ^(Hopefully^).
    timeout /t 2 >nul
)

:: Running Mantella
echo Running Mantella...
timeout /t 1 >nul
"%PYTHON_EXE_TO_USE%" .\main.py
if errorlevel 1 (
    echo Error occurred while running Mantella.
    goto eof
)
echo Mantella Exited.
timeout /t 2 >nul

:eof
:: Exit Program
echo Closing in 5 seconds...
timeout /t 5 >nul
exit /b
