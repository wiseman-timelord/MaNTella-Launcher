@echo off
setlocal EnableDelayedExpansion

:: Remove trailing backslash from ScriptDirectoryWt
set "ScriptDirectoryWt=%~dp0"
set "ScriptDirectoryWt=%ScriptDirectoryWt:~0,-1%"

:: Change to the script's directory
pushd "%ScriptDirectoryWt%"

:: Display Is Reset
cls
echo ========================================================================================================================
echo                                             Mantella-WT Optimizer/Launcher
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo Working Dir: %ScriptDirectoryWt%
timeout /t 1 >nul

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo This script requires administrative privileges. 
    echo Right click and run as an administrator.
    echo This script exits in 15 seconds...
    timeout /t 15 >nul
    popd
    exit /b
)

:: Check if LM Studio is running
tasklist /FI "IMAGENAME eq LM Studio.exe" 2>NUL | find /I /N "LM Studio.exe">NUL
if "%ERRORLEVEL%" EQU "0" (
    set "LM_RUNNING=1"
) else (
    set "LM_RUNNING=0"
)

:: Check for Ollama
set "OLLAMA_RUNNING=0"
set "OLLAMA_LOADED=0"
ollama ps > ollama_output.txt 2>&1
if %ERRORLEVEL% EQU 0 (
    set "OLLAMA_RUNNING=1"
    findstr /C:"NAME    ID      SIZE    PROCESSOR       UNTIL" ollama_output.txt >nul
    if !ERRORLEVEL! EQU 0 (
        find /v /c "" ollama_output.txt > count.txt
        set /p LINE_COUNT=<count.txt
        if !LINE_COUNT! GTR 1 (
            set "OLLAMA_LOADED=1"
        )
    )
)
del ollama_output.txt count.txt 2>nul

:: Determine which service to use and save to main-wt.txt
if "%LM_RUNNING%"=="1" (
    echo service=lmstudio > main-wt.txt
) else if "%OLLAMA_LOADED%"=="1" (
    echo service=ollama > main-wt.txt
) else (
    echo Requirement: LM Studio or Ollama, with Loaded Model
    powershell -c "(New-Object Media.SoundPlayer 'C:\Windows\Media\Windows Balloon.wav').PlaySync()"
    echo Load the Language Model, and Try Again.
    timeout /t 5 >nul
    popd
    exit /b
)

:: Run the Python script for config cleaning and menu
echo Running Mantella-WT Optimizer-Launcher...
python main-wt.py
echo ...Mantella/xVASynth Optimizer-Launcher Closed...
timeout /t 1 >nul

:: Debug
pause

:: Display Is Reset
cls
echo ========================================================================================================================
echo                                             Mantella-WT Optimizer/Launcher
echo ------------------------------------------------------------------------------------------------------------------------
echo.
echo Working Dir: %ScriptDirectoryWt%
timeout /t 1 >nul

:: Read the output values from main-wt.txt
for /f "tokens=1,2 delims==" %%i in (main-wt.txt) do (
    if "%%i"=="exit_code" set exit_code=%%j
    if "%%i"=="xvasynth_path" set xvasynth_path=%%j
    if "%%i"=="game" set game=%%j
    if "%%i"=="game_folder" set game_folder=%%j
)

if "%exit_code%" equ "1" (
    echo User chose to exit. Closing in 5 seconds...
    timeout /t 5 >nul
    popd
    exit /b
)

:: Check if the game is running and start if necessary
echo Checking for %game%...
if "%game%"=="Fallout4" (
    set "game_exe=Fallout4.exe"
) else if "%game%"=="Fallout4VR" (
    set "game_exe=Fallout4VR.exe"
) else if "%game%"=="Skyrim" (
    set "game_exe=SkyrimSE.exe"
) else if "%game%"=="SkyrimVR" (
    set "game_exe=SkyrimVR.exe"
)

tasklist /FI "IMAGENAME eq %game_exe%" 2>NUL | find /I /N "%game_exe%">NUL
if "%ERRORLEVEL%" NEQ "0" (
    echo %game_exe% is not running. Starting %game%...
    if exist "%game_folder%\%game_exe%" (
        pushd "%game_folder%"
        powershell -Command "Start-Process '%game_folder%\%game_exe%' -NoNewWindow"
        popd
    ) else (
        echo Error: %game_exe% not found at %game_folder%
        echo Please check your config.ini file and ensure the game folder path is correct.
        timeout /t 10 >nul
        popd
        exit /b
    )
    timeout /t 3 >nul
)

:: Check if xVASynth.exe is running and start if necessary
echo Checking for xVASynth...
tasklist /FI "IMAGENAME eq xVASynth.exe" 2>NUL | find /I /N "xVASynth.exe">NUL
if "%ERRORLEVEL%" NEQ "0" (
    echo xVASynth.exe is not running. Starting xVASynth...
    if exist "%xvasynth_path%\xVASynth.exe" (
        pushd "%xvasynth_path%"
        powershell -Command "Start-Process '%xvasynth_path%\xVASynth.exe' -NoNewWindow"
        popd
    ) else (
        echo Error: xVASynth.exe not found at %xvasynth_path%
        echo Please check your config.ini file and ensure the xvasynth_folder path is correct.
        timeout /t 10 >nul
        popd
        exit /b
    )
    timeout /t 3 >nul
)

timeout /t 1 >nul

:: Running Mantella
echo Running Mantella...
timeout /t 1 >nul
python .\main.py

:: Cleanup and exit
echo Mantella Exited.
timeout /t 10 >nul

:: Return to the original directory
popd
exit /b