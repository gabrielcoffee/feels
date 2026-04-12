import calendar
from datetime import date

from rich.console import Console
from rich.text import Text

from .database import get_monthly_scores
from .utils import score_color, score_reverse_color

console = Console()

FILLED = "██"
EMPTY = "  "
GAP = " "


def run_graph(config: dict, year: int = None, month: int = None) -> None:
    today = date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month

    scores = get_monthly_scores(year, month, config)

    console.print()
    _render_graph(year, month, today, scores, "mood", score_color)

    if config.get("focus"):
        console.print()
        _render_graph(year, month, today, scores, "focus", score_color)

    if config.get("stress"):
        console.print()
        _render_graph(year, month, today, scores, "stress", score_reverse_color)

    console.print()


def _render_graph(year: int, month: int, today: date, scores: dict, field: str, color_fn) -> None:
    days_in_month = calendar.monthrange(year, month)[1]
    month_name = calendar.month_name[month]

    console.print(f"  [bold]{month_name} {year}[/bold]  [dim]{field}[/dim]")
    console.print()

    # One score per day (None if no data)
    day_scores = []
    for d in range(1, days_in_month + 1):
        day_str = date(year, month, d).strftime("%Y-%m-%d")
        avg = scores.get(day_str, {}).get(field)
        day_scores.append(round(avg) if avg is not None else None)

    # Day number header
    header = Text("  ")
    for i, d in enumerate(range(1, days_in_month + 1)):
        if i > 0:
            header.append(GAP)
        header.append(f"{d:2d}", style="dim")
    console.print(header)

    # Block rows — level 5 at top, level 1 at bottom
    for level in range(5, 0, -1):
        row = Text("  ")
        for i, score in enumerate(day_scores):
            if i > 0:
                row.append(GAP)
            if score is not None and score >= level:
                row.append(FILLED, style=color_fn(score))
            else:
                row.append(EMPTY)
        console.print(row)

    # Score numbers row
    num_row = Text("  ")
    for i, score in enumerate(day_scores):
        if i > 0:
            num_row.append(GAP)
        if score is not None:
            num_row.append(f" {score}", style=f"dim {color_fn(score)}")
        else:
            num_row.append(" ×", style="dim")
    console.print(num_row)
