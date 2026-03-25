from rich.console import Console
from rich.prompt import Confirm

from .database import delete_log, get_log
from .utils import format_entry

console = Console()


def run_delete(config: dict, log_id: int) -> None:
    entry = get_log(log_id)

    if not entry:
        console.print(f"\n[red]No log found with id #{log_id}[/red]\n")
        return

    console.print()
    console.print(format_entry(entry, config))
    console.print()

    confirmed = Confirm.ask("  Are you sure you want to delete this entry?", default=False)

    console.print()
    if confirmed:
        delete_log(log_id)
        console.print(f"[green]✓[/green] Entry [dim]#{log_id}[/dim] deleted.")
    else:
        console.print("[dim]Cancelled.[/dim]")
    console.print()
