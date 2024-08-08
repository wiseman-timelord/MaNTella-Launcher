@echo off
setlocal EnableDelayedExpansion

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
