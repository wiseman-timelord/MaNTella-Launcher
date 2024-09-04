@echo off
setlocal EnableDelayedExpansion

:: Initialization
set "ScriptDirectoryWt=%~dp0"
set "ScriptDirectoryWt=%ScriptDirectoryWt:~0,-1%"
pushd "%ScriptDirectoryWt%"
echo Working Dir: %ScriptDirectoryWt%

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Error: Admin Required!
    echo Right Click, then Run As Administrator.
    timeout /t 3 >nul
    goto :eof
)

:: Global Variables
set "PYTHON_EXE_TO_USE="

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

:: Display Is Reset
cls
echo ========================================================================================================================
echo                                        Mantella-Local-Launcher For Mantella v11.4
echo ------------------------------------------------------------------------------------------------------------------------
echo.
timeout /t 1 >nul

echo Admin Status: Administrator 

:: First run check and requirement installation
if not exist ".\config.bak" (
    echo First Run, Fool-Proofing Mantella..
    timeout /t 1 >nul
    "%PYTHON_EXE_TO_USE%" -m pip install -r requirements.txt
    echo ..Requirements Installed ^(Hopefully^).
    timeout /t 2 >nul
)
echo Note: 'config.bak' Retains Instructions.

:: Load configuration from multiple locations
set "config_file="
if exist ".\config.ini" (
    set "config_file=.\config.ini"
) else if exist "%USERPROFILE%\Documents\Mantella\config.ini" (
    set "config_file=%USERPROFILE%\Documents\Mantella\config.ini"
) else if exist "C:\Mantella\config.ini" (
    set "config_file=C:\Mantella\config.ini"
)

if defined config_file (
    echo Config Loaded: %config_file%
    timeout /t 1 >nul
) else (
    echo Error: No configuration file found.
    echo Please ensure a config.ini exists in one of the expected locations.
    timeout /t 3 >nul
    goto :eof
)

:: Check if LM Studio or Ollama is running, act appropriately.
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
        goto :eof
    ) else (
        echo service=lmstudio > .\data\temporary_batch.txt
        echo LM Studio Status: Running
        timeout /t 1 >nul
    )
) else if "%OLLAMA_RUNNING%"=="1" (
    echo service=ollama > .\data\temporary_batch.txt
    echo Ollama Status: Running
    timeout /t 1 >nul    
) else (
    echo Error: Neither LM Studio nor Ollama is running.
    echo Load one of the Language Models and try again.
    timeout /t 3 >nul
    goto :eof
)

:: Run the Python script for config cleaning and menu
echo Running Mantella-Local-Launcher...
"%PYTHON_EXE_TO_USE%" launcher.py
echo ...Mantella-Local-Launcher Closed.
timeout /t 1 >nul

:: Read the output values from .\data\temporary_batch.txt
for /f "tokens=1,2 delims==" %%i in (.\data\temporary_batch.txt) do (
    if "%%i"=="exit_code" set exit_code=%%j
    if "%%i"=="xvasynth_folder" set xvasynth_folder=%%j
    if "%%i"=="game" set game=%%j
    if "%%i"=="game_folder" set game_folder=%%j
)
echo Read File: .\data\temporary_batch.txt
timeout /t 1 >nul
if "%exit_code%" equ "1" (
    echo Exit and Save Complete. 
    goto :eof
)
timeout /t 1 >nul

:: Check if the game is running and start if necessary
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
        timeout /t 1 >nul
        powershell -Command "Start-Process '%game_folder%\%game_se%' -NoNewWindow"
        popd
    ) else (
        echo Error: %game_se% not found at %game_folder%
        echo Check, config.ini game path and Script Extender presence.
        timeout /t 3 >nul
        goto :eof
    )
    timeout /t 3 >nul
)

:: Check if xVASynth.exe is running and start if necessary
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
        goto :eof
    )
    timeout /t 3 >nul
)

timeout /t 1 >nul

:: Running Mantella
echo Running Mantella...
timeout /t 1 >nul
"%PYTHON_EXE_TO_USE%" .\main.py

:: Cleanup and exit
echo Mantella Exited.
timeout /t 1 >nul

:eof
:: Exit Program
del .\.\data\temporary_batch.txt
echo File Deleted: .\data\temporary_batch.txt
timeout /t 1 >nul
pushd "%ScriptDirectoryWt%"
echo Closing in 15 seconds...
timeout /t 15 >nul
exit /b
