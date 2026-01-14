"""
Main Textual Application for Pomodoro Timer - FIXED

Issues fixed:
1. Input field now only visible when needed
2. Keybindings work globally (not captured by input)
3. Timer format is MM:SS (25:00 not 00:25)
4. ASCII art properly displayed
"""

from textual.app import ComposeResult, on
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Input, Footer
from textual.binding import Binding
from textual.reactive import reactive
from rich.align import Align
from datetime import datetime
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.absolute()))

from src.tui import PomodoroTUI
from src.pomo import PomodoroTimer
from src.logger import SessionLogger

# Tomato ASCII Art (Large 25:00 display)
TOMATO_LARGE = """
    ╔════════════════════╗
    ║   🍅  P O M O  🍅   ║
    ╚════════════════════╝
"""


class TimerDisplay(Static):
    """Main timer display widget with real-time updates."""

    timer_update = reactive(0.0)

    def __init__(self, app_logic, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_logic = app_logic

    def render(self) -> str:
        """Render the timer display."""
        # Trigger re-render on timer update
        _ = self.timer_update

        timer = self.app_logic.timer
        time_str = timer.format_time()
        activity = timer.activity
        status = "▶ RUNNING" if timer.is_running() else "⏸ PAUSED"
        mode = f"[{self.app_logic.current_mode.upper()}]"

        display = (
            f"\n{TOMATO_LARGE}\n"
            f"[bold red on black]{time_str}[/bold red on black]\n\n"
            f"[yellow]{activity}[/yellow]\n\n"
            f"[cyan]{status}[/cyan]  {mode}\n\n"
            f"[white]Today: {self.app_logic.session_count} sessions[/white]\n"
        )

        return Align.center(display)


class ActivityPrompt(Static):
    """Prompt to enter activity - only shown when needed."""

    def render(self) -> str:
        return "[dim]Press [yellow]A[/yellow] to set activity[/dim]"


class HelpSection(Static):
    """Help/keybindings display."""

    def render(self) -> str:
        help_text = (
            "[bold red]CONTROLS[/bold red]\n"
            "[yellow]S[/yellow] Start  "
            "[yellow]P[/yellow] Pause  "
            "[yellow]R[/yellow] Reset  "
            "[yellow]T[/yellow] Toggle  "
            "[yellow]A[/yellow] Activity  "
            "[yellow]Q[/yellow] Quit"
        )
        return Align.center(f"\n{help_text}\n")


class PomodoroApp:
    """Textual app wrapper - manages the UI."""

    def __init__(self):
        from textual.app import App

        class PomodoroCLI(App):
            """Main Textual application."""

            BINDINGS = [
                Binding("s", "start", "Start", show=False),
                Binding("p", "pause", "Pause", show=False),
                Binding("r", "reset", "Reset", show=False),
                Binding("t", "toggle", "Toggle", show=False),
                Binding("a", "set_activity", "Activity", show=False),
                Binding("q", "quit", "Quit", show=False),
            ]

            CSS = """
            Screen {
                background: $panel;
                align: center middle;
            }
            
            #main_container {
                width: 70;
                height: auto;
                border: solid $error;
            }
            
            #timer_display {
                border: none;
                width: 100%;
                height: auto;
            }
            
            #activity_input {
                width: 100%;
                height: 3;
                border: solid $warning;
                display: none;
            }
            
            #activity_input.active {
                display: block;
            }
            
            #help_section {
                border: none;
                width: 100%;
                height: auto;
            }
            
            Input {
                margin: 1 0;
            }
            """

            def __init__(self):
                super().__init__()
                self.app_logic = PomodoroTUI()
                self.timer_display = None
                self.activity_input = None
                self.input_active = False

            def compose(self) -> ComposeResult:
                """Compose the UI."""
                self.timer_display = TimerDisplay(self.app_logic, id="timer_display")
                self.activity_input = Input(
                    placeholder="Enter activity and press Enter", id="activity_input"
                )

                yield Container(
                    Vertical(
                        self.timer_display,
                        self.activity_input,
                        HelpSection(id="help_section"),
                    ),
                    id="main_container",
                )

            def on_mount(self) -> None:
                """Initialize after app mounts."""
                # Start timer update loop
                self.set_interval(0.1, self._update_timer)
                # Focus on app, not input
                self.focus()

            def _update_timer(self) -> None:
                """Update timer display every 0.1 seconds."""
                if self.app_logic.timer.is_running():
                    self.app_logic.update_timer()
                    if self.timer_display:
                        # Trigger reactive update
                        self.timer_display.timer_update = (
                            self.timer_display.timer_update + 0.1
                        )

            def action_start(self) -> None:
                """Start the timer (S key)."""
                if not self.input_active:
                    self.app_logic.start_timer()
                    self._refresh()

            def action_pause(self) -> None:
                """Pause the timer (P key)."""
                if not self.input_active:
                    self.app_logic.pause_timer()
                    self._refresh()

            def action_reset(self) -> None:
                """Reset the timer (R key)."""
                if not self.input_active:
                    self.app_logic.reset_timer()
                    self._refresh()

            def action_toggle(self) -> None:
                """Toggle between work and break (T key)."""
                if not self.input_active:
                    self.app_logic.toggle_mode()
                    self._refresh()

            def action_set_activity(self) -> None:
                """Activate activity input (A key)."""
                if not self.input_active:
                    self.input_active = True
                    self.activity_input.add_class("active")
                    self.activity_input.focus()
                else:
                    # Already active, deactivate
                    self.input_active = False
                    self.activity_input.remove_class("active")
                    self.activity_input.value = ""
                    self.focus()

            def action_quit(self) -> None:
                """Quit application (Q key)."""
                self.exit()

            def _refresh(self) -> None:
                """Refresh the display."""
                if self.timer_display:
                    self.timer_display.refresh()

            @on(Input.Submitted, "#activity_input")
            def on_activity_submitted(self, event: Input.Submitted) -> None:
                """Handle activity input submission."""
                activity = event.value.strip()
                if activity:
                    self.app_logic.set_activity(activity)
                    self._refresh()

                # Deactivate input
                self.input_active = False
                self.activity_input.remove_class("active")
                self.activity_input.value = ""
                self.focus()

        self.app = PomodoroCLI()

    def run(self) -> None:
        """Run the application."""
        self.app.run()


def main():
    """Entry point for the Pomodoro app."""
    app = PomodoroApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Pomodoro session ended. Keep focused!")
        sys.exit(0)


if __name__ == "__main__":
    main()
