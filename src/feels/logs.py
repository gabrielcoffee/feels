from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

from .database import get_logs
from .utils import format_entry, get_project_color, score_color
from .validation import validate_date, handle_invalid_date

console = Console()


def run_logs(config: dict, args) -> None:
    from_date = getattr(args, "from_date", None)
    to_date = getattr(args, "to_date", None)

    # Validate date formats
    if from_date and not validate_date(from_date):
        handle_invalid_date(from_date, "--from")
        return

    if to_date and not validate_date(to_date):
        handle_invalid_date(to_date, "--to")
        return

    try:
        logs = get_logs(
            from_date=from_date,
            to_date=to_date,
            project=getattr(args, "project", None),
            newest_first=not getattr(args, "oldest", False),
            all_logs=getattr(args, "all", False),
        )
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to retrieve logs. {str(e)}")
        return

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

        proj = entry.get("project")
        border = get_project_color(proj, config) if proj else score_color(entry["mood"])
        console.print(Panel.fit(
            format_entry(entry, config),
            border_style=border,
            padding=(0, 2),
        ))
        console.print()
