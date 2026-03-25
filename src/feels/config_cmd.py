from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table
from rich import box

from .config import save_config

console = Console()


def run_config(config: dict) -> None:
    console.print()

    # Show current config
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column(style="dim")
    table.add_column()

    table.add_row("mood", "[green]on[/green]")
    table.add_row("focus", "[green]on[/green]" if config.get("focus") else "[dim]off[/dim]")
    table.add_row("stress", "[green]on[/green]" if config.get("stress") else "[dim]off[/dim]")
    table.add_row("projects", "[green]on[/green]" if config.get("projects") else "[dim]off[/dim]")

    console.print("[bold]Current config:[/bold]")
    console.print(table)
    console.print()

    # Ask to update
    if Confirm.ask("Update any settings?", default=False):
        focus = Confirm.ask("  Enable focus score?", default=config.get("focus", False))
        stress = Confirm.ask("  Enable stress score?", default=config.get("stress", False))
        projects = Confirm.ask("  Enable projects?", default=config.get("projects", False))

        config["focus"] = focus
        config["stress"] = stress
        config["projects"] = projects

        if projects and "active_projects" not in config:
            config["active_projects"] = []

        save_config(config)
        console.print()
        console.print("[green]✓[/green] Config updated.")
    else:
        console.print("[dim]No changes.[/dim]")

    console.print()
