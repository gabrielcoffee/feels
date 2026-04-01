from datetime import datetime, timedelta

from rich.console import Console
from rich.prompt import Prompt

from .config import save_config
from .database import insert_log
from .utils import assign_project_color, prompt_asciimoji, prompt_score, score_color

console = Console()


def run_add(config: dict, date: str = None, yesterday: bool = False) -> None:
    try:
        entry = {}

        if date and yesterday:
            console.print("\n[red]Error:[/red] Cannot use --date and --yesterday together.\n")
            return

        now = datetime.now()

        if date:
            try:
                log_date = datetime.strptime(date, "%d-%m-%Y")
            except ValueError:
                console.print(f"\n[red]Error:[/red] Invalid date '{date}'. Use DD-MM-YYYY format (e.g. 30-03-2026)\n")
                return
            log_dt = log_date.replace(hour=now.hour, minute=now.minute, second=now.second)
        elif yesterday:
            yesterday_dt = now - timedelta(days=1)
            log_dt = yesterday_dt.replace(microsecond=0)
        else:
            log_dt = now

        console.print()

        if log_dt.date() != now.date():
            console.print(f"  [dim]Logging for {log_dt.strftime('%-d %b %Y')}[/dim]")
            console.print()

        # Project
        if config.get("projects"):
            val = Prompt.ask(
                f"  [bold]Project[/bold] [dim]({config['last_project']})[/dim]"
                if config.get("last_project")
                else "  [bold]Project[/bold]",
                default=config.get("last_project") or "",
            )
            entry["project"] = val.strip()

            if entry["project"]:
                active_projects = config.get("active_projects", [])
                if entry["project"] not in active_projects:
                    active_projects.append(entry["project"])
                    config["active_projects"] = active_projects
                assign_project_color(entry["project"], config)
                if entry["project"] != config.get("last_project"):
                    config["last_project"] = entry["project"]
                save_config(config)
            console.print()


        entry["mood"] = prompt_score(console, "Mood")
        console.print()

        # Focus
        if config.get("focus"):
            entry["focus"] = prompt_score(console, "Focus")
            console.print()

        # Stress
        if config.get("stress"):
            entry["stress"] = prompt_score(console, "Stress")
            console.print()

        # Note
        note = Prompt.ask("  [bold]Note[/bold] [dim](optional)[/dim]", default="")
        if note.strip():
            entry["note"] = note.strip()
        console.print()

        # Asciimoji — last, separate from mood
        if config.get("asciimoji"):
            entry["asciimoji"] = prompt_asciimoji(console)
            console.print()

        entry["timestamp"] = log_dt.isoformat(timespec="seconds")

        log_id = insert_log(entry)

        mood_color = score_color(entry["mood"])
        date_suffix = ""
        if log_dt.date() != now.date():
            date_suffix = f"  [dim]for {log_dt.strftime('%-d %b %Y')}[/dim]"
        console.print(
            f"[green]✓[/green] Logged [bold {mood_color}]{entry['mood']}/5[/bold {mood_color}] mood  [dim]#{log_id}[/dim]{date_suffix}"
        )
        console.print()
        console.print("Run [bold]feels[/bold] to start again.")
        console.print()
    except Exception as e:
        console.print(f"\n[red]Error:[/red] Failed to save entry. {str(e)}\n")
