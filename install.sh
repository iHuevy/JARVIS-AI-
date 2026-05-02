#!/bin/bash

echo ""
echo "  ============================================"
echo "   JARVIS AI Assistant — Setup"
echo "   Made by iHuevy"
echo "  ============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "  [ERROR] Python 3 not found!"
    echo "  Install with: sudo apt install python3 (Ubuntu)"
    echo "  Or: brew install python3 (macOS)"
    exit 1
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "  [OK] Python $PY_VERSION found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "  [ERROR] pip3 not found. Installing..."
    python3 -m ensurepip --upgrade
fi

echo ""
echo "  Installing dependencies..."
echo "  (This may take a few minutes)"
echo ""

pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "  [WARNING] Some packages failed. Trying minimal install..."
    pip3 install anthropic pyttsx3 SpeechRecognition pyautogui Pillow psutil colorama python-dotenv
fi

# Linux-specific extras
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo ""
    echo "  Installing Linux audio/GUI dependencies..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y python3-tk portaudio19-dev python3-pyaudio libespeak1 espeak 2>/dev/null
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-tkinter portaudio-devel espeak 2>/dev/null
    fi
fi

echo ""
echo "  ============================================"
echo "   Setup complete!"
echo "  ============================================"
echo ""
echo "  NEXT STEPS:"
echo ""
echo "   1. Copy .env.example to .env:"
echo "      cp .env.example .env"
echo ""
echo "   2. Edit .env and add your Anthropic API key"
echo "      Get one at: https://console.anthropic.com"
echo ""
echo "   3. Run JARVIS:"
echo "      python3 main.py"
echo ""
echo "   Or for terminal mode:"
echo "      python3 main.py --nogui"
echo ""
echo "   With voice enabled:"
echo "      python3 main.py --voice"
echo ""
