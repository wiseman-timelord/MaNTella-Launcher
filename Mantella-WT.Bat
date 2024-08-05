@echo off
setlocal EnableDelayedExpansion

:: Change to the script's directory
set "ScriptDirectoryWt=%~dp0"
set "ScriptDirectoryWt=%ScriptDirectoryWt:~0,-1%"
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
    echo Error: Admin Required!
    echo Right Click, then Run As Administrator.
    timeout /t 3 >nul
    goto :eof
)
echo Admin Status: Administrator 

:: First run check and requirement installation
if not exist ".\config.bak" (
    echo First Run, Fool-Proofing Mantella..
    timeout /t 1 >nul
    pip install -r requirements.txt
	echo ..Requirements Installed ^(Hopefully^).
	timeout /t 2 >nul
)
echo Note: 'config.bak' Retains Instructions.

:: Check if LM Studio is running
tasklist /FI "IMAGENAME eq LM Studio.exe" 2>NUL | find /I /N "LM Studio.exe">NUL
if "%ERRORLEVEL%" EQU "0" (
    set "LM_RUNNING=1"
) else (
    set "LM_RUNNING=0"
)

:: Determine service status and save to temp-wt.txt
if "%LM_RUNNING%"=="1" (
    echo service=lmstudio > temp-wt.txt
	echo LM Studio Status: Running 
) else (
    echo Error: LM Studio Must Be Running.
    echo Load the Language Model In LM Studio, and Try Again.
    timeout /t 5 >nul
    popd
    exit /b
)

:: Run the Python script for config cleaning and menu
echo Running Mantella-WT Optimizer-Launcher...
python main-wt.py
echo ...Mantella/xVASynth Optimizer-Launcher Closed.
timeout /t 1 >nul

:: Read the output values from temp-wt.txt
for /f "tokens=1,2 delims==" %%i in (temp-wt.txt) do (
    if "%%i"=="exit_code" set exit_code=%%j
    if "%%i"=="xvasynth_folder" set xvasynth_folder=%%j
    if "%%i"=="game" set game=%%j
    if "%%i"=="game_folder" set game_folder=%%j
)
echo Read File: temp-wt.txt
timeout /t 1 >nul
if "%exit_code%" equ "1" (
    echo Exit and Save Complete. 
    goto eof:
)
timeout /t 1 >nul

:: Check if the game is running and start if necessary
echo Checking for %game%...
if "%game%"=="Fallout4" (
    if exist "%game_folder%\f4se_loader.exe" (
        set "game_exe=f4se_loader.exe"
    ) else (
        set "game_exe=Fallout4.exe"
    )
) else if "%game%"=="Fallout4VR" (
    if exist "%game_folder%\f4sevr_loader.exe" (
        set "game_exe=f4sevr_loader.exe"
    ) else (
        set "game_exe=Fallout4VR.exe"
    )
) else if "%game%"=="Skyrim" (
    if exist "%game_folder%\skse64_loader.exe" (
        set "game_exe=skse64_loader.exe"
    ) else (
        set "game_exe=SkyrimSE.exe"
    )
) else if "%game%"=="SkyrimVR" (
    if exist "%game_folder%\sksevr_loader.exe" (
        set "game_exe=sksevr_loader.exe"
    ) else (
        set "game_exe=SkyrimVR.exe"
    )
)

tasklist /FI "IMAGENAME eq %game_exe%" 2>NUL | find /I /N "%game_exe%">NUL
if "%ERRORLEVEL%" NEQ "0" (
    echo %game_exe% is not running. Starting %game%...
    if exist "%game_folder%\%game_exe%" (
        pushd "%game_folder%"
        echo Found and running %game_exe%.
        timeout /t 1 >nul
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
    if exist "%xvasynth_folder%\xVASynth.exe" (
        pushd "%xvasynth_folder%"
        powershell -Command "Start-Process '%xvasynth_folder%\xVASynth.exe'"
        popd
    ) else (
        echo Error: xVASynth.exe not found at %xvasynth_folder%
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

:eof
:: Exit Program
del .\temp-wt.txt
echo File Deleted: temp-wt.txt
pushd "%ScriptDirectoryWt%"
echo Closing in 5 seconds...
rem timeout /t 5 >nul
exit /b
