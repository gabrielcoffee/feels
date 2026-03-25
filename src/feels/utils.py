from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

SCORE_COLORS = ["white", "bright_red", "orange1", "bright_yellow", "bright_green", "blue"]


def score_color(score: int) -> str:
    return SCORE_COLORS[max(0, min(5, score))]


def prompt_score(console: Console, label: str, default: Optional[int] = None) -> int:
    default_str = str(default) if default is not None else None
    while True:
        raw = Prompt.ask(f"  [bold]{label}[/bold] [dim](0–5)[/dim]", default=default_str)
        if raw is not None and str(raw).isdigit() and 0 <= int(raw) <= 5:
            return int(raw)
        console.print("  [red]Enter a number between 0 and 5.[/red]")


def format_entry(entry: dict, config: dict) -> Text:
    ts = datetime.fromisoformat(entry["timestamp"])
    time_str = ts.strftime("%H:%M")

    t = Text()

    # Header line: #id  ·  time  ·  project
    t.append(f"#{entry['id']}", style="bold dim")
    t.append("  ·  ", style="dim")
    t.append(time_str, style="bold")
    if entry.get("project"):
        t.append("  ·  ", style="dim")
        t.append(entry["project"], style="bright_cyan")
    t.append("\n")

    # Scores line
    mood_color = score_color(entry["mood"])
    t.append(f"{entry['mood']}/5", style=f"bold {mood_color}")

    if config.get("focus") and entry.get("focus") is not None:
        t.append("  ")
        t.append(f"{entry['focus']}/5", style=f"bold {score_color(entry['focus'])}")
        t.append(" focus", style="dim")

    if config.get("stress") and entry.get("stress") is not None:
        t.append("  ")
        t.append(f"{entry['stress']}/5", style=f"bold {score_color(entry['stress'])}")
        t.append(" stress", style="dim")

    if entry.get("tags"):
        t.append(f"  {entry['tags']}", style="bright_cyan")

    # Note line
    if entry.get("note"):
        t.append(f"\n{entry['note']}", style="italic dim")

    return t
