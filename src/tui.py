from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Input, Footer, Header
from textual.binding import Binding
from textual.reactive import reactive
from datetime import datetime
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from loguru import logger

import sys
import pathlib
import asyncio

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.absolute()))

from src.pomo import PomodoroTimer
from src.logger import SessionLogger


# Tomato ASCII Art
TOMATO_ASCII = """
   ╭─────────────╮
   │   🍅 POMO   │
   ╰─────────────╯
"""


# Configure loguru
logger.remove()
logger.add("pomodoro.log", format="{time} | {level} | {message}")


class TimerDisplay(Static):
    """Main timer display widget with real-time updates."""

    timer_update = reactive(0.0)

    def __init__(self, app_logic, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_logic = app_logic

    def render(self) -> str:
        """Render the timer display."""
        # Force update by accessing timer state
        _ = self.timer_update

        timer = self.app_logic.timer
        time_str = timer.format_time()
        activity = timer.activity
        status = "▶ RUNNING" if timer.is_running() else "⏸ PAUSED"
        mode_indicator = f"[{self.app_logic.current_mode.upper()}]"

        display_text = (
            f"\n{TOMATO_ASCII}\n"
            f"[bold red on black]{time_str}[/bold red on black]\n\n"
            f"[yellow]{activity}[/yellow]\n\n"
            f"[cyan]{status}[/cyan]  {mode_indicator}\n\n"
            f"[white]Today: {self.app_logic.session_count} sessions[/white]\n"
        )

        return Align.center(display_text)


class HelpText(Static):
    """Keybindings help section."""

    def render(self) -> str:
        help_content = (
            "[bold red]CONTROLS[/bold red]\n"
            "[yellow]S[/yellow] Start  "
            "[yellow]P[/yellow] Pause  "
            "[yellow]R[/yellow] Reset\n"
            "[yellow]T[/yellow] Toggle Mode  "
            "[yellow]Q[/yellow] Quit"
        )
        return Align.center(f"\n{help_content}\n")


class ActivityInput(Static):
    """Input field for activity description."""

    def compose(self) -> ComposeResult:
        yield Input(placeholder="📝 Enter activity description...", id="activity_input")


class PomodoroTUI:
    """Business logic for the Pomodoro TUI."""

    MODES = {
        "work": {"duration": 25 * 60, "name": "POMODORO", "type": "pomodoro"},
        "short_break": {
            "duration": 5 * 60,
            "name": "SHORT BREAK",
            "type": "short_break",
        },
        "long_break": {"duration": 15 * 60, "name": "LONG BREAK", "type": "long_break"},
    }

    def __init__(self):
        self.logger = SessionLogger()
        self.current_mode = "work"
        self.session_count = self.logger.get_session_count()
        self.timer = self._create_timer()
        self.session_start = None

        logger.info(f"Pomodoro app started. Today's sessions: {self.session_count}")

    def _create_timer(self) -> PomodoroTimer:
        """Create timer for current mode."""
        mode = self.MODES[self.current_mode]
        duration_minutes = mode["duration"] // 60

        timer = PomodoroTimer(duration=duration_minutes, activity=mode["name"])
        timer.on_finished = self._on_timer_finished
        return timer

    def _on_timer_finished(self) -> None:
        """Handle timer completion."""
        if self.session_start:
            self.logger.log_session(
                activity=self.timer.activity,
                session_type=self.MODES[self.current_mode]["type"],
                duration_minutes=self.timer.duration,
                start_time=self.session_start,
                end_time=datetime.now(),
                completed=True,
            )
            logger.info(f"✓ Session completed: {self.timer.activity}")

        # Switch mode
        if self.current_mode == "work":
            self.session_count += 1
            if self.session_count % 4 == 0:
                self.current_mode = "long_break"
            else:
                self.current_mode = "short_break"
        else:
            self.current_mode = "work"

        self.timer = self._create_timer()
        self.session_start = None

    def start_timer(self) -> None:
        """Start the timer."""
        if not self.timer.is_running():
            self.timer.start()
            self.session_start = datetime.now()
            logger.info(f"⏱️  Timer started: {self.timer.activity}")

    def pause_timer(self) -> None:
        """Pause the timer."""
        if self.timer.is_running():
            self.timer.stop()
            logger.info("⏸️  Timer paused")

    def reset_timer(self) -> None:
        """Reset the timer."""
        self.timer.reset()
        self.session_start = None
        logger.info("🔄 Timer reset")

    def toggle_mode(self) -> None:
        """Toggle between work and break."""
        if self.session_start and self.timer.is_running():
            self.logger.log_session(
                activity=self.timer.activity,
                session_type=self.MODES[self.current_mode]["type"],
                duration_minutes=self.timer.duration,
                start_time=self.session_start,
                end_time=datetime.now(),
                completed=False,
            )

        # Cycle through modes
        if self.current_mode == "work":
            self.current_mode = "short_break"
        elif self.current_mode == "short_break":
            self.current_mode = "work"
        else:
            self.current_mode = "work"

        self.timer = self._create_timer()
        self.session_start = None
        logger.info(f"🔄 Mode switched to: {self.current_mode}")

    def set_activity(self, activity: str) -> None:
        """Set custom activity description."""
        if activity.strip():
            self.timer.activity = activity
            logger.info(f"📝 Activity set to: {activity}")

    def update_timer(self) -> None:
        """Update timer (call frequently)."""
        if self.timer.is_running():
            self.timer.update()


# Test the app logic independently
if __name__ == "__main__":
    app = PomodoroTUI()
    print("✓ Pomodoro TUI initialized successfully")
    print(f"✓ Logging to: sessions.csv")
    print(f"✓ Sessions logged today: {app.session_count}")
