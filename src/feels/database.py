import sqlite3
from datetime import datetime, timedelta
from typing import Optional

from .config import CONFIG_DIR

DB_FILE = CONFIG_DIR / "data.db"


def db_exists() -> bool:
    return DB_FILE.exists()


def init_db(config: dict) -> None:
    CONFIG_DIR.mkdir(exist_ok=True)

    columns = [
        "id INTEGER PRIMARY KEY AUTOINCREMENT",
        "timestamp TEXT NOT NULL",
        "mood INTEGER NOT NULL",
    ]

    if config.get("focus"):
        columns.append("focus INTEGER")
    if config.get("stress"):
        columns.append("stress INTEGER")
    if config.get("projects"):
        columns.append("project TEXT")

    columns += ["tags TEXT", "note TEXT", "asciimoji TEXT"]

    conn = sqlite3.connect(DB_FILE)
    conn.execute(f"CREATE TABLE IF NOT EXISTS logs ({', '.join(columns)})")
    conn.commit()
    conn.close()


def ensure_columns(config: dict) -> None:
    """Add any columns missing from an existing DB (schema migration)."""
    conn = _connect()
    existing = {row[1] for row in conn.execute("PRAGMA table_info(logs)").fetchall()}

    additions = []
    if config.get("focus") and "focus" not in existing:
        additions.append("focus INTEGER")
    if config.get("stress") and "stress" not in existing:
        additions.append("stress INTEGER")
    if config.get("projects") and "project" not in existing:
        additions.append("project TEXT")
    if "asciimoji" not in existing:
        additions.append("asciimoji TEXT")

    for col in additions:
        conn.execute(f"ALTER TABLE logs ADD COLUMN {col}")
    if additions:
        conn.commit()
    conn.close()


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def insert_log(entry: dict) -> int:
    conn = _connect()
    cols = ", ".join(entry.keys())
    placeholders = ", ".join("?" * len(entry))
    cur = conn.execute(
        f"INSERT INTO logs ({cols}) VALUES ({placeholders})",
        list(entry.values()),
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def get_log(log_id: int) -> Optional[dict]:
    conn = _connect()
    row = conn.execute("SELECT * FROM logs WHERE id = ?", (log_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_logs(
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    project: Optional[str] = None,
    newest_first: bool = True,
    all_logs: bool = False,
) -> list[dict]:
    conditions = []
    params = []

    if not all_logs and from_date is None:
        since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        conditions.append("DATE(timestamp) >= ?")
        params.append(since)

    if from_date:
        conditions.append("DATE(timestamp) >= ?")
        params.append(from_date)

    if to_date:
        conditions.append("DATE(timestamp) <= ?")
        params.append(to_date)

    if project:
        conditions.append("project = ?")
        params.append(project)

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    order = "DESC" if newest_first else "ASC"

    conn = _connect()
    rows = conn.execute(
        f"SELECT * FROM logs {where} ORDER BY timestamp {order}",
        params,
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_log(log_id: int, fields: dict) -> None:
    assignments = ", ".join(f"{k} = ?" for k in fields)
    conn = _connect()
    conn.execute(
        f"UPDATE logs SET {assignments} WHERE id = ?",
        [*fields.values(), log_id],
    )
    conn.commit()
    conn.close()


def delete_log(log_id: int) -> None:
    conn = _connect()
    conn.execute("DELETE FROM logs WHERE id = ?", (log_id,))
    conn.commit()
    conn.close()


def get_stats(config: dict) -> dict:
    conn = _connect()

    total = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]

    date_rows = conn.execute(
        "SELECT DISTINCT DATE(timestamp) AS d FROM logs ORDER BY d DESC"
    ).fetchall()
    dates = {row["d"] for row in date_rows}

    today = datetime.now().date()
    logged_today = today.strftime("%Y-%m-%d") in dates

    streak = 0
    check = today
    while check.strftime("%Y-%m-%d") in dates:
        streak += 1
        check -= timedelta(days=1)

    since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    week_rows = [dict(r) for r in conn.execute(
        "SELECT * FROM logs WHERE DATE(timestamp) >= ?", (since,)
    ).fetchall()]

    week_avg: dict = {}
    if week_rows:
        week_avg["mood"] = sum(r["mood"] for r in week_rows) / len(week_rows)
        if config.get("focus"):
            vals = [r["focus"] for r in week_rows if r.get("focus") is not None]
            if vals:
                week_avg["focus"] = sum(vals) / len(vals)
        if config.get("stress"):
            vals = [r["stress"] for r in week_rows if r.get("stress") is not None]
            if vals:
                week_avg["stress"] = sum(vals) / len(vals)

    conn.close()
    return {
        "total": total,
        "streak": streak,
        "logged_today": logged_today,
        "week_avg": week_avg,
    }


def get_weekly_mood_by_day() -> dict:
    """Get average mood for each day in the last 7 calendar days.

    Returns dict mapping date_str (YYYY-MM-DD) to average mood (float).
    Only includes days that have log entries.
    """
    since = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")
    conn = _connect()
    rows = conn.execute(
        "SELECT DATE(timestamp) as day, AVG(mood) as avg_mood FROM logs WHERE DATE(timestamp) >= ? GROUP BY day ORDER BY day",
        (since,),
    ).fetchall()
    conn.close()
    return {row["day"]: row["avg_mood"] for row in rows}


def get_monthly_scores(year: int, month: int, config: dict) -> dict:
    """Get avg mood/focus/stress per day for the given month.

    Returns dict mapping date_str (YYYY-MM-DD) to {field: avg_value}.
    """
    if month == 12:
        end_year, end_month = year + 1, 1
    else:
        end_year, end_month = year, month + 1

    start = f"{year:04d}-{month:02d}-01"
    end = f"{end_year:04d}-{end_month:02d}-01"

    select_fields = ["DATE(timestamp) as day", "AVG(mood) as mood"]
    if config.get("focus"):
        select_fields.append("AVG(focus) as focus")
    if config.get("stress"):
        select_fields.append("AVG(stress) as stress")

    conn = _connect()
    rows = conn.execute(
        f"SELECT {', '.join(select_fields)} FROM logs "
        "WHERE DATE(timestamp) >= ? AND DATE(timestamp) < ? GROUP BY day ORDER BY day",
        (start, end),
    ).fetchall()
    conn.close()

    result = {}
    for row in rows:
        d = dict(row)
        day = d.pop("day")
        result[day] = d
    return result
