@echo off
setlocal EnableDelayedExpansion

:: Global Variables
set "PYTHON_EXE_TO_USE="
set "config_folder="
set "mantella_version="
set "ATTEMPTS=0"

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

:: Initialize display
call :banner_display

:: Check for python.exe in the specified locations or prompt user for a custom path
set "PYTHON_PATHS=C:\Program Files\Python311\python.exe C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
for %%I in (%PYTHON_PATHS%) do (
    if exist "%%~I" (
        set "PYTHON_EXE_TO_USE=%%~I"
        goto :python_found
    )
)
echo Python not found in the specified locations.
set /p PYTHON_EXE_TO_USE="Please enter the full path to python.exe (including python.exe): "
if not exist %PYTHON_EXE_TO_USE% (
    set /a ATTEMPTS+=1
    if %ATTEMPTS% lss 3 (
        echo The provided path does not exist. Attempt %ATTEMPTS% of 3. Please try again.
        goto find_python
    ) else (
        echo Maximum attempts reached. Exiting script.
        pause
        exit /b 1
    )
)
:python_found
echo Python 3.11 found at: %PYTHON_EXE_TO_USE%
timeout /t 1 >nul

:find_config
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
goto :menu

:: ML Banner 
:banner_display
cls
echo ========================================================================================================================
echo                                                      Install-Setup                                                     I
echo ========================================================================================================================
echo.
goto :eof

:: Main Menu
:menu
call :banner_display
echo.
echo.
echo.
echo     1. Install Requirements
echo.
echo     2. Install Torch[CPU]
echo.
echo     3. Upgrade Pip Version
echo.
echo.
echo.
echo.
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo.
echo.
echo.
echo     Mantella Detected: %mantella_version%
echo.
echo.
echo.
echo.
echo ========================================================================================================================
set /p "choice=Selection; Menu Options (1-3), Exit Install-Setup (X): "

if "%choice%"=="1" goto install_requirements
if "%choice%"=="2" goto install_torch
if "%choice%"=="3" goto upgrade_pip
if /i "%choice%"=="X" goto exit_script

:: Invalid choice handler
echo Invalid option. Please choose a valid option.
timeout /t 2 >nul
goto menu

:: Option 1: Install Requirements
:install_requirements
call :banner_display
echo Installing Requirements, Ensure Python v3.11...
timeout /t 2 >nul
"%PYTHON_EXE_TO_USE%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements. Check Python and pip installation.
    timeout /t 5 >nul
    goto menu
)
echo ..Requirements Installed ^(Hopefully^).
echo.
timeout /t 2 >nul
echo Verifying installation...
"%PYTHON_EXE_TO_USE%" -m pip check
if errorlevel 1 (
    echo Warning: Some conflicts may still exist. Please review the output above.
) else (
    echo All packages are installed correctly with no conflicts.
)
echo.
pause
goto menu

:: Option 2: Install Torch[CPU]
:install_torch
call :banner_display
call :find_python
if not defined PYTHON_EXE_TO_USE goto menu

:: Use python.exe -m pip to uninstall and install torch packages
echo Uninstalling existing Torch packages...
%PYTHON_EXE_TO_USE% -m pip uninstall torch torchvision torchaudio -y
echo Installing Torch for CPU...
%PYTHON_EXE_TO_USE% -m pip install torch==2.0.0+cpu torchvision==0.15.1+cpu torchaudio==2.0.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo Failed to install Torch[CPU]. Please check your Python installation.
    timeout /t 5 >nul
    goto menu
)
echo Torch[CPU] Installed.
timeout /t 2 >nul
goto menu

:: Option 3: Upgrade pip
:upgrade_pip
call :find_python
if not defined PYTHON_EXE_TO_USE goto menu

:: 3. Upgrade pip
call :banner_display
echo Upgrading pip...
%PYTHON_EXE_TO_USE% -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip. Please check your Python installation.
    timeout /t 5 >nul
    goto menu
)
echo pip upgraded.
pause
goto menu

:end_of_file
:: Exit Program
echo Closing in 5 seconds...
timeout /t 5 >nul
exit /b

:: Function Definitions
:backup_config
if defined config_folder (
    echo Config File: %config_folder%\config.ini
    if exist "%config_folder%\config.bak" (
        echo Backup Already Exists: %config_folder%\config.bak
        timeout /t 5 >nul
    ) else (
        copy /y "%config_folder%\config.ini" "%config_folder%\config.bak"
        echo File Backed Up: config.ini ^> config.bak
        echo Backup File: %config_folder%\config.bak
    )
    timeout /t 2 >nul
) else (
    echo Error: No configuration file found.
    echo Please ensure a config.ini exists in one of the expected locations.
    timeout /t 5 >nul
    goto :end_of_file
)
goto :eof

:: Exit Option: X
:exit_script
if "%mantella_version%"=="v11.4" (
    echo 1. Ensure to configure %config_folder%\config.ini.
    echo 2. After Configuration, Run MaNTella-Local.Bat.
    timeout /t 10 >nul
) else if "%mantella_version%"=="v12" (
    echo 1. Exit Mantella After "Waiting for player to select an NPC..."
    echo 2. Ensure to configure %config_folder%\config.ini.
    echo 3. After Configuration, Run Mantella.Bat.
    timeout /t 10 >nul
    echo Running Mantella...
    timeout /t 2 >nul
    "%PYTHON_EXE_TO_USE%" .\main.py
    if errorlevel 1 (
        echo Error occurred while running Mantella.
        goto end_of_file
    )
	call :backup_config
    timeout /t 5 >nul    
)
echo Exiting the script... Please wait.
timeout /t 2 >nul
exit /b
