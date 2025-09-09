import math
import time


class PomodoroTimer:
    def __init__(self, duration: int | float = 25, *args, **kwargs):
        if not isinstance(duration, (int, float)):
            raise TypeError("Duration has to be a number.")
        if duration <= 0:
            raise ValueError("Duration has to be a positive number.")
        self.duration = int(duration)
        self._start_time = 0.0
        self._remaining = duration
        self._is_running = False
        self.on_finished = None  # Callback function

    def start(self):
        if self._is_running:
            return "already_started"
        self._start_time = time.time()
        self._remaining = self.duration
        self._is_running = True
        return "started"

    def stop(self):
        if not self._is_running: 
            return "not_running"
        self._is_running = False
        return "stopped"

    def reset(self):
        self._is_running = False
        self._remaining = self.duration
        self._start_time = 0.0
        return "reset"

    def remaining(self):
        return self._remaining

    def update(self, seconds=None):
        if not self._is_running:
            return
            
        # Store previous state to detect transition
        was_finished = self.finished()
        
        # Always calculate based on elapsed time from start
        elapsed_time = time.time() - self._start_time
        remaining_exact = self.duration - elapsed_time
        
        if remaining_exact <= 0:
            self._remaining = 0
        else:
            self._remaining = math.ceil(remaining_exact)
        
        # Call callback only on transition to finished state
        if not was_finished and self.finished() and self.on_finished:
            self.on_finished()

    def finished(self):
        return self._remaining == 0

    def is_running(self):
        return self._is_running
