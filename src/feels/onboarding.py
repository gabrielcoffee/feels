from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text
from rich import box

from .config import save_config

console = Console()


def run_onboarding() -> None:
    welcome = Text.assemble(
        ("Welcome to ", "bold"),
        ("feels", "bold bright_cyan"),
        "\n",
        ("A mood tracker for developers. Runs entirely in your terminal.", "dim"),
    )

    console.print()
    console.print(Panel.fit(
        welcome,
        border_style="bright_black",
        padding=(1, 4),
    ))
    console.print()

    use_defaults = Confirm.ask(
        "[bold]Start with default config?[/bold] [dim](mood score, tags and note)[/dim]",
        default=True,
    )

    if use_defaults:
        config = {
            "focus": False,
            "stress": False,
            "projects": False,
        }
    else:
        console.print()
        focus = Confirm.ask("  Add [bold]Focus[/bold] score? [dim](0–5)[/dim]", default=False)
        stress = Confirm.ask("  Add [bold]Stress[/bold] score? [dim](0–5)[/dim]", default=False)
        projects = Confirm.ask("  Enable [bold]projects[/bold]? [dim](separate logs by project)[/dim]", default=False)

        config = {
            "focus": focus,
            "stress": stress,
            "projects": projects,
        }

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

    table.add_row("mood score", "[green]always on[/green]")
    table.add_row("focus score", "[green]on[/green]" if config["focus"] else "[dim]off[/dim]")
    table.add_row("stress score", "[green]on[/green]" if config["stress"] else "[dim]off[/dim]")
    table.add_row("projects", "[green]on[/green]" if config["projects"] else "[dim]off[/dim]")
    table.add_row("tags", "[green]always on[/green]")
    table.add_row("notes", "[green]always on[/green]")

    console.print("[bold]Your config:[/bold]")
    console.print(table)
