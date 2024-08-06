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

:: First run check and requirement installation
if not exist "%USERPROFILE%\Documents\My Games\Mantella\config.bak" (
    echo First Run, Fool-Proofing Mantella...
    timeout /t 1 >nul
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install requirements. Check Python and pip installation.
        goto eof
    )
    echo ..Requirements Installed ^(Hopefully^).
    timeout /t 2 >nul

    :: Backup config.ini to config.bak
    if exist "%USERPROFILE%\Documents\My Games\Mantella\config.ini" (
        echo Creating backup of config.ini...
        copy /Y "%USERPROFILE%\Documents\My Games\Mantella\config.ini" "%USERPROFILE%\Documents\My Games\Mantella\config.bak" >nul
        echo Backup created: config.bak
    ) else (
        echo Warning: config.ini not found. No backup created.
    )
)

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
