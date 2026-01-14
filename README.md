# 🍅 Pomodoro Timer - Terminal MVP

A minimal, beautiful, and responsive Pomodoro timer for the command line. Built with Python, Textual, and Rich.

## Features

✨ **Core Features**

- ⏱️ **25:00 / 5:00 Timers** - Default Pomodoro (25 min) and break (5 min) durations
- 📝 **Activity Tracking** - Describe what you're working on for each session
- 🎯 **Session Counter** - Tracks completed sessions per day
- 📊 **CSV Logging** - Automatically logs all sessions to `sessions.csv` for analysis
- ⌨️ **Keyboard Shortcuts** - Fast controls: S(tart), P(ause), R(eset), T(oggle), Q(uit)
- 🎨 **Terminal UI** - Clean, minimal interface with red/tomato theme
- 🍅 **ASCII Art** - Cute tomato emoji and Unicode timer display
- 📱 **Responsive Design** - Works with any terminal size

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd pomodoro-app

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

## Usage

### Starting the App

```bash
python main.py
```

### Keybindings

| Key | Action |
|-----|--------|
| **S** | Start / Resume timer |
| **P** | Pause timer |
| **R** | Reset timer |
| **T** | Toggle between work/break mode |
| **Q** | Quit application |

### Workflow Example

1. **Start a Pomodoro session**
   - Press `S` to start the 25-minute work timer
   - Type your activity in the input field (e.g., "Coding backend API")
   - Focus on your work

2. **When timer ends**
   - Session auto-logs to `sessions.csv`
   - Timer automatically switches to 5-minute break
   - You can press `S` again to start the break

3. **After 4 pomodoros**
   - Timer switches to 15-minute long break
   - Track your productivity in `sessions.csv`

## Project Structure

```
pomodoro-app/
├── src/
│   ├── pomo.py           # Core timer class with all logic
│   ├── logger.py         # CSV session logging
│   ├── tui.py           # Business logic and display widgets
│   └── __init__.py
├── tests/
│   └── test_pomodoro.py # Unit tests for timer
├── main.py              # Entry point - Textual app
├── sessions.csv         # Auto-generated session log
├── pomodoro.log         # App activity log
├── requirements.txt
└── README.md
```

## CSV Session Log

Every completed session is logged to `sessions.csv`:

```csv
date,activity,session_type,duration_minutes,start_time,end_time,completed
2025-12-29,Coding backend API,pomodoro,25,14:30:05,14:55:12,Yes
2025-12-29,Break,short_break,5,14:55:13,15:00:18,Yes
2025-12-29,Testing features,pomodoro,25,15:00:19,15:25:47,Yes
```

## Core Classes

### PomodoroTimer

Located in `src/pomo.py` - The heart of the application

```python
from src.pomo import PomodoroTimer

timer = PomodoroTimer(duration=25, activity="Coding")
timer.start()
timer.update()  # Call frequently to update countdown
timer.is_running()  # Check status
timer.format_time()  # Get "MM:SS" format
```

### SessionLogger

Located in `src/logger.py` - Handles CSV persistence

```python
from src.logger import SessionLogger
from datetime import datetime

logger = SessionLogger()
logger.log_session(
    activity="Feature Development",
    session_type="pomodoro",
    duration_minutes=25,
    start_time=datetime.now(),
    end_time=datetime.now(),
    completed=True
)
```

### PomodoroTUI

Located in `src/tui.py` - Business logic and state management

```python
from src.tui import PomodoroTUI

app = PomodoroTUI()
app.start_timer()
app.set_activity("My task")
app.toggle_mode()
```

## Testing

Run the test suite:

```bash
pytest tests/test_pomodoro.py -v
```

Tests cover:

- Timer start/stop/reset functionality
- Countdown accuracy with mocked time
- Edge cases (expired timers, invalid inputs)
- Callback on completion
- State consistency

## Design Decisions

### Keep It Simple (KISS)

- No database - CSV logging is lightweight and portable
- No external timer libraries - Pure Python `time.time()`
- Terminal-only UI - Focus on core functionality
- Minimal dependencies - Only Textual, Rich, and Loguru

### Test-Driven Development

- All timer logic tested before UI integration
- Mock time functions for deterministic testing
- Focus on backend reliability, not UI perfection

### Responsive Backend

- Timer updates frequently for smooth countdown
- Callbacks for state transitions
- Clean separation of concerns (timer, logger, UI)

## Customization

### Change Default Timers

Edit `src/tui.py`:

```python
MODES = {
    "work": {"duration": 30 * 60, "name": "DEEP WORK"},  # 30 min
    "short_break": {"duration": 10 * 60, "name": "BREAK"},  # 10 min
    "long_break": {"duration": 20 * 60, "name": "LONG BREAK"},  # 20 min
}
```

### Change Colors

Edit CSS in `main.py`:

```python
CSS = """
#timer_display {
    border: solid $error;  # Change from $error to $warning, $success, etc
}
"""
```

## Logs

Two types of logs are maintained:

1. **sessions.csv** - Structured session data for analysis
2. **pomodoro.log** - Application activity log with timestamps

## Future Enhancements (Not in MVP)

- Audio notifications when timer ends
- Sound file options
- Custom timer presets
- Weekly/monthly statistics dashboard
- Integration with task managers
- Distraction blocker

## License

MIT License - Feel free to use and modify!

## Contributing

Contributions welcome! Please:

1. Write tests for new features
2. Keep code simple and readable
3. Follow existing patterns
4. Update documentation

---

**Made with ❤️ for focused developers who love the terminal**
