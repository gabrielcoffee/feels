from rich.console import Console
from rich.prompt import Confirm

from .database import delete_log, get_log
from .utils import format_entry

console = Console()


def run_delete(config: dict, log_ids: list) -> None:
    entries = {}
    not_found = []

    for log_id in log_ids:
        entry = get_log(log_id)
        if entry:
            entries[log_id] = entry
        else:
            not_found.append(log_id)

    if not_found:
        if len(not_found) == 1:
            console.print(f"\n[red]No log found with id #{not_found[0]}[/red]\n")
        else:
            console.print(f"\n[red]No logs found with ids #{', #'.join(map(str, not_found))}[/red]\n")

    if not entries:
        return

    console.print()
    for log_id, entry in entries.items():
        console.print(format_entry(entry, config))
        console.print()

    id_list = ", ".join(f"#{id}" for id in entries.keys())
    confirmed = Confirm.ask(f"  Are you sure you want to delete {len(entries)} {'entry' if len(entries) == 1 else 'entries'} ({id_list})?", default=False)

    console.print()
    if confirmed:
        for log_id in entries.keys():
            delete_log(log_id)
        if len(entries) == 1:
            console.print(f"[green]✓[/green] Entry [dim]#{list(entries.keys())[0]}[/dim] deleted.")
        else:
            console.print(f"[green]✓[/green] {len(entries)} entries deleted.")
    else:
        console.print("[dim]Cancelled.[/dim]")
    console.print()
