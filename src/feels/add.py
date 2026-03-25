from datetime import datetime

from rich.console import Console
from rich.prompt import Prompt

from .config import load_config, save_config
from .database import insert_log
from .utils import prompt_score, score_color

console = Console()


def run_add(config: dict) -> None:
    try:
        entry = {}

        console.print()

        # Project
        if config.get("projects"):
            last = config.get("last_project")
            if last:
                val = Prompt.ask(f"  [bold]Project[/bold] [dim]({last})[/dim]", default=last)
            else:
                val = Prompt.ask("  [bold]Project[/bold]")
            entry["project"] = val.strip()

            if entry["project"]:
                # Auto-add project if it doesn't exist
                active_projects = config.get("active_projects", [])
                if entry["project"] not in active_projects:
                    active_projects.append(entry["project"])
                    config["active_projects"] = active_projects

                # Update last_project
                if entry["project"] != config.get("last_project"):
                    config["last_project"] = entry["project"]

                save_config(config)

        # Scores
        entry["mood"] = prompt_score(console, "Mood")

        if config.get("focus"):
            entry["focus"] = prompt_score(console, "Focus")

        if config.get("stress"):
            entry["stress"] = prompt_score(console, "Stress")

        # Tags
        console.print()
        tags = Prompt.ask("  [bold]Tags[/bold] [dim](optional, e.g. #work #tired)[/dim]", default="")
        if tags.strip():
            entry["tags"] = tags.strip()

        # Note
        note = Prompt.ask("  [bold]Note[/bold] [dim](optional)[/dim]", default="")
        if note.strip():
            entry["note"] = note.strip()

        entry["timestamp"] = datetime.now().isoformat(timespec="seconds")

        log_id = insert_log(entry)

        mood_color = score_color(entry["mood"])
        console.print()
        console.print(
            f"[green]✓[/green] Logged [bold {mood_color}]{entry['mood']}/5[/bold {mood_color}] mood  [dim]#{log_id}[/dim]"
        )
        console.print()
    except Exception as e:
        console.print(f"\n[red]Error:[/red] Failed to save entry. {str(e)}\n")
