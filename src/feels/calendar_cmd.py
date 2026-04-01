import calendar
from datetime import date

from rich.console import Console
from rich.text import Text

from .database import get_monthly_scores
from .utils import score_color, score_reverse_color

console = Console()

_DAY_LABELS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]


def parse_month_arg(s: str, current_year: int) -> tuple[int, int] | None:
    """Parse MM-YYYY or MM into (year, month). Returns None on invalid input."""
    import re
    m = re.match(r'^(\d{1,2})-(\d{4})$', s)
    if m:
        month, year = int(m.group(1)), int(m.group(2))
    else:
        m = re.match(r'^(\d{1,2})$', s)
        if m:
            month, year = int(m.group(1)), current_year
        else:
            return None
    if not 1 <= month <= 12:
        return None
    return year, month


def run_calendar(config: dict, year: int = None, month: int = None) -> None:
    today = date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month

    scores = get_monthly_scores(year, month, config)

    console.print()
    _render_calendar(year, month, today, scores, "mood", "mood", score_color)

    if config.get("focus"):
        console.print()
        _render_calendar(year, month, today, scores, "focus", "focus", score_color)

    if config.get("stress"):
        console.print()
        _render_calendar(year, month, today, scores, "stress", "stress", score_reverse_color)

    console.print()


def _render_calendar(year: int, month: int, today: date, scores: dict, field: str, label: str, color_fn) -> None:
    month_name = calendar.month_name[month]

    console.print(f"  [bold]{month_name} {year}[/bold]  [dim]{label}[/dim]")
    console.print()

    header = Text("  ")
    for i, d in enumerate(_DAY_LABELS):
        if i > 0:
            header.append("   ")
        header.append(d, style="dim")
    console.print(header)

    cal = calendar.monthcalendar(year, month)
    for week in cal:
        row = Text("  ")
        for i, day in enumerate(week):
            if i > 0:
                row.append("  ")
            if day == 0:
                row.append("   ")
            else:
                day_date = date(year, month, day)
                day_str = day_date.strftime("%Y-%m-%d")
                avg = scores.get(day_str, {}).get(field)
                day_label = f"{day:2d} "
                if avg is not None:
                    row.append(day_label, style=f"bold {color_fn(round(avg))}")
                elif day_date == today:
                    row.append(day_label, style="dim underline")
                else:
                    row.append(day_label, style="dim")
        console.print(row)
