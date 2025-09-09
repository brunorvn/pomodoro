import sys
import pathlib

import time
from unittest.mock import patch

import pytest

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from src.pomo import PomodoroTimer


@patch("time.time", return_value=12345)
def test_timer_returns_correct_time(mock_time):
    assert time.time() == 12345


def test_timer_starts_correctly():
    timer = PomodoroTimer()
    result = timer.start()
    assert result == "started"


def test_timer_stops_correctly():
    timer = PomodoroTimer()
    timer.start()
    result = timer.stop()
    assert result == "stopped"


def test_timer_resets_correctly():
    timer = PomodoroTimer()
    timer.start()
    timer.stop()
    result = timer.reset()
    assert result == "reset"


def test_countdown_accuracy():
    timer = PomodoroTimer(duration=5)
    with patch("time.time", side_effect=[100.0, 101.0, 104.9, 105.0]):
        timer.start()
        assert timer.remaining() == 5
        timer.update()
        assert timer.remaining() == 4
        timer.update()
        assert timer.remaining() == 1
        timer.update()
        assert timer.finished()


def test_starting_already_started_timer_does_not_restart():
    timer = PomodoroTimer()
    timer.start()
    original_start_time = timer._start_time
    result = timer.start()
    assert result == "already_started" and timer._start_time == original_start_time
    assert timer.is_running()

def test_stopping_not_started_timer_does_not_stop():
    timer = PomodoroTimer()
    result = timer.stop()
    assert result == "not_running" or result == "stopped"
    assert not timer.is_running()

def resetting_never_started_timer():
    timer = PomodoroTimer()
    result = timer.reset()
    assert result == "reset"
    assert timer.remaining() == timer.duration

def resetting_already_started_timer():
    timer = PomodoroTimer()
    timer.start()

    result = timer.reset()
    assert result == "reset"
    assert timer.remaining() == timer.duration

def test_negative_duration_raises_error():
    with pytest.raises(ValueError):
        PomodoroTimer(duration=-1)

def test_zero_duration_raises_error():
    with pytest.raises(ValueError):
        PomodoroTimer(duration=0)

def test_very_large_duration_works():
    timer = PomodoroTimer(duration=86400)  # 24 hours
    assert timer.duration == 86400

def test_timer_exactly_at_expiration():
    timer = PomodoroTimer(duration=1)
    with patch("time.time", side_effect=[100.0, 101.0]):
        timer.start()
        timer.update()
        assert timer.finished()
        assert timer.remaining() == 0

def test_timer_just_before_expiration():
    timer = PomodoroTimer(duration=5)
    with patch("time.time", side_effect=[100.0, 104.9]):
        timer.start()
        timer.update()
        assert not timer.finished()
        assert timer.remaining() == 1  # Should round up
def test_timer_past_expiration():
    timer = PomodoroTimer(duration=5)
    with patch("time.time", side_effect=[100.0, 107.0]):
        timer.start()
        timer.update()
        assert timer.finished()
        assert timer.remaining() == 0

# Multiple Cycles

def test_multiple_start_stop_cycles():
    timer = PomodoroTimer(duration=10)
    
    # First cycle
    timer.start()
    timer.stop()
    assert not timer.is_running()
    
    # Second cycle
    result = timer.start()
    assert result == "started"
    assert timer.is_running()

def test_reset_after_completion():
    timer = PomodoroTimer(duration=1)
    with patch("time.time", side_effect=[100.0, 101.0]):
        timer.start()
        timer.update()
        assert timer.finished()
        
        timer.reset()
        assert not timer.finished()
        assert timer.remaining() == 1

# State Consistency

def test_timer_state_after_stop():
    timer = PomodoroTimer(duration=10)
    with patch("time.time", side_effect=[100.0, 105.0]):
        timer.start()
        timer.update()
        remaining_before_stop = timer.remaining()
        
        timer.stop()
        assert timer.remaining() == remaining_before_stop
        assert not timer.is_running()

def test_timer_cannot_update_when_stopped():
    timer = PomodoroTimer(duration=10)
    timer.start()
    timer.stop()
    
    with patch("time.time", return_value=999999):
        timer.update()
        # Remaining should not change when stopped
        assert timer.remaining() > 0

# PyQt5 Signal Connection Test (Simple Backend Focus)

def test_timer_expiration_callback():
    callback_called = False
    
    def on_timer_finished():
        nonlocal callback_called
        callback_called = True
    
    timer = PomodoroTimer(duration=1)
    timer.on_finished = on_timer_finished  # Simple callback pattern
    
    with patch("time.time", side_effect=[100.0, 101.0]):
        timer.start()
        timer.update()
        
    assert callback_called

# String Representation for Debugging

def test_timer_string_representation():
    timer = PomodoroTimer(duration=1500)  # 25 minutes
    timer_str = str(timer)
    assert "25:00" in timer_str or "1500" in timer_str

def test_timer_provides_consistent_state_info():
    timer = PomodoroTimer(duration=10)
    
    # Before starting
    assert not timer.is_running()
    assert not timer.finished()
    assert timer.remaining() == 10
    
    # After starting
    timer.start()
    assert timer.is_running()
    assert not timer.finished()
    
    # After finishing
    with patch("time.time", side_effect=[100.0, 110.0]):
        timer.update()
        assert timer.finished()
        assert not timer.is_running()
