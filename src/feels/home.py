from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()


def show_home(config: dict, stats: dict) -> None:
    header = Text.assemble(
        ("Welcome to ", "bold"),
        ("feels", "bold bright_cyan"),
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

    # Nudge
    if total == 0:
        nudge = Text("run feels add to log your first entry", style="dim")
    elif not stats["logged_today"]:
        nudge = Text("haven't logged today yet", style="dim")
    else:
        nudge = None

    commands_label = Text("main commands:", style="bold")

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
    ]
    if nudge:
        rows += [Text(""), nudge]
    rows += [Text(""), commands_label, Text(""), table]

    console.print()
    console.print(Panel(Group(*rows), border_style="bright_black", padding=(1, 4)))
    console.print()
