from textual.app import ComposeResult, on
from textual.containers import Container, Vertical
from textual.widgets import Static, Input, Footer
from textual.binding import Binding
from datetime import datetime
from rich.align import Align
from rich.console import Console
from rich.text import Text

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.absolute()))

from src.pomo import PomodoroTimer
from src.logger import SessionLogger


# ASCII Art Tomato Timer
TOMATO_ASCII = """
   ╔════════════════╗
   ║    🍅 POMO 🍅   ║
   ╚════════════════╝
"""

HELP_TEXT = """
[bold red]KEYBINDINGS[/bold red]
[yellow]S[/yellow] - Start/Resume    [yellow]P[/yellow] - Pause    [yellow]R[/yellow] - Reset
[yellow]T[/yellow] - Toggle Break     [yellow]Q[/yellow] - Quit
"""


class TimerDisplay(Static):
    """Main timer display widget."""
    
    def __init__(self, timer: PomodoroTimer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = timer
        self.session_count = 0

    def render(self) -> str:
        """Render the timer display."""
        time_str = self.timer.format_time()
        activity = self.timer.activity
        status = "▶ RUNNING" if self.timer.is_running() else "⏸ PAUSED"
        
        display = f"""
{TOMATO_ASCII}

[bold red]{time_str}[/bold red]

[yellow]{activity}[/yellow]

[cyan]{status}[/cyan]

[white]Sessions Today: {self.session_count}[/white]
"""
        return Align.center(display)


class ActivityInput(Static):
    """Input field for activity description."""
    
    def __init__(self, timer: PomodoroTimer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = timer
        self.input_widget = Input(
            placeholder="Enter activity (or press Enter to skip)",
            id="activity_input"
        )
    
    def compose(self) -> ComposeResult:
        yield self.input_widget


class PomodoroApp:
    """Main Pomodoro application."""
    
    MODES = {
        "work": {"duration": 25 * 60, "name": "Pomodoro"},
        "short_break": {"duration": 5 * 60, "name": "Short Break"},
        "long_break": {"duration": 15 * 60, "name": "Long Break"},
    }
    
    def __init__(self):
        self.logger = SessionLogger()
        self.current_mode = "work"
        self.session_count = 0
        self.timer = self._create_timer()
        self.session_start = None
        self.is_break = False
    
    def _create_timer(self) -> PomodoroTimer:
        """Create a new timer for current mode."""
        mode = self.MODES[self.current_mode]
        duration_minutes = mode["duration"] // 60
        
        timer = PomodoroTimer(
            duration=duration_minutes,
            activity=mode["name"]
        )
        timer.on_finished = self._on_timer_finished
        return timer
    
    def _on_timer_finished(self) -> None:
        """Called when timer finishes."""
        # Log the session
        if self.session_start:
            self.logger.log_session(
                activity=self.timer.activity,
                session_type=self.current_mode,
                duration_minutes=self.timer.duration,
                start_time=self.session_start,
                end_time=datetime.now(),
                completed=True
            )
        
        # Auto-switch to break or next pomodoro
        self._switch_mode()
        self.timer = self._create_timer()
    
    def _switch_mode(self) -> None:
        """Switch between work and break modes."""
        if self.current_mode == "work":
            self.session_count += 1
            if self.session_count % 4 == 0:
                self.current_mode = "long_break"
            else:
                self.current_mode = "short_break"
        else:
            self.current_mode = "work"
    
    def set_activity(self, activity: str) -> None:
        """Set the activity description."""
        if activity.strip():
            self.timer.activity = activity
    
    def start_timer(self) -> None:
        """Start the timer."""
        self.timer.start()
        self.session_start = datetime.now()
    
    def pause_timer(self) -> None:
        """Pause the timer."""
        self.timer.stop()
    
    def reset_timer(self) -> None:
        """Reset the timer."""
        self.timer.reset()
    
    def toggle_break(self) -> None:
        """Toggle between work and break mode."""
        # Log if session was started
        if self.session_start and self.timer.is_running():
            self.logger.log_session(
                activity=self.timer.activity,
                session_type=self.current_mode,
                duration_minutes=self.timer.duration,
                start_time=self.session_start,
                end_time=datetime.now(),
                completed=False
            )
        
        self._switch_mode()
        self.timer = self._create_timer()
        self.session_start = None


# For testing - you'll integrate this with Textual separately
if __name__ == "__main__":
    app = PomodoroApp()
    print("Pomodoro App initialized successfully")
    print(f"CSV Logger ready at: {app.logger.filepath}")
