from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text
from rich import box

from .config import save_config
from .home import create_logo

console = Console()


def run_onboarding() -> None:
    logo, border_color = create_logo()

    console.print()
    console.print(Panel(
        Group(logo, Text(""), Text("A mood tracker and journal for developers. Runs entirely in your terminal. \n\nLet's start your journey!", style="dim")), 
        border_style=border_color,
        padding=(1, 2),
    ))
    console.print()

    name = Prompt.ask("  [bold]What's your name?[/bold] [dim](optional)[/dim]", default="")
    console.print()

    use_defaults = Confirm.ask(
        "  [bold]Start with default config?[/bold] [dim](mood, asciimoji and note)[/dim]",
        default=True,
    )

    if use_defaults:
        config = {
            "focus": False,
            "stress": False,
            "projects": False,
            "asciimoji": True,
        }
    else:
        console.print()
        focus = Confirm.ask("  Add [bold]Focus[/bold] score? [dim](0–5)[/dim]", default=False)
        stress = Confirm.ask("  Add [bold]Stress[/bold] score? [dim](0–5)[/dim]", default=False)
        projects = Confirm.ask("  Enable [bold]projects[/bold]? [dim](separate logs by project)[/dim]", default=False)
        asciimoji = Confirm.ask("  Enable [bold]asciimoji[/bold]? [dim](pick mood from ASCII faces)[/dim]", default=True)

        config = {
            "focus": focus,
            "stress": stress,
            "projects": projects,
            "asciimoji": asciimoji,
        }

    if name.strip():
        config["name"] = name.strip()

    _show_summary(config)

    save_config(config)
    console.print()
    console.print("[green]✓[/green] Config saved. Run [bold bright_cyan]feels[/bold bright_cyan] to get started.")
    console.print()


def _show_summary(config: dict) -> None:
    console.print()

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column(style="dim")
    table.add_column()

    table.add_row("mood", "[green]always on[/green]")
    table.add_row("focus", "[green]on[/green]" if config["focus"] else "[dim]off[/dim]")
    table.add_row("stress", "[green]on[/green]" if config["stress"] else "[dim]off[/dim]")
    table.add_row("projects", "[green]on[/green]" if config["projects"] else "[dim]off[/dim]")
    table.add_row("notes", "[green]always on[/green]")
    table.add_row("asciimoji", "[green]on[/green]" if config.get("asciimoji") else "[dim]off[/dim]")

    console.print("[bold]Your config:[/bold]")
    console.print(table)
