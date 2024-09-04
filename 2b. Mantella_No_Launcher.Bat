@echo off
setlocal EnableDelayedExpansion

:: Global Variables
set "PIP_EXE_TO_USE="
set "PYTHON_EXE_TO_USE="

:: Change to the script's directory
set "ScriptDirectoryMantella=%~dp0"
set "ScriptDirectoryMantella=%ScriptDirectoryMantella:~0,-1%"
pushd "%ScriptDirectoryMantella%"

:: Display Is Reset
cls
echo ========================================================================================================================
echo                                                         Mantella
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo Working Folder: %ScriptDirectoryMantella%
timeout /t 1 >nul

:: Find Python 3.11 and pip
set "PYTHON_FOLDER_TO_USE="
for %%I in (
    "C:\Python311\"
    "C:\Program Files\Python311\"
    "%LocalAppData%\Programs\Python\Python311\"
) do (
    if exist "%%~I" (
        set "PYTHON_FOLDER_TO_USE=%%~I"
        set "PYTHON_EXE_TO_USE=%%~Ipython.exe"
        set "PIP_EXE_TO_USE=%%~IScripts\pip.exe"
        goto :found_python311
    )
)

:found_python311
if not defined PYTHON_EXE_TO_USE (
    echo Python 3.11 not found. Please ensure Python 3.11 is installed.
    goto eof
)

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
