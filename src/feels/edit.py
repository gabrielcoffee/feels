from rich.console import Console
from rich.prompt import Prompt

from .database import get_log, update_log
from .utils import format_entry, prompt_score

console = Console()


def run_edit(config: dict, log_id: int) -> None:
    entry = get_log(log_id)

    if not entry:
        console.print(f"\n[red]No log found with id #{log_id}[/red]\n")
        return

    console.print()
    console.print(format_entry(entry, config))
    console.print()
    console.print("[dim]Press Enter to keep the current value, or type to replace it.[/dim]")
    console.print()

    updates = {}

    try:
        if config.get("projects") and entry.get("project") is not None:
            val = Prompt.ask("  [bold]Project[/bold]", default=entry.get("project") or "")
            if val != (entry.get("project") or ""):
                updates["project"] = val.strip() or None

        # Mood (always present) - use validated prompt
        mood = prompt_score(console, "Mood", default=entry["mood"])
        if mood != entry["mood"]:
            updates["mood"] = mood

        if config.get("focus") and entry.get("focus") is not None:
            focus = prompt_score(console, "Focus", default=entry.get("focus"))
            if focus != entry.get("focus"):
                updates["focus"] = focus

        if config.get("stress") and entry.get("stress") is not None:
            stress = prompt_score(console, "Stress", default=entry.get("stress"))
            if stress != entry.get("stress"):
                updates["stress"] = stress

        tags = Prompt.ask("  [bold]Tags[/bold]", default=entry.get("tags") or "")
        if tags != (entry.get("tags") or ""):
            updates["tags"] = tags.strip() or None

        note = Prompt.ask("  [bold]Note[/bold]", default=entry.get("note") or "")
        if note != (entry.get("note") or ""):
            updates["note"] = note.strip() or None

        console.print()
        if updates:
            update_log(log_id, updates)
            console.print(f"[green]✓[/green] Entry [dim]#{log_id}[/dim] updated.")
        else:
            console.print("[dim]No changes made.[/dim]")
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to update entry. {str(e)}")
    console.print()
