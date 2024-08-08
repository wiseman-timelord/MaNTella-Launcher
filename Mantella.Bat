@echo off
setlocal EnableDelayedExpansion

:: Display Is Reset
cls
echo ========================================================================================================================
echo                                                         Mantella
echo ------------------------------------------------------------------------------------------------------------------------
echo.
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
