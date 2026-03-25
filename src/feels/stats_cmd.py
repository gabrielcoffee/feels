from datetime import datetime, timedelta

from rich.console import Console
from rich.table import Table
from rich import box

from .database import get_logs
from .utils import score_color

console = Console()


def run_stats(config: dict) -> None:
    console.print()

    all_logs = get_logs(all_logs=True, newest_first=False)

    if not all_logs:
        console.print("[dim]No logs yet.[/dim]")
        console.print()
        return

    # Overall stats
    moods = [log["mood"] for log in all_logs]
    avg_mood = sum(moods) / len(moods)
    best_mood = max(moods)
    worst_mood = min(moods)

    console.print("[bold]Overall[/bold]")
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column(style="dim")
    table.add_column()
    table.add_row("total logs", str(len(all_logs)))
    table.add_row(
        "avg mood",
        f"{avg_mood:.1f}/5",
        style=f"bold {score_color(round(avg_mood))}",
    )
    table.add_row("best", f"{best_mood}/5", style=f"bold {score_color(best_mood)}")
    table.add_row("worst", f"{worst_mood}/5", style=f"bold {score_color(worst_mood)}")
    console.print(table)

    # Optional scores
    if config.get("focus"):
        focuses = [log["focus"] for log in all_logs if log.get("focus") is not None]
        if focuses:
            console.print()
            console.print("[bold]Focus[/bold]")
            table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
            table.add_column(style="dim")
            table.add_column()
            avg_focus = sum(focuses) / len(focuses)
            table.add_row("avg", f"{avg_focus:.1f}/5", style=f"bold {score_color(round(avg_focus))}")
            table.add_row("best", f"{max(focuses)}/5", style=f"bold {score_color(max(focuses))}")
            table.add_row("worst", f"{min(focuses)}/5", style=f"bold {score_color(min(focuses))}")
            console.print(table)

    if config.get("stress"):
        stresses = [log["stress"] for log in all_logs if log.get("stress") is not None]
        if stresses:
            console.print()
            console.print("[bold]Stress[/bold]")
            table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
            table.add_column(style="dim")
            table.add_column()
            avg_stress = sum(stresses) / len(stresses)
            table.add_row("avg", f"{avg_stress:.1f}/5", style=f"bold {score_color(round(avg_stress))}")
            table.add_row("best", f"{min(stresses)}/5", style=f"bold {score_color(min(stresses))}")
            table.add_row("worst", f"{max(stresses)}/5", style=f"bold {score_color(max(stresses))}")
            console.print(table)

    # Weekly breakdown
    console.print()
    console.print("[bold]Last 7 days[/bold]")
    since = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")
    week_logs = get_logs(from_date=since, newest_first=False)
    if week_logs:
        week_moods = [log["mood"] for log in week_logs]
        week_avg = sum(week_moods) / len(week_moods)
        table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
        table.add_column(style="dim")
        table.add_column()
        table.add_row("logs this week", str(len(week_logs)))
        table.add_row(
            "avg mood",
            f"{week_avg:.1f}/5",
            style=f"bold {score_color(round(week_avg))}",
        )
        console.print(table)
    else:
        console.print("[dim]No logs in the last 7 days.[/dim]")

    console.print()
