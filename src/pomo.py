"""
Core Pomodoro Timer Module

Pure timer logic with no UI dependencies.
Fully testable with mocked time.
"""

import math
import time
from datetime import datetime
from typing import Optional, Callable


class PomodoroTimer:
    """
    Pomodoro Timer with activity tracking and callbacks.

    Features:
    - Start/stop/reset timer
    - Activity description
    - Callback on completion
    - Time formatting (MM:SS)
    - Session tracking
    """

    WORK_DURATION = 25 * 60  # 25 minutes in seconds
    SHORT_BREAK_DURATION = 5 * 60  # 5 minutes
    LONG_BREAK_DURATION = 15 * 60  # 15 minutes

    def __init__(
        self, duration: int | float = 25, activity: str = "Work", *args, **kwargs
    ):
        """
        Initialize timer.

        Args:
            duration: Duration in minutes (default 25)
            activity: Description of activity (default "Work")

        Raises:
            TypeError: If duration is not a number
            ValueError: If duration is not positive
        """
        if not isinstance(duration, (int, float)):
            raise TypeError("Duration has to be a number.")
        if duration <= 0:
            raise ValueError("Duration has to be a positive number.")

        # Store duration in seconds
        self.duration = int(duration * 60)  # Convert minutes to seconds
        self.activity = activity
        self._start_time = 0.0
        self._remaining = self.duration  # Remaining in seconds
        self._is_running = False
        self.on_finished: Optional[Callable] = None
        self.start_datetime: Optional[datetime] = None

    def start(self) -> str:
        """
        Start the timer.

        Returns:
            "started" if successful
            "already_started" if timer is already running
        """
        if self._is_running:
            return "already_started"
        self._start_time = time.time()
        self._remaining = self.duration
        self._is_running = True
        self.start_datetime = datetime.now()
        return "started"

    def stop(self) -> str:
        """
        Pause/stop the timer.

        Returns:
            "stopped" if successful
            "not_running" if timer is not running
        """
        if not self._is_running:
            return "not_running"
        self._is_running = False
        return "stopped"

    def reset(self) -> str:
        """
        Reset timer to initial state.

        Returns:
            "reset"
        """
        self._is_running = False
        self._remaining = self.duration
        self._start_time = 0.0
        self.start_datetime = None
        return "reset"

    def remaining(self) -> int:
        """
        Get remaining time in seconds.

        Returns:
            Remaining time as integer seconds
        """
        return self._remaining

    def update(self, seconds: Optional[int] = None) -> None:
        """
        Update the timer with elapsed time.

        Should be called frequently (e.g., every 0.1 seconds).

        Args:
            seconds: Optional explicit seconds to subtract (for testing)
        """
        if not self._is_running:
            return

        # Always calculate based on elapsed time from start
        elapsed_time = time.time() - self._start_time
        remaining_exact = self.duration - elapsed_time

        if remaining_exact <= 0:
            self._remaining = 0
        else:
            self._remaining = math.ceil(remaining_exact)

        # Call callback only on transition to finished state
        if self._remaining == 0 and self.on_finished:
            self.on_finished()

    def finished(self) -> bool:
        """
        Check if timer has finished.

        Returns:
            True if remaining time is 0
        """
        return self._remaining == 0

    def is_running(self) -> bool:
        """
        Check if timer is currently running.

        Returns:
            True if timer is active
        """
        return self._is_running

    def format_time(self) -> str:
        """
        Format remaining time as MM:SS.

        Returns:
            String in format "MM:SS" (e.g., "25:00", "04:32")
        """
        minutes = self._remaining // 60
        seconds = self._remaining % 60
        return f"{minutes:02d}:{seconds:02d}"

    def get_elapsed(self) -> int:
        """
        Get elapsed time in seconds since session started.

        Returns:
            Elapsed time in seconds, capped at duration
        """
        if self.start_datetime is None:
            return 0
        elapsed = int((datetime.now() - self.start_datetime).total_seconds())
        return min(elapsed, self.duration)
