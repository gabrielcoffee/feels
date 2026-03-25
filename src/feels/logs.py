from datetime import datetime

from rich.console import Console
from rich.rule import Rule

from .database import get_logs
from .utils import format_entry

console = Console()


def run_logs(config: dict, args) -> None:
    logs = get_logs(
        from_date=getattr(args, "from_date", None),
        to_date=getattr(args, "to_date", None),
        project=getattr(args, "project", None),
        newest_first=not getattr(args, "oldest", False),
        all_logs=getattr(args, "all", False),
    )

    console.print()

    if not logs:
        console.print("[dim]  No logs found.[/dim]")
        console.print()
        return

    current_day = None
    for entry in logs:
        ts = datetime.fromisoformat(entry["timestamp"])
        day = ts.date()

        if day != current_day:
            current_day = day
            console.print(Rule(f"[dim]{ts.strftime('%B %-d, %Y')}[/dim]", style="bright_black"))
            console.print()

        console.print(format_entry(entry, config))
        console.print()
