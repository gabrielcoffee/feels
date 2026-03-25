from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm

console = Console()


def run_reset() -> None:
    """Delete all user data (config and database) with double confirmation."""
    console.print()

    # First confirmation
    first_confirm = Confirm.ask(
        "[yellow]This will delete all your logs, projects, and settings.[/yellow]\nAre you sure?",
        default=False,
    )

    if not first_confirm:
        console.print("[dim]Cancelled.[/dim]")
        console.print()
        return

    console.print()

    # Second confirmation with CAPSLOCK message
    second_confirm = Confirm.ask(
        "[red]THIS ACTION CANNOT BE UNDONE. ALL DATA WILL BE PERMANENTLY DELETED. ARE YOU SURE?[/red]",
        default=False,
    )

    if not second_confirm:
        console.print("[dim]Cancelled.[/dim]")
        console.print()
        return

    # Delete config and database
    config_dir = Path.home() / ".feels"
    config_file = config_dir / "config.json"
    db_file = config_dir / "data.db"

    deleted_count = 0

    if config_file.exists():
        config_file.unlink()
        deleted_count += 1

    if db_file.exists():
        db_file.unlink()
        deleted_count += 1

    console.print()
    if deleted_count > 0:
        console.print("[green]✓[/green] All data deleted. Run [bold]feels[/bold] to start fresh.")
    else:
        console.print("[dim]No data found to delete.[/dim]")

    console.print()
