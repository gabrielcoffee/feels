import csv
import json
from datetime import datetime
from pathlib import Path

from rich.console import Console

from .database import get_logs

console = Console()


def run_export(config: dict, args) -> None:
    format_type = args.format.lower()
    logs = get_logs(all_logs=True, newest_first=False)

    if not logs:
        console.print("\n[dim]No logs to export.[/dim]\n")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    home = Path.home()

    console.print()

    if format_type == "json":
        filename = f"feels_{timestamp}.json"
        path = home / filename

        try:
            with open(path, "w") as f:
                json.dump(logs, f, indent=2)
            console.print(f"[green]✓[/green] Exported {len(logs)} logs to [bold]{filename}[/bold]")
        except IOError as e:
            console.print(f"[red]Error:[/red] Failed to write JSON file. {str(e)}")

    elif format_type == "csv":
        filename = f"feels_{timestamp}.csv"
        path = home / filename

        if not logs:
            return

        try:
            fieldnames = list(logs[0].keys())
            with open(path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(logs)
            console.print(f"[green]✓[/green] Exported {len(logs)} logs to [bold]{filename}[/bold]")
        except IOError as e:
            console.print(f"[red]Error:[/red] Failed to write CSV file. {str(e)}")

    else:
        console.print(f"[red]Error:[/red] Unknown format: '{format_type}'. Use 'json' or 'csv'.")

    console.print()
