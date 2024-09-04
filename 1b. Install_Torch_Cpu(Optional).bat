@echo off

:: Global Variables
set PYTHON_EXE_TO_USE=""
set ATTEMPTS=0

:find_python
:: Check for python.exe in the specified locations
if exist "C:\Program Files\Python311\python.exe" (
    set PYTHON_EXE_TO_USE="C:\Program Files\Python311\python.exe"
) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON_EXE_TO_USE="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
) else (
    echo Python not found in the specified locations.
    set /p PYTHON_EXE_TO_USE="Please enter the full path to python.exe (including python.exe): "
    
    :: Check if the user-provided path exists
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
)

:: Reset attempts if a valid path is found
set ATTEMPTS=0

:: Use python.exe -m pip to uninstall and install packages
%PYTHON_EXE_TO_USE% -m pip uninstall torch torchvision torchaudio -y
%PYTHON_EXE_TO_USE% -m pip install torch==2.0.0+cpu torchvision==0.15.1+cpu torchaudio==2.0.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu

:: End Of Script
pause
