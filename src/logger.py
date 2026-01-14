import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class SessionLogger:
    """Logs Pomodoro sessions to CSV file."""
    
    CSV_FILENAME = "sessions.csv"
    FIELDNAMES = [
        "date",
        "activity",
        "session_type",
        "duration_minutes",
        "start_time",
        "end_time",
        "completed"
    ]
    
    def __init__(self, filepath: str = CSV_FILENAME):
        self.filepath = Path(filepath)
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self) -> None:
        """Create CSV file with headers if it doesn't exist."""
        if not self.filepath.exists():
            with open(self.filepath, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                writer.writeheader()
    
    def log_session(
        self,
        activity: str,
        session_type: str,
        duration_minutes: int,
        start_time: datetime,
        end_time: datetime,
        completed: bool = True
    ) -> None:
        """
        Log a completed session.
        
        Args:
            activity: Description of the activity (e.g., "Coding", "Reading")
            session_type: "pomodoro", "short_break", or "long_break"
            duration_minutes: Duration of the session in minutes
            start_time: When the session started
            end_time: When the session ended
            completed: Whether the session was completed
        """
        row = {
            "date": start_time.strftime("%Y-%m-%d"),
            "activity": activity,
            "session_type": session_type,
            "duration_minutes": duration_minutes,
            "start_time": start_time.strftime("%H:%M:%S"),
            "end_time": end_time.strftime("%H:%M:%S"),
            "completed": "Yes" if completed else "No"
        }
        
        with open(self.filepath, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            writer.writerow(row)
    
    def get_session_count(self, date: Optional[datetime] = None) -> int:
        """
        Get number of completed sessions for a given date.
        If date is None, use today.
        """
        if date is None:
            date = datetime.now()
        
        target_date = date.strftime("%Y-%m-%d")
        count = 0
        
        if self.filepath.exists():
            with open(self.filepath, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (row.get("date") == target_date and 
                        row.get("session_type") == "pomodoro" and
                        row.get("completed") == "Yes"):
                        count += 1
        
        return count
