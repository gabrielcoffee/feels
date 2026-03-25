from rich.console import Console

from .config import save_config

console = Console()


def run_project(config: dict, args) -> None:
    if not config.get("projects"):
        console.print("\n[red]Projects not enabled. Run 'feels config' to enable them.[/red]\n")
        return

    console.print()

    action = args.action
    name = args.name.strip() if hasattr(args, "name") and args.name else None
    projects = config.get("active_projects", [])

    if action == "add":
        if not name:
            console.print("[red]Project name required.[/red]")
        elif name in projects:
            console.print(f"[dim]Project '{name}' already exists.[/dim]")
        else:
            projects.append(name)
            config["active_projects"] = projects
            save_config(config)
            console.print(f"[green]✓[/green] Added project '{name}'")

    elif action == "list":
        if not projects:
            console.print("[dim]No projects yet.[/dim]")
        else:
            for p in projects:
                console.print(f"  {p}")

    elif action == "delete":
        if not name:
            console.print("[red]Project name required.[/red]")
        elif name not in projects:
            console.print(f"[red]Project '{name}' not found.[/red]")
        else:
            projects.remove(name)
            config["active_projects"] = projects
            save_config(config)
            console.print(f"[green]✓[/green] Deleted project '{name}'")

    console.print()
