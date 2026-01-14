#!/usr/bin/env python3
"""
Pomodoro Timer - Terminal-based Pomodoro Technique implementation

Run with: python -m pomodoro.main
or: python main.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.absolute()))

from main import run

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n\n👋 Pomodoro session ended. Keep up the great work!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
