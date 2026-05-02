# JARVIS AI Desktop Assistant
### Just A Rather Very Intelligent System
**Made by iHuevy** · Powered by Claude AI (Anthropic)

```
    ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
    ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
    ██║███████║██████╔╝██║   ██║██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
```

---

## Features

| Category | Capabilities |
|---|---|
| **Voice** | Wake word detection, speech-to-text, text-to-speech |
| **Files** | Read, search, organize, edit, delete files & folders |
| **Apps** | Open and close any application by name |
| **Screen** | Capture screenshots, analyze what you're working on |
| **PC Clean** | Remove temp files, browser cache, recycle bin |
| **Messaging** | Send emails, desktop notifications, open WhatsApp |
| **Timers** | Countdown timers, reminders, Pomodoro sessions |
| **Code** | Read, write, edit, run Python scripts and code files |
| **System** | CPU/RAM/Disk monitoring, kill processes, set volume |
| **Web** | Search the web, weather, currency, word definitions |
| **Extras** | Quick notes, jokes, motivation quotes, calculator |
| **AI Chat** | Full conversation with memory via Claude |

---

## Quick Start

### 1. Requirements
- Python 3.10 or later
- An Anthropic API key → https://console.anthropic.com

### 2. Install

**Windows:**
```bat
install.bat
```

**Linux / macOS:**
```bash
chmod +x install.sh
./install.sh
```

**Manual:**
```bash
pip install -r requirements.txt
```

### 3. Configure

Copy the example config and edit it:
```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Open `.env` and fill in at minimum:
```env
ANTHROPIC_API_KEY=your_key_here
```

### 4. Run

```bash
# With GUI (default)
python main.py

# Terminal only (no GUI)
python main.py --nogui

# Enable wake-word voice from startup
python main.py --voice

# Quick launch (Windows)
run.bat

# Quick launch (Linux/macOS)
./run.sh
```

---

## Voice Commands

Say **"JARVIS"** followed by your command:

| Say | JARVIS does |
|---|---|
| "JARVIS open Chrome" | Launches Chrome |
| "JARVIS close Spotify" | Closes Spotify |
| "JARVIS take a screenshot" | Captures + analyzes screen |
| "JARVIS clean my PC" | Scans and removes junk files |
| "JARVIS set a 25-minute timer" | Countdown timer |
| "JARVIS read my Downloads folder" | Lists files |
| "JARVIS send email to john@..." | Opens email compose |
| "JARVIS how much RAM am I using?" | System info |
| "JARVIS search for Python tutorials" | Web search |
| "JARVIS tell me a joke" | 😄 |

---

## Text Commands (GUI / Terminal)

Type anything naturally. JARVIS understands:

```
open vscode
close discord
organize my Downloads folder
take a screenshot and tell me what you see
set a reminder at 14:30 to drink water
read the file ~/Documents/notes.txt
clean temp files
what's the weather in London
convert 100 USD to EUR
show system info
run ~/scripts/backup.py
help
```

---

## Project Structure

```
JARVIS/
├── main.py               ← Entry point
├── .env                  ← Your config (create from .env.example)
├── .env.example          ← Config template
├── requirements.txt      ← Python dependencies
├── install.bat           ← Windows installer
├── install.sh            ← Linux/macOS installer
├── run.bat               ← Windows quick launch
├── run.sh                ← Linux/macOS quick launch
│
├── jarvis/
│   ├── core.py           ← Claude AI brain
│   ├── gui.py            ← Neon GUI window
│   ├── voice.py          ← TTS + STT
│   ├── dispatcher.py     ← Action routing
│   ├── apps.py           ← App open/close
│   ├── files.py          ← File management
│   ├── screen.py         ← Screen capture + control
│   ├── cleaner.py        ← PC cleaning
│   ├── messaging.py      ← Email + notifications
│   ├── timers.py         ← Timers + reminders
│   ├── code_helper.py    ← Code editing + running
│   ├── system.py         ← System monitoring
│   ├── web_search.py     ← Web search + APIs
│   └── extras.py         ← Bonus features
│
├── assets/
│   └── icon_gen.py       ← Neon icon generator
│
└── logs/
    └── jarvis.log        ← Runtime logs
```

---

## Configuration Reference

Edit `.env` to customize JARVIS:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Voice
WAKE_WORD=jarvis
VOICE_RATE=175
VOICE_VOLUME=1.0
VOICE_ID=0

# Email (for send_email feature)
EMAIL_ADDRESS=you@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

# Screen watching (JARVIS monitors your screen proactively)
ENABLE_SCREEN_WATCH=false
SCREEN_WATCH_INTERVAL=10
```

> **Gmail users**: Use an App Password, not your main password.
> Enable at: Google Account → Security → 2-Step Verification → App Passwords

---

## Troubleshooting

**"ANTHROPIC_API_KEY not found"**
→ Make sure `.env` exists and contains your key.

**Voice not working**
→ Install: `pip install SpeechRecognition pyttsx3`
→ Linux also needs: `sudo apt install espeak portaudio19-dev`

**pyautogui fails (screen capture)**
→ Linux: `sudo apt install python3-tk python3-dev`
→ macOS: Grant screen recording permission in System Preferences

**GUI won't open**
→ Run `python main.py --nogui` to use terminal mode instead.

---

## License

MIT — Free to use, modify, and distribute.
Built with ❤️ by **iHuevy**

---

*JARVIS is not affiliated with Marvel, Disney, or Iron Man (unfortunately).*
