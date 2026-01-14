# Pomodoro App - Project Structure

```txt
pomodoro-app/
├── src/
│   ├── __init__.py
│   ├── pomo.py                 # Core timer logic (existing)
│   ├── logger.py               # CSV logging functionality
│   └── ui.py                   # Textual TUI implementation
├── tests/
│   └── test_pomodoro.py        # Unit tests (existing)
├── sessions.csv                # Session history log
├── requirements.txt
├── .gitignore
└── README.md
```

## Dependencies

```txt
textual>=0.40.0
rich>=13.0.0
loguru>=0.7.0
pytest>=7.0
```
