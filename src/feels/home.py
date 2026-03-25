from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from .utils import score_color

console = Console()


def show_home(config: dict, stats: dict) -> None:
    header = Text.assemble(
        ("Welcome to ", "bold"),
        ("feels", "bold bright_cyan"),
        "\n",
        ("A mood tracker for developers. Runs entirely in your terminal.", "dim"),
    )

    # Stats line
    total = stats["total"]
    streak = stats["streak"]
    total_label = f"{total} log{'s' if total != 1 else ''}"
    streak_label = f"{streak} day streak" if streak > 0 else "no streak yet"
    summary = Text.assemble(
        (total_label, "dim"),
        ("  ·  ", "dim"),
        (streak_label, "dim"),
    )

    # Week averages or nudge for new users
    week_avg = stats["week_avg"]
    if week_avg:
        avgs = Text.assemble(("avg this week:  ", "dim"))
        avgs.append(f"{week_avg['mood']:.1f}/5", style=f"bold {score_color(round(week_avg['mood']))}")
        avgs.append(" mood", style="dim")
        if "focus" in week_avg:
            avgs.append("  ")
            avgs.append(f"{week_avg['focus']:.1f}/5", style=f"bold {score_color(round(week_avg['focus']))}")
            avgs.append(" focus", style="dim")
        if "stress" in week_avg:
            avgs.append("  ")
            avgs.append(f"{week_avg['stress']:.1f}/5", style=f"bold {score_color(round(week_avg['stress']))}")
            avgs.append(" stress", style="dim")
    else:
        avgs = Text("no logs in the last 7 days", style="dim")

    # Nudge
    if total == 0:
        nudge = Text("run feels add to log your first entry", style="dim")
    elif not stats["logged_today"]:
        nudge = Text("haven't logged today yet", style="dim")
    else:
        nudge = None

    commands_label = Text("commands:", style="bold")

    table = Table(box=None, show_header=False, padding=(0, 2), pad_edge=False)
    table.add_column(style="bold")
    table.add_column(style="dim")

    table.add_row("feels add", "log how you're feeling")
    table.add_row("feels logs", "view recent entries")
    table.add_row("feels config", "update your settings")
    table.add_row("feels help", "see all available commands")

    rows = [
        header,
        Text(""),
        summary,
        Text(""),
        avgs,
    ]
    if nudge:
        rows += [Text(""), nudge]
    rows += [Text(""), commands_label, Text(""), table]

    console.print()
    console.print(Panel(Group(*rows), border_style="bright_black", padding=(1, 4)))
    console.print()
