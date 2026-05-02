@echo off
TITLE JARVIS AI — Installer
color 0B

echo.
echo  ============================================
echo   JARVIS AI Assistant - Setup
echo   Made by iHuevy
echo  ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python not found!
    echo  Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo  [OK] Python found
echo.

:: Check pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] pip not found. Please reinstall Python.
    pause
    exit /b 1
)

echo  Installing dependencies...
echo  (This may take a few minutes)
echo.

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo  [WARNING] Some packages failed. Trying minimal install...
    pip install anthropic pyttsx3 SpeechRecognition pyautogui Pillow psutil colorama python-dotenv
)

echo.
echo  ============================================
echo   Setup complete!
echo  ============================================
echo.
echo  NEXT STEPS:
echo.
echo   1. Copy .env.example to .env
echo      copy .env.example .env
echo.
echo   2. Edit .env and add your Anthropic API key
echo      Get one at: https://console.anthropic.com
echo.
echo   3. Run JARVIS:
echo      python main.py
echo.
echo   Or for terminal mode:
echo      python main.py --nogui
echo.
echo   With voice enabled:
echo      python main.py --voice
echo.
pause
