@echo off
setlocal EnableDelayedExpansion

:: Change to the script's directory
set "ScriptDirectoryMantella=%~dp0"
set "ScriptDirectoryMantella=%ScriptDirectoryMantella:~0,-1%"
pushd "%ScriptDirectoryMantella%"

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Error: Admin Required!
    echo Right Click, then Run As Administrator.
    timeout /t 3 >nul
    goto :end_of_file
)
echo Admin Status: Administrator 

:: Check Folder
echo Working Folder: %ScriptDirectoryMantella%
timeout /t 1 >nul

:: Find Config
if exist ".\config.ini" (
    set "mantella_version=v11.4"
    set "config_folder=.\"
) else if exist "%USERPROFILE%\Documents\My Games\Mantella\config.ini" (
    set "mantella_version=v12"
    set "config_folder=%USERPROFILE%\Documents\My Games\Mantella"
) else (
    echo Error: File Missing: config.ini
    timeout /t 5 >nul
    goto :end_of_file
)
	
:: Display Is Reset
cls
echo ========================================================================================================================
echo                                                          Mantella %mantella_version%
echo ------------------------------------------------------------------------------------------------------------------------
echo.

:: First run check and requirement installation
echo Installing Requirements, Ensure Python v3.11...
timeout /t 2 >nul
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements. Check Python and pip installation.
    goto end_of_file
)
echo ..Requirements Installed ^(Hopefully^).
echo.
timeout /t 2 >nul

:: Backup Config
if defined config_folder (
	echo Config File: %config_folder%\config.ini
	copy /y "%config_folder%\config.ini" "%config_folder%\config.bak"
    echo File Backed Up: config.ini ^> config.bak
	echo Backup File: %config_folder%\config.bak
    timeout /t 2 >nul
) else (
    echo Error: No configuration file found.
    echo Please ensure a config.ini exists in one of the expected locations.
    timeout /t 5 >nul
    goto : end_of_file
)

:: After Requirements.
if "%mantella_version%"=="v11.4" (
    echo After First_Run Exits...
    echo 1. Ensure to configure %config_file%.
    echo 2. After Configuring, Run Launcher.Bat.
    timeout /t 2 >nul
    echo Exit Sequence In 10 Seconds...
    timeout /t 10 >nul
    goto end_of_file
) else if "%mantella_version%"=="v12" (
    echo 1. Exit Mantella After "Waiting for player to select an NPC...
    echo 2. Ensure to configure %config_file%.
    echo 3. After Configuring, Run Launcher.Bat.
    timeout /t 2 >nul
    echo.
    echo Running Mantella In 10 Seconds...
    timeout /t 10 >nul
    echo Running Mantella...
    timeout /t 2 >nul
    python .\main.py
    if errorlevel 1 (
        echo Error occurred while running Mantella.
        goto end_of_file
    )
    echo Mantella Exited.
    timeout /t 5 >nul    
)

:end_of_file
:: Exit Program
echo Closing in 5 seconds...
timeout /t 5 >nul
exit /b
