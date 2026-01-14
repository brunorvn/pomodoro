# 🍅 Pomodoro Timer - Visual Quick Reference

## Installation & Launch (30 seconds)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch
python main.py

# That's it! You're in the timer
```

## What You'll See

```
   ╭─────────────╮
   │   🍅 POMO   │
   ╰─────────────╯

   [bold red]25:00[/bold red]

   POMODORO

   ⏸ PAUSED [work]

   Today: 0 sessions

📝 Enter activity description...

[CONTROLS]
S Start  P Pause  R Reset
T Toggle Mode  Q Quit
```

## Workflow

### Scenario 1: First Pomodoro Session

```
User → python main.py
   ↓
Display → Shows 25:00 timer, PAUSED
   ↓
User → Types "Backend API Development"
   ↓
User → Presses S (Start)
   ↓
Timer → Starts counting down: 24:59, 24:58, ...
   ↓
After 25 minutes → 
   • Timer reaches 00:00
   • Auto-logs to CSV
   • Switches to 5-minute break
   • Shows 05:00 timer
   ↓
User → Presses S to start break
   ↓
After 5 minutes →
   • Timer finishes
   • Auto-logs break
   • Switches back to work mode
   • Shows 25:00 again
```

### Scenario 2: Interrupted Session

```
User → Presses P (Pause)
   ↓
Timer → Stops counting
   ↓
User → Takes unexpected call
   ↓
User → Can press:
   • S to resume (continues from paused time)
   • R to reset (starts over)
   • T to switch modes (skip to break)
```

## Key Commands

| Key | What Happens | Use Case |
|-----|-------------|----------|
| **S** | Start or resume timer | Begin work session |
| **P** | Pause timer | Unexpected interruption |
| **R** | Reset timer | Restart from 25:00 |
| **T** | Switch work ↔ break | Skip to break early |
| **Q** | Quit app | Done for now |

## Session Log (sessions.csv)

After each session, a line is added:

```csv
date         activity              session_type  duration  start_time  end_time   completed
2025-12-29   Backend API Dev       pomodoro      25        14:30:05    14:55:12   Yes
2025-12-29   Coffee Break          short_break   5         14:55:13    15:00:18   Yes
```

## Color Meanings

| Color | Meaning |
|-------|---------|
| 🔴 **Red** | Timer display (Pomodoro theme) |
| 🟡 **Yellow** | Activity description |
| 🔵 **Cyan** | Status (Running/Paused) |
| ⚪ **White** | Session counter |

## Timer Modes

```
Work Mode (25 min)
        ↓↓ (After 25 minutes)
Short Break (5 min)
        ↓↓ (After 5 minutes)
Work Mode (25 min)
        ↓↓ (x3 times)
Long Break (15 min)
        ↓↓ (After 15 minutes)
Work Mode (25 min) [Cycle repeats]
```

## Example Session

**14:00** - Launch `python main.py`
- Display: `25:00 POMODORO ⏸ PAUSED`

**14:00:30** - Type "Implement user auth"

**14:00:45** - Press `S`
- Display: `24:45 Implement user auth ▶ RUNNING [work]`

**14:25:00** - Timer finishes automatically
- Auto-logged to CSV ✓
- Display: `05:00 SHORT BREAK ⏸ PAUSED`

**14:25:10** - Press `S`
- Display: `04:50 SHORT BREAK ▶ RUNNING [short_break]`

**14:30:00** - Break ends
- Auto-logged to CSV ✓
- Display: `25:00 POMODORO ⏸ PAUSED`

**Session count** → +1 (now showing "Today: 1 sessions")

## Tips & Tricks

### ✅ Best Practices
- 🎯 Set a specific activity before starting
- ⏸️ Pause if interrupted; resume when ready
- 🔄 Use T to skip breaks if not needed
- 📊 Review CSV weekly to track patterns

### ⚠️ Common Issues
- Q: "Timer doesn't seem to update"
  - A: Updates every 0.1 seconds; might look frozen
  
- Q: "Can't type in activity field"
  - A: Click on input field first (may vary by terminal)
  
- Q: "Colors look wrong"
  - A: Set `export TERM=xterm-256color`

### 🚀 Advanced Usage
```bash
# Create alias for quick launch
alias pomo="cd ~/path/to/pomodoro && python main.py"

# Then just type: pomo

# Run tests
pytest tests/test_pomodoro.py -v

# Analyze your sessions
head -20 sessions.csv  # View latest sessions
wc -l sessions.csv     # Count total sessions
```

## CSV Analysis

```bash
# Count today's sessions
grep "2025-12-29" sessions.csv | wc -l

# View only completed pomodoros (not breaks)
grep "pomodoro" sessions.csv | grep "Yes"

# Export to analysis tool
cat sessions.csv | head -100
```

## Typical Day (Example)

```
08:00 - Start Pomodoro 1: "Code review"
08:25 - Break
08:30 - Start Pomodoro 2: "Bug fixes"
08:55 - Break
09:00 - Start Pomodoro 3: "Unit tests"
09:25 - Break
09:30 - Start Pomodoro 4: "Documentation"
09:55 - Long Break (15 min)
10:10 - Start Pomodoro 5: "API integration"
...

Result: 5 pomodoros ≈ 2 hours 5 minutes of focused work
Breaks: 20 minutes
Total: ~2.5 hours block
```

## What Gets Logged

**In sessions.csv:**
- ✅ Activity name
- ✅ Session type (pomodoro/short_break/long_break)
- ✅ Duration
- ✅ Start and end times
- ✅ Whether it was completed

**In pomodoro.log:**
- ✅ All app actions (start, pause, reset)
- ✅ Mode switches
- ✅ Activity changes
- ✅ Timestamps

## Keyboard Shortcut Cheatsheet

```
╔════════════════════════════════╗
║   POMODORO TIMER SHORTCUTS     ║
╠════════════════════════════════╣
║ S - START/RESUME               ║
║ P - PAUSE                      ║
║ R - RESET                      ║
║ T - TOGGLE MODE                ║
║ Q - QUIT                       ║
╚════════════════════════════════╝
```

## Success Indicators

✅ You'll know it's working when:
- Timer counts down from 25:00 to 00:00
- Sessions appear in `sessions.csv`
- You can pause/resume without losing time
- Mode switches automatically after timer ends

## Troubleshooting Quick Fixes

| Problem | Fix |
|---------|-----|
| App won't start | `pip install -r requirements.txt` |
| Colors wrong | `export TERM=xterm-256color` |
| CSV not updating | Check file permissions in current dir |
| Tests fail | `python -m pytest tests/ -v` |
| Timer jumps | Normal due to rounding; use ceil() |

---

**You're ready to use your Pomodoro timer!** 🍅✨

Print this page or bookmark for quick reference while using the app.
