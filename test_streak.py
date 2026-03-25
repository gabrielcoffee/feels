#!/usr/bin/env python3
"""
Test script to visualize streak styling at different milestone levels.

Change the 'days' variable to test different streak lengths:
- 1, 3: Just number bold
- 5, 6: Whole text bold
- 7, 9: Bold with 1 !
- 10-19: Yellow with 2 !!
- 20-29: Cyan with 3 !!!
- 30-39: Magenta with 4 !!!!
- 50-59: Blue with 6 !!!!!!
- 100: Random color with 1 !
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

# ============= CHANGE THIS NUMBER TO TEST DIFFERENT STREAKS =============
days = 1000
# =========================================================================

db = Path.home() / ".feels" / "data.db"
conn = sqlite3.connect(db)

# Clear existing logs
conn.execute("DELETE FROM logs")

# Create logs for consecutive days
today = datetime.now()
for i in range(days):
    date = today - timedelta(days=days-1-i)
    conn.execute(
        "INSERT INTO logs (timestamp, mood, tags, note) VALUES (?, ?, ?, ?)",
        (date.isoformat(), 4, "#test", f"Day {i+1}")
    )

conn.commit()
conn.close()

print(f"✓ Created {days}-day streak test data")
