"""
JARVIS Main Entry Point — Orchestrates all modules and starts the assistant.

Usage:
    python main.py              # Launch with GUI
    python main.py --nogui      # Terminal-only mode
    python main.py --voice      # Enable voice from startup
"""

import os
import sys
import logging
import threading
import argparse
from pathlib import Path

# ── Setup logging ────────────────────────────────────────────────────────────
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "jarvis.log"),
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger("JARVIS")

# ── Load .env ────────────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        example = Path(__file__).parent / ".env.example"
        if example.exists():
            import shutil
            shutil.copy(str(example), str(env_path))
            print("[JARVIS] Created .env from .env.example — please add your ANTHROPIC_API_KEY!")
    load_dotenv(env_path)
except ImportError:
    pass


# ── Banner ───────────────────────────────────────────────────────────────────
BANNER = """
\033[36m
    ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
    ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
    ██║███████║██████╔╝██║   ██║██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
\033[0m
\033[90mJust A Rather Very Intelligent System — v2.0
\033[36mMade by iHuevy\033[90m  |  Powered by Claude AI\033[0m
"""


class JARVIS:
    """
    Main JARVIS orchestrator.
    Coordinates: Core AI, Voice, GUI, and Action Dispatcher.
    """

    def __init__(self, nogui: bool = False, voice_enabled: bool = False):
        self.nogui = nogui
        self.voice_enabled = voice_enabled
        self.gui = None
        self.core = None
        self.voice = None
        self.dispatcher = None
        self._running = True

    def start(self):
        """Initialize all systems and start JARVIS."""
        print(BANNER)
        logger.info("Starting JARVIS...")

        # ── Check API key ─────────────────────────────────────────────────────
        if not os.getenv("ANTHROPIC_API_KEY"):
            print("\033[31m[ERROR] ANTHROPIC_API_KEY not set in .env file!\033[0m")
            print("  1. Open the .env file")
            print("  2. Replace 'your_anthropic_api_key_here' with your key")
            print("  3. Get a key at: https://console.anthropic.com\n")
            if self.nogui:
                sys.exit(1)

        # ── Init core AI ─────────────────────────────────────────────────────
        logger.info("Initializing AI brain...")
        try:
            from jarvis.core import JARVISCore
            self.core = JARVISCore()
            logger.info("✓ AI Brain online")
        except Exception as e:
            logger.error(f"Core AI init failed: {e}")
            self.core = None

        # ── Init voice ────────────────────────────────────────────────────────
        logger.info("Initializing voice systems...")
        try:
            from jarvis.voice import VoiceEngine
            self.voice = VoiceEngine()
            logger.info("✓ Voice systems online")
        except Exception as e:
            logger.warning(f"Voice init failed (optional): {e}")
            self.voice = None

        # ── Init dispatcher ───────────────────────────────────────────────────
        speak_fn = self.voice.speak if self.voice else (lambda t: print(f"[JARVIS] {t}"))
        from jarvis.dispatcher import ActionDispatcher
        self.dispatcher = ActionDispatcher(speak_callback=speak_fn)
        logger.info("✓ Action dispatcher ready")

        # ── Start screen watcher (optional) ──────────────────────────────────
        screen_watch = os.getenv("ENABLE_SCREEN_WATCH", "false").lower() == "true"
        if screen_watch and self.core:
            self._start_screen_watcher()

        # ── Start voice wake word (optional) ─────────────────────────────────
        if self.voice_enabled and self.voice:
            self.voice.listen_for_wake_word(self._handle_voice_command)
            logger.info(f"✓ Wake word '{self.voice.wake_word}' active")

        # ── Launch GUI or terminal ────────────────────────────────────────────
        if self.nogui:
            self._run_terminal()
        else:
            self._run_gui()

    def _handle_input(self, text: str):
        """Process user text input through the AI pipeline."""
        if not text.strip():
            return

        logger.info(f"User: {text}")

        # Update GUI status
        if self.gui:
            self.gui.set_thinking(True)

        try:
            # Check for direct commands first (bypass AI for speed)
            direct = self._handle_direct_command(text)
            if direct is not None:
                self._respond(direct)
                return

            # Pass to Claude for AI reasoning
            if self.core:
                response, actions = self.core.think(text)

                # Execute any actions Claude requested
                if actions:
                    results = self.dispatcher.dispatch_all(actions)
                    # Summarize results and optionally re-ask Claude
                    context_parts = []
                    for action, result in zip(actions, results):
                        context_parts.append(
                            f"Action '{action['action']}': "
                            f"{'✓ ' + str(result)[:200] if result.get('success') else '✗ ' + result.get('error', 'failed')}"
                        )
                    if context_parts:
                        context = "\n".join(context_parts)
                        # Get Claude to interpret results
                        followup, _ = self.core.think(
                            f"Action results:\n{context}\nPlease provide a natural language response about what was done.",
                        )
                        response = followup or response

                self._respond(response)
            else:
                self._respond("I'm experiencing issues with my AI core. Please check your API key in .env")

        except Exception as e:
            logger.error(f"Input handling error: {e}")
            self._respond(f"I encountered an error: {str(e)}")
        finally:
            if self.gui:
                self.gui.set_thinking(False)

    def _respond(self, text: str):
        """Output a response via GUI and/or voice."""
        logger.info(f"JARVIS: {text[:100]}...")
        if self.gui:
            self.gui.add_jarvis_message(text)
        if self.voice:
            self.voice.speak(text)
        else:
            print(f"\n\033[36m[JARVIS]\033[0m {text}\n")

    def _handle_direct_command(self, text: str) -> str | None:
        """Handle simple direct commands for speed."""
        text_lower = text.lower().strip()

        if text_lower in ["quit", "exit", "goodbye", "bye"]:
            self._respond("Shutting down all systems. Goodbye.")
            self._running = False
            if self.gui:
                self.gui.root.after(1500, self.gui.root.destroy)
            return "Initiating shutdown sequence."

        if text_lower in ["clear", "reset", "new conversation"]:
            if self.core:
                self.core.reset_conversation()
            return "Conversation history cleared. Starting fresh."

        if text_lower in ["help", "what can you do"]:
            return (
                "I can help you with:\n"
                "• File management — read, search, organize files\n"
                "• App control — open or close any application\n"
                "• Screen capture — take screenshots and analyze them\n"
                "• PC cleaning — free up disk space\n"
                "• Messaging — send emails and notifications\n"
                "• Timers — set countdowns and reminders\n"
                "• Code editing — read, write, and run code\n"
                "• System monitoring — CPU, RAM, disk, battery\n"
                "• General AI chat — just talk to me!"
            )

        return None

    def _handle_voice_command(self, text: str):
        """Handle voice input from wake word detection."""
        logger.info(f"Voice command: {text}")
        if self.gui:
            self.gui.add_user_message(f"[VOICE] {text}")
        self._handle_input(text)

    def _handle_screenshot_request(self):
        """Take screenshot and analyze it."""
        if self.gui:
            self.gui.add_system_message("Capturing screen...", "info")

        from jarvis.screen import ScreenWatcher
        watcher = ScreenWatcher()
        b64 = watcher.capture()

        if b64 and self.core:
            if self.gui:
                self.gui.set_thinking(True)
            response, actions = self.core.think(
                "I've taken a screenshot. Please analyze what's on screen and offer assistance.",
                screenshot_b64=b64
            )
            if actions:
                self.dispatcher.dispatch_all(actions)
            self._respond(response)
            if self.gui:
                self.gui.set_thinking(False)
        else:
            self._respond("Screenshot captured. However, I couldn't analyze it — AI core may be offline.")

    def _handle_voice_toggle(self):
        """Toggle continuous voice listening."""
        if not self.voice:
            if self.gui:
                self.gui.add_system_message("Voice system not available.", "error")
            return

        if self.voice.is_listening:
            self.voice.stop_listening()
            if self.gui:
                self.gui.add_system_message("Voice deactivated.", "info")
        else:
            self.voice.listen_for_wake_word(self._handle_voice_command)
            if self.gui:
                self.gui.add_system_message(
                    f"Voice activated. Say '{self.voice.wake_word}' to speak.", "success"
                )

    def _start_screen_watcher(self):
        """Start proactive screen analysis."""
        interval = int(os.getenv("SCREEN_WATCH_INTERVAL", "10"))
        from jarvis.screen import ScreenWatcher
        watcher = ScreenWatcher()

        def on_screen(b64):
            if self.core:
                response, _ = self.core.analyze_screen(b64)
                if response and len(response) > 20:
                    self._respond(response)

        watcher.start_watching(on_screen, interval)
        logger.info(f"Screen watcher started (every {interval}s)")

    def _run_gui(self):
        """Start the GUI interface."""
        logger.info("Launching GUI...")
        from jarvis.gui import JARVISWindow
        self.gui = JARVISWindow(
            on_input=self._handle_input,
            on_screenshot=self._handle_screenshot_request,
            on_voice_toggle=self._handle_voice_toggle,
        )
        self.gui.run()

    def _run_terminal(self):
        """Run in terminal-only mode."""
        print("\033[36m[JARVIS]\033[0m Terminal mode active. Type 'quit' to exit.\n")
        while self._running:
            try:
                user_input = input("\033[90mYou: \033[0m").strip()
                if user_input:
                    self._handle_input(user_input)
            except (KeyboardInterrupt, EOFError):
                print("\n[JARVIS] Shutting down...")
                break


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JARVIS AI Assistant")
    parser.add_argument("--nogui", action="store_true", help="Run in terminal mode")
    parser.add_argument("--voice", action="store_true", help="Enable voice from startup")
    args = parser.parse_args()

    jarvis = JARVIS(nogui=args.nogui, voice_enabled=args.voice)
    jarvis.start()
