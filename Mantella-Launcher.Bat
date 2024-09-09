:: Script: Mantella-Launcher.Bat

:: Initialization
@echo off
setlocal EnableDelayedExpansion

:: Global Variables
set "PYTHON_EXE_TO_USE="
set "CONFIG_INI_PATH="
set "ATTEMPTS=0"
set "ALL_FILES_OKAY="

:main_menu
cls
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
if "%choice%"=="3" goto installer_setup
if /i "%choice%"=="X" goto end_script

echo Invalid option. Please try again.
timeout /t 2 >nul
goto main_menu

:run_mantella
call :admin_check
call :find_python
call :check_config
echo Running Mantella...
"%PYTHON_EXE_TO_USE%" .\main.py
if errorlevel 1 (
    echo Error occurred while running Mantella.
    pause
    goto main_menu
)
echo Mantella Exited.
pause
goto main_menu

:mantella_launcher
call :admin_check
call :find_python
call :check_config
call :check_lm_ollama
if "%exit_code%"=="1" goto main_menu
call :check_game
call :check_xvasynth
echo Running Mantella...
"%PYTHON_EXE_TO_USE%" .\main.py
echo Mantella Exited.
del .\data\temporary_batch.txt
echo File Deleted: .\data\temporary_batch.txt
pause
goto main_menu

:installer_setup
call :admin_check
call :find_python
:installer_menu
cls
echo ========================================================================================================================
echo     Installer-Setup                                                     
echo ========================================================================================================================
echo.
echo.
echo.
echo.
echo.
echo.
echo     1. Install `.\requirements.txt`
echo.
echo     2. Install Torch[CPU]
echo.
echo     3. First Run Setup
echo.
echo     4. Upgrade Pip Version
echo.
echo     5. Check Dependency Conflicts
echo.
echo     6. File Integrity Test
echo.
echo.
echo.
echo.
echo.
echo.
echo ========================================================================================================================
set /p "install_choice=Selection; Menu Options = 1-6, Back to Main = B: "

if "%install_choice%"=="1" goto install_requirements
if "%install_choice%"=="2" goto install_torch
if "%install_choice%"=="3" goto first_run_setup
if "%install_choice%"=="4" goto upgrade_pip
if "%install_choice%"=="5" goto check_dependencies
if "%install_choice%"=="6" goto integrity_test
if /i "%install_choice%"=="B" goto main_menu

echo Invalid option. Please try again.
timeout /t 2 >nul
goto installer_menu

:upgrade_pip
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
echo Running First Run Setup...
echo Waiting for User to Close Mantella Window...
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
cls
echo ========================================================================================================================
echo     File Integrity Check
echo ========================================================================================================================
echo.
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

:admin_check
net session >nul 2>&1 || (
    echo Error: Admin privileges required. Right-click and select "Run as administrator".
    timeout /t 3 >nul
    goto main_menu
)
echo Status: Administrator
set "SCRIPT_DIRECTORY_PATH=%~dp0"
set "SCRIPT_DIRECTORY_PATH=%SCRIPT_DIRECTORY_PATH:~0,-1%"
pushd "%SCRIPT_DIRECTORY_PATH%"
echo Path Dp0'd To Script.
goto :eof

:find_python
for %%I in (
    "C:\Program Files\Python311\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
) do (
    if exist "%%~I" (
        set "PYTHON_EXE_TO_USE=%%~I"
        goto :python_found
    )
)
echo Python 3.11 not found. Please install it before running this script.
timeout /t 3 >nul
goto main_menu
:python_found
echo Python 3.11 Found
goto :eof

:check_config
for /f "usebackq tokens=3*" %%A in (`reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Personal`) do (
    set "CONFIG_INI_PATH=%%A\My Games\Mantella\config.ini"
)
set "CONFIG_INI_PATH=%CONFIG_INI_PATH:/=\%"
if not exist "%CONFIG_INI_PATH%" (
    echo First Run Detected. Please run Install-Setup first!
    timeout /t 3 >nul
    goto main_menu
)
echo Found Config File.
goto :eof

:check_lm_ollama
tasklist /FI "IMAGENAME eq LM Studio.exe" 2>NUL | find /I /N "LM Studio.exe" >NUL
if "%ERRORLEVEL%" EQU "0" (
    set "LM_RUNNING=1"
) else (
    set "LM_RUNNING=0"
)

tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe" >NUL
if "%ERRORLEVEL%" EQU "0" (
    set "OLLAMA_RUNNING=1"
) else (
    set "OLLAMA_RUNNING=0"
)

if "%LM_RUNNING%"=="1" (
    if "%OLLAMA_RUNNING%"=="1" (
        echo Error: Multiple Model Servers
        echo Please run, Ollama or LM Studio, not both
        timeout /t 3 >nul
        set "exit_code=1"
        goto :eof
    ) else (
        echo service=lmstudio > .\data\temporary_batch.txt
        echo LM Studio Status: Running
    )
) else if "%OLLAMA_RUNNING%"=="1" (
    echo service=ollama > .\data\temporary_batch.txt
    echo Ollama Status: Running
) else (
    echo Error: Neither LM Studio nor Ollama is running.
    echo Load one of the Language Models and try again.
    timeout /t 3 >nul
    set "exit_code=1"
    goto :eof
)
goto :eof

:check_game
for /f "tokens=1,2 delims==" %%i in (.\data\temporary_batch.txt) do (
    if "%%i"=="game" set game=%%j
    if "%%i"=="game_folder" set game_folder=%%j
)
echo Checking for %game%...
if "%game%"=="Fallout4" (
    if exist "%game_folder%\f4se_loader.exe" (
        set "game_se=f4se_loader.exe"
        set "game_exe=Fallout4.exe"
    )
) else if "%game%"=="Fallout4VR" (
    if exist "%game_folder%\f4sevr_loader.exe" (
        set "game_se=f4sevr_loader.exe"
        set "game_exe=Fallout4VR.exe"
    )
) else if "%game%"=="Skyrim" (
    if exist "%game_folder%\skse64_loader.exe" (
        set "game_se=skse64_loader.exe"
        set "game_exe=SkyrimSE.exe"
    )
) else if "%game%"=="SkyrimVR" (
    if exist "%game_folder%\sksevr_loader.exe" (
        set "game_se=sksevr_loader.exe"
        set "game_exe=SkyrimVR.exe"
    )
)
tasklist /FI "IMAGENAME eq %game_exe%" 2>NUL | find /I /N "%game_exe%">NUL
if "%ERRORLEVEL%" NEQ "0" (
    echo %game_exe% is not running. Starting %game%...
    if exist "%game_folder%\%game_se%" (
        pushd "%game_folder%"
        echo Found and Running, %game_se%.
        powershell -Command "Start-Process '%game_folder%\%game_se%' -NoNewWindow"
        popd
    ) else (
        echo Error: %game_se% not found at %game_folder%
        echo Check, config.ini game path and Script Extender presence.
        timeout /t 3 >nul
        goto main_menu
    )
    timeout /t 3 >nul
)
goto :eof

:check_xvasynth
for /f "tokens=1,2 delims==" %%i in (.\data\temporary_batch.txt) do (
    if "%%i"=="xvasynth_folder" set xvasynth_folder=%%j
)
echo Checking for xVASynth...
tasklist /FI "IMAGENAME eq xVASynth.exe" 2>NUL | find /I /N "xVASynth.exe">NUL
if "%ERRORLEVEL%" NEQ "0" (
    echo xVASynth.exe is not running. Starting xVASynth...
    if exist "%xvasynth_folder%\xVASynth.exe" (
        pushd "%xvasynth_folder%"
        powershell -Command "Start-Process '%xvasynth_folder%\xVASynth.exe'"
        popd
    ) else (
        echo Error: xVASynth.exe not found.
        echo Check config.ini xvasynth path validity.
        timeout /t 3 >nul
        goto main_menu
    )
    timeout /t 3 >nul
)
goto :eof

:end_script
echo Exiting the script... Please wait.
timeout /t 2 >nul
exit /b