import random
from datetime import datetime, timedelta

import pyfiglet
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from .utils import score_color

console = Console()

_LOGO_FONTS = [
    "avatar", "big_money-sw", "big", "blocks", "cards",
    "bulbhead", "chiseled", "crazy", "dancing_font", "fire_font-s",
    "flower_power", "ghost", "isometric1", "slant_relief", "ascii12",
    "alligator", "georgia11", "kban",
]

_LOGO_COLORS = [
    "bold bright_blue",
    "bold bright_cyan",
    "bold bright_magenta",
    "bold bright_green",
    "bold bright_yellow",
]


def create_logo(seq: int = None) -> tuple:
    """Returns (logo Text, border_style str). seq cycles linearly; None uses random."""
    if seq is not None:
        font = _LOGO_FONTS[seq % len(_LOGO_FONTS)]
        color = _LOGO_COLORS[seq % len(_LOGO_COLORS)]
    else:
        font = random.choice(_LOGO_FONTS)
        color = random.choice(_LOGO_COLORS)
    border_color = color.replace("bold ", "")
    figlet_text = pyfiglet.figlet_format("feels", font=font)
    logo = Text()
    for i, line in enumerate(figlet_text.splitlines()):
        if i > 0:
            logo.append("\n")
        logo.append(line, style=color)
    return logo, border_color


def format_streak(streak: int) -> Text:
    """Format streak with styling based on day count."""
    if streak == 0:
        return Text("no streak yet", style="dim")

    # Color sequence for milestones
    colors = ["yellow", "bright_cyan", "magenta", "bright_green", "bright_blue", "bright_red", "bright_white"]

    # Calculate exclamation marks and styling
    if streak < 5:
        # Days 1-4: Number bold, text dim
        return Text.assemble(
            (str(streak), "bold"),
            (" day streak", "dim"),
        )
    elif streak < 7:
        # Days 5-6: Number bold, text dim
        return Text.assemble(
            (str(streak), "bold"),
            (" day streak", "dim"),
        )
    elif streak < 10:
        # Days 7-9: Number bold, text dim with !
        return Text.assemble(
            (str(streak), "bold"),
            (" day streak!", "dim"),
        )
    elif streak < 100:
        # Days 10-99: Number bold with color, text dim
        # Day 10: 2 !!, Day 20: 3 !!!, Day 30: 4 !!!!, etc.
        milestone_tier = streak // 10  # 10-19: tier 1, 20-29: tier 2, etc.
        color_index = (milestone_tier - 1) % len(colors)  # 1->0, 2->1, 3->2, etc
        color = colors[color_index]
        exclamations = "!" * (milestone_tier + 1)  # tier 1: 2 !!, tier 2: 3 !!!, etc.
        return Text.assemble(
            (str(streak), f"bold {color}"),
            (f" day streak{exclamations}", "dim"),
        )
    elif streak < 1000:
        # Days 100-999: Number bold with random color, text dim with !
        colors_100_plus = ["bright_cyan", "magenta", "bright_green", "bright_blue", "bright_red", "bright_white", "yellow"]
        color = random.choice(colors_100_plus)
        return Text.assemble(
            (str(streak), f"bold {color}"),
            (" day streak!", "dim"),
        )
    else:
        # Days 1000+: Number bold yellow, text dim with !
        return Text.assemble(
            (str(streak), "bold yellow"),
            (" day streak!", "dim"),
        )


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
            num_row.append(" ×", style="dim")
    rows.append(num_row)

    return rows


def show_home(config: dict, stats: dict, weekly_moods: dict = None, logo_seq: int = None) -> None:
    header, border_color = create_logo(seq=logo_seq)

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
    has_logs_this_week = bool(weekly_moods)
    name = config.get("name")

    if total == 0:
        if name:
            nudge = Text.assemble(
                (f"Welcome, {name} ", ""),
                ("run ", "dim"),
                ("feels log", f"bold {border_color}"),
                (" to log your first entry", "dim"),
            )
        else:
            nudge = Text.assemble(
                ("run ", "dim"),
                ("feels log", f"bold {border_color}"),
                (" to log your first entry", "dim"),
            )
    elif not stats["logged_today"]:
        nudge = Text.assemble(
        ("run ", "dim"),
        ("feels log", f"bold {border_color}"),
        (" and log your entry for today", "dim"),
        )
    else:
        nudge = None

    commands_label = Text("main commands:", style="bold")

    table = Table(box=None, show_header=False, padding=(0, 2), pad_edge=False)
    table.add_column(style="bold")
    table.add_column(style="dim")

    table.add_row("feels log", "log how you're feeling")
    table.add_row("feels logs", "view recent entries")
    table.add_row("feels reminder", "set a daily reminder")
    table.add_row("feels config", "update your settings")
    table.add_row("feels help", "see all available commands")

    rows = [
        header,
        Text(""),
        summary,
    ]

    # Mood matrix — only when there's at least 1 log this week
    if weekly_moods:
        rows.append(Text(""))
        rows += format_mood_matrix(weekly_moods)

    if nudge:
        rows += [Text(""), nudge]
    rows += [Text(""), commands_label, Text(""), table]

    # fls tip — shown until user has invoked fls at least once
    if not config.get("used_fls"):
        fls_tip = Text.assemble(
            ("Tip: You can also use ", "dim"),
            ("fls", "bold"),
            (" instead of feels!", "dim"),
        )
        rows += [Text(""), fls_tip]

    # calendar tip — shown after 2nd log until user runs calendar/graph for the first time
    if total >= 2 and not config.get("used_dash"):
        dash_tip = Text.assemble(
            ("Tip: run ", "dim"),
            ("feels calendar", "bold"),
            (" or ", "dim"),
            ("feels graph", "bold"),
            (" to see your monthly mood", "dim"),
        )
        rows += [Text(""), dash_tip]

    console.print()
    console.print(Panel(Group(*rows), border_style=border_color, padding=(1, 2)))
    console.print()
