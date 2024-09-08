@echo off
setlocal EnableDelayedExpansion

:: Global Variables
set "PYTHON_EXE_TO_USE="
set "CONFIG_INI_PATH="
set "ATTEMPTS=0"

:: Initialize display
call :banner_display

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
echo Dp0'd to Script Dir.
timeout /t 1 >nul
:: ...ADMIN AND DP0, BLOCK, DO NOT MODIFY: END

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
echo Python 3.11 found
timeout /t 1 >nul

:: Fetch Documents folder from Registry
for /f "usebackq tokens=3*" %%A in (`reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Personal`) do (
    set "CONFIG_INI_PATH=%%A\My Games\Mantella\config.ini"
)
set "CONFIG_INI_PATH=%CONFIG_INI_PATH:/=\%"
echo config.ini found
timeout /t 1 >nul

:: Initialization Over
goto :menu

:: ML Banner 
:banner_display
cls
echo ========================================================================================================================
echo                                                      Install-Setup                                                     
echo ========================================================================================================================
echo.
goto :eof

:: Main Menu
:menu
call :banner_display
echo.
echo.
echo     1. Upgrade Pip Version
echo.
echo     2. Install Requirements
echo.
echo     3. Install Torch[CPU]
echo.
echo     4. First Run Setup
echo.
echo.
echo.
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo.
echo.
echo     Python Path: %PYTHON_EXE_TO_USE%
echo.
echo     Config File: %config_folder%\config.ini
echo.
echo.
echo.
echo ========================================================================================================================
set /p "choice=Selection; Menu Options (1-4), Exit Install-Setup (X): "

if "%choice%"=="1" goto upgrade_pip
if "%choice%"=="2" goto install_requirements
if "%choice%"=="3" goto install_torch
if "%choice%"=="4" goto first_run_setup
if /i "%choice%"=="X" goto exit_script

:: Invalid choice handler
echo Invalid option. Please choose a valid option.
timeout /t 2 >nul
goto menu

:: Option 1: Upgrade pip
:upgrade_pip
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

:: Option 2: Install Requirements
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

:: Option 3: Install Torch[CPU]
:install_torch
call :banner_display
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
pause
goto menu

:: Option 4: First Run Setup
:first_run_setup
call :banner_display
echo Running First Run Setup...
echo Waiting for User to Close Mantella Window...
start "" %PYTHON_EXE_TO_USE% .\main.py
:wait_loop
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    timeout /t 2 >nul
    goto :wait_loop
)
echo Created: config.ini
echo Returning to Menu
timeout /t 2 >nul
goto menu

:exit_script
echo Exiting the script... Please wait.
timeout /t 2 >nul
exit /b