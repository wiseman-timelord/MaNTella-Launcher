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
    goto :eof
)
echo Admin Status: Administrator 

:: Show Directory
echo Working Folder: %ScriptDirectoryMantella%
timeout /t 1 >nul

:: Find Config
if exist ".\config.ini" (
    set "mantella_version=v11.4"
) else if exist "%USERPROFILE%\Documents\My Games\Mantella\config.ini" (
    set "mantella_version=v12"
) else (
    echo Error: File Missing: config.ini
    timeout /t 3 >nul
    goto :end_of_file
)
echo.
timeout /t 2 >nul
	
:: Display Is Reset
cls
echo ========================================================================================================================
echo                                                          Mantella %mantella_version%
echo ------------------------------------------------------------------------------------------------------------------------
echo.

:: Running Mantella
echo Running Mantella...
timeout /t 1 >nul
python .\main.py
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
