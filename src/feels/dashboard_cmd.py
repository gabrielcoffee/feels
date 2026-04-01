import calendar
from datetime import date

from rich.console import Console
from rich.text import Text

from .database import get_monthly_scores
from .utils import score_color

console = Console()

_DAY_LABELS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]


def run_dashboard(config: dict) -> None:
    today = date.today()
    scores = get_monthly_scores(today.year, today.month, config)

    console.print()
    _render_calendar(today, scores, "mood", "mood")

    if config.get("focus"):
        console.print()
        _render_calendar(today, scores, "focus", "focus")

    if config.get("stress"):
        console.print()
        _render_calendar(today, scores, "stress", "stress")

    console.print()


def _render_calendar(today: date, scores: dict, field: str, label: str) -> None:
    month_name = calendar.month_name[today.month]

    console.print(
        f"  [bold]{month_name} {today.year}[/bold]  [dim]{label}[/dim]"
    )
    console.print()

    # Day-name header
    header = Text("  ")
    for i, d in enumerate(_DAY_LABELS):
        if i > 0:
            header.append("   ")
        header.append(d, style="dim")
    console.print(header)

    # Weeks
    cal = calendar.monthcalendar(today.year, today.month)
    for week in cal:
        row = Text("  ")
        for i, day in enumerate(week):
            if i > 0:
                row.append("  ")
            if day == 0:
                row.append("   ")
            else:
                day_str = date(today.year, today.month, day).strftime("%Y-%m-%d")
                avg = scores.get(day_str, {}).get(field)
                day_label = f"{day:2d} "
                if avg is not None:
                    row.append(day_label, style=f"bold {score_color(round(avg))}")
                elif date(today.year, today.month, day) == today:
                    row.append(day_label, style="dim underline")
                else:
                    row.append(day_label, style="dim")
        console.print(row)
