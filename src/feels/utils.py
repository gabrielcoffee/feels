import math
import random
from datetime import datetime
from itertools import zip_longest
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

SCORE_COLORS = ["bright_red", "red", "orange1", "bright_yellow", "bright_green", "blue"]

REVERSE_COLORS = ["blue", "bright_green", "bright_yellow", "orange1", "red", "bright_red"]

ASCIIMOJIS = [
    (1,  "love",         "♥‿♥"),
    (2,  "sending love", "(づ๑•ᴗ•๑)づ♡"),
    (3,  "xoxo",         "( ˘ ³˘)♥"),
    (4,  "yay!",         "\\(^-^)/"),
    (5,  "happy",        "ᕕ( ᐛ )ᕗ"),
    (6,  "shy",          "(*ᴗ͈ˬᴗ͈)ꕤ*.ﾟ"),
    (7,  "i mean...",    "¯\\_(ツ)_/¯"),
    (8,  "duckface",     "(・3・)"),
    (9,  "awkward",      "•͡˘㇁•͡˘"),
    (10, "endure it",    "(҂ ◡ _ ◡ ) ᕤ"),
    (11, "cmon",         "(╯°□°）╯︵ ┻━┻"),
    (12, "oh no",        "ಠ_ಠ"),
    (13, "sad",          "(︶︹︶)"),
    (14, "crying",       "(╥﹏╥)"),
    (15, "hurt",         "(ಥ﹏ಥ)"),
    (16, "going insane", "ʘ ‿ ʘ"),
    (17, "mad",          "ᕙ( ᗒᗣᗕ )ᕗ"),
    (18, "screw you",    "╭∩╮( •̀_•́ )╭∩╮"),
    (19, "furious",      "(╬ಠ益ಠ)"),
]

_ASCIIMOJI_COLOR = {
    "love":         "bright_magenta",
    "sending love": "magenta",
    "xoxo":         "medium_orchid1",
    "yay!":         "bright_green",
    "happy":        "green",
    "shy":          "bright_yellow",
    "i mean...":    "yellow",
    "duckface":     "grey84",
    "awkward":      "grey62",
    "endure it":    "wheat1",
    "cmon":         "orange1",
    "oh no":        "dark_orange",
    "sad":          "steel_blue1",
    "crying":       "cornflower_blue",
    "hurt":         "blue",
    "going insane": "medium_purple1",
    "mad":          "red",
    "screw you":    "bright_red",
    "furious":      "red1",
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

    mid = math.ceil(len(ASCIIMOJIS) / 2)
    left = ASCIIMOJIS[:mid]
    right = ASCIIMOJIS[mid:]

    grid = Table(box=None, show_header=False, padding=(0, 1), pad_edge=False)
    grid.add_column(style="dim", justify="right", width=2, no_wrap=True)
    grid.add_column(width=12, no_wrap=True)
    grid.add_column(width=20, no_wrap=True)
    grid.add_column(style="dim", justify="right", width=2, no_wrap=True)
    grid.add_column(width=12, no_wrap=True)
    grid.add_column(no_wrap=True)

    for i, (l_item, r_item) in enumerate(zip_longest(left, right)):
        ln, lname, lface = l_item
        lcol = _ASCIIMOJI_COLOR.get(lname, "white")
        if r_item:
            rn, rname, rface = r_item
            rcol = _ASCIIMOJI_COLOR.get(rname, "white")
            grid.add_row(str(ln), lname, Text(lface, style=lcol), str(rn), rname, Text(rface, style=rcol))
        else:
            grid.add_row(str(ln), lname, Text(lface, style=lcol), "", "", Text(""))
        if i < len(left) - 1:
            grid.add_row("", "", Text(""), "", "", Text(""))

    console.print(grid)
    console.print()

    default_str = None
    if default_face:
        for num, _, face in ASCIIMOJIS:
            if face == default_face:
                default_str = str(num)
                break

    total = len(ASCIIMOJIS)
    while True:
        raw = Prompt.ask(f"  [dim]pick 1–{total}[/dim]", default=default_str)
        if raw is not None and str(raw).isdigit() and 1 <= int(raw) <= total:
            return ASCIIMOJIS[int(raw) - 1][2]
        console.print(f"  [red]Enter a number between 1 and {total}.[/red]\n")


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
        t.append(entry["note"])


    return t
