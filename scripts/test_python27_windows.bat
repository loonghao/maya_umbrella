@echo off
REM Maya Umbrella Python 2.7 Windows Compatibility Test Runner
REM This batch file helps run the Python 2.7 compatibility tests on Windows

echo ========================================
echo Maya Umbrella Python 2.7 Test Runner
echo ========================================

REM Check if Python 2.7 is available
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 2.7 and add it to your PATH
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python version: %PYTHON_VERSION%

REM Check if it's Python 2.7
echo %PYTHON_VERSION% | findstr /C:"2.7" >nul
if errorlevel 1 (
    echo WARNING: This test is designed for Python 2.7
    echo Current version: %PYTHON_VERSION%
    echo Continue anyway? (y/n)
    set /p choice=
    if /i not "%choice%"=="y" exit /b 1
)

echo.
echo Running Maya Umbrella Python 2.7 compatibility tests...
echo.

REM Run the test script
python "%~dp0test_python27_windows.py"

REM Check exit code
if errorlevel 1 (
    echo.
    echo ========================================
    echo TESTS FAILED
    echo ========================================
    echo Some tests failed. Please check the output above.
) else (
    echo.
    echo ========================================
    echo ALL TESTS PASSED
    echo ========================================
    echo Maya Umbrella is compatible with Python 2.7!
)

echo.
echo Press any key to exit...
pause >nul
