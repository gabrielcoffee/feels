from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def run_help() -> None:
    console.print()

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column(style="bold")
    table.add_column(style="dim")

    table.add_row("feels", "show home screen")
    table.add_row("feels add", "log an entry")
    table.add_row("feels logs", "view entries (last 7 days)")
    table.add_row("feels logs --all", "view all entries ever")
    table.add_row("feels logs --oldest", "sort oldest first")
    table.add_row("feels logs --from YYYY-MM-DD", "custom start date")
    table.add_row("feels logs --to YYYY-MM-DD", "custom end date")
    table.add_row("feels logs --project <name>", "filter by project")
    table.add_row("feels edit <id>", "edit an entry")
    table.add_row("feels delete <id>", "delete an entry")
    table.add_row("feels config", "update settings")
    table.add_row("feels project add <name>", "add a project")
    table.add_row("feels project list", "show all projects")
    table.add_row("feels project delete <name>", "remove a project")
    table.add_row("feels stats", "view statistics")
    table.add_row("feels export --format json", "export logs as JSON")
    table.add_row("feels export --format csv", "export logs as CSV")
    table.add_row("feels help", "show this help")

    console.print(table)
    console.print()
