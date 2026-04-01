import random
from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

SCORE_COLORS = ["bright_red", "red", "orange1", "bright_yellow", "bright_green", "blue"]

REVERSE_COLORS = ["blue", "bright_green", "bright_yellow", "orange1", "red", "bright_red"]

ASCIIMOJIS = [
    (1,  "cry",     "(╥﹏╥)"),
    (2,  "sad",     "(︶︹︶)"),
    (3,  "afraid",  "(ㆆ _ ㆆ)"),
    (4,  "angry",   "•`_´•"),
    (5,  "tired",   "(=____=)"),
    (6,  "bored",   "(-_-)"),
    (7,  "shy",     "=^_^="),
    (8,  "awkward", "•͡˘㇁•͡˘"),
    (9,  "happy",   "(´• ω •`)"),
    (10, "love",    "♥‿♥"),
]

_ASCIIMOJI_COLOR = {
    "cry":     "blue",
    "sad":     "blue",
    "afraid":  "bright_red",
    "angry":   "bright_red",
    "tired":   "orange1",
    "bored":   "orange1",
    "shy":     "bright_yellow",
    "awkward": "bright_yellow",
    "happy":   "bright_green",
    "love":    "bright_magenta",
}

PROJECT_COLORS = [
    "bright_blue", "bright_cyan", "bright_magenta", "bright_green",
    "bright_yellow", "cyan", "blue", "magenta", "green", "yellow",
]


def score_color(score: int) -> str:
    return SCORE_COLORS[max(0, min(5, score))]

def score_reverse_color(score: int) -> str:
    return REVERSE_COLORS[max(0, min(5, score))]

def get_project_color(project: str, config: dict) -> str:
    return config.get("project_colors", {}).get(project, "bright_cyan")


def assign_project_color(project: str, config: dict) -> str:
    """Assign a random color to a project if it doesn't have one yet."""
    colors = config.get("project_colors", {})
    if project not in colors:
        used = set(colors.values())
        available = [c for c in PROJECT_COLORS if c not in used]
        colors[project] = random.choice(available if available else PROJECT_COLORS)
        config["project_colors"] = colors
    return colors[project]


def prompt_asciimoji(console: Console, default_face: Optional[str] = None) -> str:
    """Asciimoji picker — 2-column grid, returns the selected face string."""
    console.print("  [bold]Asciimoji[/bold] [dim](how are you feeling?)[/dim]")
    console.print()

    left = ASCIIMOJIS[:5]
    right = ASCIIMOJIS[5:]

    grid = Table(box=None, show_header=False, padding=(0, 1), pad_edge=False)
    grid.add_column(style="dim", justify="right", width=2, no_wrap=True)
    grid.add_column(width=8, no_wrap=True)
    grid.add_column(width=20, no_wrap=True)
    grid.add_column(style="dim", justify="right", width=2, no_wrap=True)
    grid.add_column(width=8, no_wrap=True)
    grid.add_column(no_wrap=True)

    for i, ((ln, lname, lface), (rn, rname, rface)) in enumerate(zip(left, right)):
        lcol = _ASCIIMOJI_COLOR.get(lname, "white")
        rcol = _ASCIIMOJI_COLOR.get(rname, "white")
        grid.add_row(
            str(ln), lname, Text(lface, style=lcol),
            str(rn), rname, Text(rface, style=rcol),
        )
        if i < 4:
            grid.add_row("", "", Text(""), "", "", Text(""))

    console.print(grid)
    console.print()

    default_str = None
    if default_face:
        for num, _, face in ASCIIMOJIS:
            if face == default_face:
                default_str = str(num)
                break

    while True:
        raw = Prompt.ask("  [dim]pick 1–10[/dim]", default=default_str)
        if raw is not None and str(raw).isdigit() and 1 <= int(raw) <= 10:
            return ASCIIMOJIS[int(raw) - 1][2]
        console.print("  [red]Enter a number between 1 and 10.[/red]\n")


def prompt_score(console: Console, label: str, default: Optional[int] = None) -> int:
    default_str = str(default) if default is not None else None
    while True:
        raw = Prompt.ask(f"  [bold]{label}[/bold] [dim](0–5)[/dim]", default=default_str)
        if raw is not None and str(raw).isdigit() and 0 <= int(raw) <= 5:
            return int(raw)
        console.print("  [red]Enter a number between 0 and 5.[/red]\n")


def format_entry(entry: dict, config: dict) -> Text:
    ts = datetime.fromisoformat(entry["timestamp"])
    time_str = ts.strftime("%H:%M")

    t = Text()

    # Header: #id  ·  time  ·  Project
    t.append(f"#{entry['id']}", style="bold dim")
    t.append("  ·  ", style="dim")
    t.append(time_str, style="bold")
    if entry.get("project"):
        proj_color = get_project_color(entry["project"], config)
        t.append("  ·  ", style="dim")
        t.append(entry["project"], style=f"bold {proj_color}")
    t.append("\n")

    # MOOD
    t.append("Mood", style="bold dim")
    t.append("  ")
    t.append(f"{entry['mood']}/5", style=f"bold {score_color(entry['mood'])}")

    # FOCUS
    if config.get("focus") and entry.get("focus") is not None:
        t.append("\n")
        t.append("Focus", style="bold dim")
        t.append("  ")
        t.append(f"{entry['focus']}/5", style=f"bold {score_color(entry['focus'])}")

    # STRESS
    if config.get("stress") and entry.get("stress") is not None:
        t.append("\n")
        t.append("Stress", style="bold dim")
        t.append("  ")
        t.append(f"{entry['stress']}/5", style=f"bold {score_reverse_color(entry['stress'])}")

    # Asciimoji
    if entry.get("asciimoji"):
        face = entry["asciimoji"]
        face_name = ""
        face_color = "white"
        for _, name, f in ASCIIMOJIS:
            if f == face:
                face_name = name
                face_color = _ASCIIMOJI_COLOR.get(name, "white")
                break
        t.append("\n")
        t.append(face, style=face_color)
        if face_name:
            t.append(f"  {face_name}", style="dim")

    # Note
    if entry.get("note"):
        t.append("\n")
        t.append("", style="bold")
        t.append("\n")
        t.append(entry["note"])


    return t
