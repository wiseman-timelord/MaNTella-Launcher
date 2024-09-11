:: Script: Mantella-Launcher.Bat

:: Initialization
@echo off
setlocal EnableDelayedExpansion

:: Global Variables
set "PYTHON_EXE_TO_USE="
set "CONFIG_INI_PATH="
set "config_folder="
set "ATTEMPTS=0"
set "ALL_FILES_OKAY="
set "SCRIPT_DIRECTORY_PATH="
set "model_service_used="

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

:: FIND PYTHON BLOCK, DO NOT MODIFY: START
for %%I in (
    "C:\Program Files\Python311\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
) do (
    if exist "%%~I" (
        set "PYTHON_EXE_TO_USE=%%~I"
        goto :python_found
    )
)
echo Python 3.11 not found.
echo See Install Notes.
timeout /t 3 >nul
goto :end_of_script
:python_found
echo Python 3.11 Found
timeout /t 1 >nul
:: FIND PYTHON BLOCK, DO NOT MODIFY: END

:: Config Notification
for /f "tokens=2*" %%A in ('reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Personal') do (
    set "config_folder=%%B"
)
if not defined config_folder (
    echo Error: Unable to retrieve Documents folder from the registry.
	timeout /t 3 >nul
    goto main_menu
)
set "CONFIG_INI_PATH=%config_folder%\My Games\Mantella\config.ini"
if not exist "%CONFIG_INI_PATH%" (
	echo Error: %CONFIG_INI_PATH% not found.
	echo Ensure to Run `First Run Setup`, and then edit `Documents\My Games\Mantella\config.ini`.
	timeout /t 5 >nul
    goto main_menu
)
echo Config Found: %CONFIG_INI_PATH%
timeout /t 1 >nul
goto :main_menu

:main_menu
rem cls
echo ========================================================================================================================
echo     Pre-Launcher Configuration  
echo ========================================================================================================================
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo     1. Just Run Mantella
echo.
echo     2. Mantella-Local-Launcher
echo.
echo     3. Installer-Setup
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo ========================================================================================================================
set /p "choice=Selection; Menu Options = 1-3, Exit Batch = X: "

if "%choice%"=="1" goto run_mantella
if "%choice%"=="2" goto mantella_launcher
if "%choice%"=="3" goto installer_menu
if /i "%choice%"=="X" goto end_script

echo Invalid option. Please try again.
timeout /t 2 >nul
goto main_menu

:run_mantella
cls
echo ========================================================================================================================
echo     Launching Mantella-Vanilla...                                                
echo ========================================================================================================================
echo.
timeout /t 1 >nul
call :check_config
echo Saving .\data\persistence.txt...
echo CONFIG_INI_PATH=%CONFIG_INI_PATH% > .\data\persistence.txt
echo model_service_used=standalone >> .\data\persistence.txt
timeout /t 1 >nul
echo Running Mantella...
"%PYTHON_EXE_TO_USE%" .\main.py
if errorlevel 1 (
    echo Error occurred while running Mantella.
    timeout /t 5 >nul
    goto main_menu
)
echo Mantella Exited.
pause
goto main_menu

:mantella_launcher
cls
echo ========================================================================================================================
echo     Launching Mantella-Local...                                                
echo ========================================================================================================================
echo.
timeout /t 1 >nul
call :check_config
echo Saving .\data\persistence.txt...
echo CONFIG_INI_PATH=%CONFIG_INI_PATH% > .\data\persistence.txt
echo model_service_used=standalone >> .\data\persistence.txt
echo PYTHON_EXE_TO_USE=%PYTHON_EXE_TO_USE% >> .\data\persistence.txt
timeout /t 1 >nul
echo Running Mantella Local Launcher...
"%PYTHON_EXE_TO_USE%" .\mantella_launcher.py
if errorlevel 1 (
    echo Error occurred in Mantella Local.
    echo Returning to menu in 5 seconds...
    timeout /t 5 >nul
    goto main_menu
)
goto main_menu


:installer_menu
cls
echo ========================================================================================================================
echo     Installer-Setup                                                     
echo ========================================================================================================================
echo.
echo.
echo     1. Install `.\requirements.txt`
echo.
echo     2 First Run Setup ^(Run Once^)
echo.
echo     3. Fix Ollama Non-Cuda/Non-Rocm GPU 
echo.
echo     4. Upgrade Pip Version
echo.
echo     5. Check Dependency Conflicts
echo.
echo     6. File Integrity Test
echo.
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo     Python Path:
echo         %PYTHON_EXE_TO_USE%
echo.
echo     Config File:
echo         %CONFIG_INI_PATH%
echo.
echo.
echo ========================================================================================================================
set /p "install_choice=Selection; Menu Options = 1-6, Back to Main = B: "

if "%install_choice%"=="1" goto install_requirements
if "%install_choice%"=="2" goto first_run_setup
if "%install_choice%"=="3" goto install_torch
if "%install_choice%"=="4" goto upgrade_pip
if "%install_choice%"=="5" goto check_dependencies
if "%install_choice%"=="6" goto integrity_test
if /i "%install_choice%"=="B" goto main_menu

echo Invalid option. Please try again.
timeout /t 2 >nul
goto installer_menu


:banner_install
cls
echo ========================================================================================================================
echo     Installation/Setup in Progress...                                                
echo ========================================================================================================================
echo.
goto :eof

:upgrade_pip
call :banner_install
echo Upgrading pip...
%PYTHON_EXE_TO_USE% -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip. Please check your Python installation.
    pause
    goto installer_menu
)
echo pip upgraded.
pause
goto installer_menu

:install_requirements
call :banner_install
echo Installing Requirements, Ensure Python v3.11...
"%PYTHON_EXE_TO_USE%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements. Check Python and pip installation.
    pause
    goto installer_menu
)
echo Requirements Installed.
pause
goto installer_menu

:install_requirements
call :banner_install
echo Installing Requirements, Ensure Python v3.11...
"%PYTHON_EXE_TO_USE%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements. Check Python and pip installation.
    pause
    goto installer_menu
)
echo Requirements Installed.
pause
goto installer_menu

:install_torch
call :banner_install
echo Uninstalling existing Torch packages...
%PYTHON_EXE_TO_USE% -m pip uninstall torch torchvision torchaudio -y
echo Installing Torch for CPU...
%PYTHON_EXE_TO_USE% -m pip install torch==2.0.0+cpu torchvision==0.15.1+cpu torchaudio==2.0.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo Failed to install Torch[CPU]. Please check your Python installation.
    pause
    goto installer_menu
)
echo Torch[CPU] Installed.
pause
goto installer_menu

:first_run_setup
call :banner_install
echo Ensure to edit the config.ini from the mantella-webui.
echo After doing so , then close the config and mantella.
echo 10 second delay...
timeout /t 10 >nul
echo Running First Run Setup...
timeout /t 1
echo Waiting for User to, Finish Editing and Close Mantella...
start "" %PYTHON_EXE_TO_USE% .\main.py
:wait_loop
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    timeout /t 2 >nul
    goto wait_loop
)
echo Created: config.ini
echo Returning to Menu
timeout /t 2 >nul
goto installer_menu


:integrity_test
call :banner_install
set "ALL_FILES_OKAY=true"
echo Searching for Mantella-Local-Launcher.Bat...
timeout /t 1 > nul
if exist ".\Mantella-Local-Launcher.Bat" (
    echo Found: Mantella-Local-Launcher.Bat
) else (
    echo ERROR: Mantella-Local-Launcher.Bat is missing!
    set "ALL_FILES_OKAY=false"
)
timeout /t 1 > nul
echo.
echo Searching for mantella_local_launcher.py...
timeout /t 1 > nul
if exist ".\mantella_local_launcher.py" (
    echo Found: mantella_local_launcher.py
) else (
    echo ERROR: mantella_local_launcher.py is missing!
    set "ALL_FILES_OKAY=false"
)
timeout /t 1 > nul
echo.
echo Generating report...
timeout /t 1 > nul
echo.
if "%ALL_FILES_OKAY%"=="true" (
    echo REPORT: All critical files are present and accounted for.
    echo Mantella-Launcher Files, Correct and Present.
) else (
    echo REPORT: Missing Critical Files
    echo Re-Install Mantella-Local-Launcher
)
timeout /t 2 > nul
echo.
echo Returning to main menu...
timeout /t 1 > nul
goto main_menu

:check_config
rem Retrieve Documents folder path from the correct registry key (User Shell Folders)
if exist "%CONFIG_INI_PATH%" (
    goto :eof
)
for /f "tokens=2*" %%A in ('reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Personal') do (
    set "config_folder=%%B"
)
set "CONFIG_INI_PATH=%config_folder%\My Games\Mantella\config.ini"
if not defined config_folder (
    Set "CONFIG_INI_PATH=Failed_Reading_Registry"
    goto :eof
)
if not exist "%CONFIG_INI_PATH%" (
    Set "CONFIG_INI_PATH=First_Run_Then_Edit_config.ini"
    goto :eof
)
goto :eof

:end_of_script
echo Exiting the script... Please wait.
timeout /t 2 >nul
exit /b