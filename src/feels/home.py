import random
from datetime import datetime, timedelta

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from .utils import score_color

console = Console()


def format_streak(streak: int) -> Text:
    """Format streak with styling based on day count."""
    if streak == 0:
        return Text("no streak yet", style="dim")

    # Color sequence for milestones
    colors = ["yellow", "bright_cyan", "magenta", "bright_green", "bright_blue", "bright_red", "bright_white"]

    # Calculate exclamation marks and styling
    if streak < 5:
        # Days 1-4: Just number bold
        streak_str = f"{streak}"
        return Text.assemble(
            (streak_str, "bold"),
            (" day streak", "dim"),
        )
    elif streak < 7:
        # Day 5-6: Whole text bold
        streak_str = f"{streak} day streak"
        return Text(streak_str, style="bold dim")
    elif streak < 10:
        # Day 7-9: Add one ! at the end
        streak_str = f"{streak} day streak!"
        return Text(streak_str, style="bold dim")
    elif streak < 100:
        # Days 10-99: Colors every 10 days with increasing !
        # Day 10: 2 !!, Day 20: 3 !!!, Day 30: 4 !!!!, etc.
        milestone_tier = streak // 10  # 10-19: tier 1, 20-29: tier 2, etc.
        color_index = (milestone_tier - 1) % len(colors)  # 1->0, 2->1, 3->2, etc
        color = colors[color_index]
        exclamations = "!" * (milestone_tier + 1)  # tier 1: 2 !!, tier 2: 3 !!!, etc.
        streak_str = f"{streak} day streak{exclamations}"
        return Text(streak_str, style=f"bold {color}")
    elif streak < 1000:
        # Days 100-999: Random color, one !, text bold
        colors_100_plus = ["bright_cyan", "magenta", "bright_green", "bright_blue", "bright_red", "bright_white", "yellow"]
        color = random.choice(colors_100_plus)
        streak_str = f"{streak} day streak!"
        return Text(streak_str, style=f"bold {color}")
    else:
        # Days 1000+: Yellow forever, whole text bold
        streak_str = f"{streak} day streak!"
        return Text(streak_str, style="bold yellow")


def format_mood_matrix(weekly_moods: dict) -> list:
    """Format a 7-day mood matrix visualization.

    Returns list of Text rows showing:
    - Day labels (Mo Tu We Th Fr Sa Su)
    - 5-row block chart (mood 1-5 from bottom to top)
    - Score numbers with colors

    weekly_moods: dict mapping date_str to avg_mood float
    """
    # Calculate last 7 calendar days
    today = datetime.now().date()
    days = [(today - timedelta(days=6 - i)) for i in range(7)]

    # Get mood scores for each day (None if no data)
    scores = []
    for day in days:
        day_str = day.strftime("%Y-%m-%d")
        if day_str in weekly_moods:
            scores.append(round(weekly_moods[day_str]))
        else:
            scores.append(None)

    # Constants for visual layout
    FILLED = "██"
    EMPTY = "  "
    GAP = " "

    # Day labels (weekday abbreviations)
    weekday_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    day_labels = Text()
    for i, day in enumerate(days):
        if i > 0:
            day_labels.append(GAP)
        day_labels.append(weekday_names[day.weekday()], style="dim")

    # Block rows (5 levels, top to bottom)
    rows = [day_labels]
    for level in range(5, 0, -1):
        row = Text()
        for i, score in enumerate(scores):
            if i > 0:
                row.append(GAP)
            if score is not None and score >= level:
                color = score_color(score)
                row.append(FILLED, style=color)
            else:
                row.append(EMPTY)
        rows.append(row)

    # Score numbers row
    num_row = Text()
    for i, score in enumerate(scores):
        if i > 0:
            num_row.append(GAP)
        if score is not None:
            color = score_color(score)
            num_row.append(f" {score}", style=f"dim {color}")
        else:
            num_row.append("  ", style="dim")
    rows.append(num_row)

    return rows


def show_home(config: dict, stats: dict, weekly_moods: dict = None) -> None:
    header = Text.assemble(
        ("Welcome to ", "bold"),
        ("feels", "bold bright_cyan"),
    )

    # Stats line
    total = stats["total"]
    streak = stats["streak"]

    # Format total logs: bold number, normal text
    total_num = Text(str(total), style="bold")
    total_text = Text(f" log{'s' if total != 1 else ''}", style="dim")

    # Format streak with special styling
    streak_text = format_streak(streak)

    summary = Text.assemble(
        total_num,
        total_text,
        ("  ·  ", "dim"),
        streak_text,
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

    # Add mood matrix if user has 7+ day streak
    if streak >= 7 and weekly_moods:
        rows.append(Text(""))
        rows += format_mood_matrix(weekly_moods)

    if nudge:
        rows += [Text(""), nudge]
    rows += [Text(""), commands_label, Text(""), table]

    console.print()
    console.print(Panel(Group(*rows), border_style="bright_black", padding=(1, 4)))
    console.print()
