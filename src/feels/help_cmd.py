from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()


def _section(title: str) -> None:
    console.print(Text(title, style="bold dim"))


def _table() -> Table:
    t = Table(box=None, show_header=False, padding=(0, 2), pad_edge=False)
    t.add_column(style="bold", no_wrap=True)
    t.add_column(style="dim")
    return t


def run_help() -> None:
    console.print()

    # General
    _section("general")
    t = _table()
    t.add_row("feels", "show home screen")
    t.add_row("feels log", "log an entry")
    t.add_row("feels log --yesterday", "log for yesterday")
    t.add_row("feels log --date DD-MM-YYYY", "log for a specific date")
    console.print(t)
    console.print()

    # Logs
    _section("logs")
    t = _table()
    t.add_row("feels logs", "view entries (last 7 days)")
    t.add_row("feels logs --all", "view all entries ever")
    t.add_row("feels logs --oldest", "sort oldest first")
    t.add_row("feels logs --from DD-MM-YYYY", "custom start date")
    t.add_row("feels logs --to DD-MM-YYYY", "custom end date")
    t.add_row("feels logs --project <name>", "filter by project")
    console.print(t)
    console.print()

    # Entries
    _section("entries")
    t = _table()
    t.add_row("feels edit <id>", "edit an entry")
    t.add_row("feels delete <id>", "delete one or more entries")
    console.print(t)
    console.print()

    # Projects
    _section("projects")
    t = _table()
    t.add_row("feels project add <name>", "add a project")
    t.add_row("feels project list", "show all projects")
    t.add_row("feels project delete <name>", "remove a project")
    console.print(t)
    console.print()

    # Data
    _section("data")
    t = _table()
    t.add_row("feels calendar", "monthly mood calendar")
    t.add_row("feels calendar --from MM-YYYY", "view a specific month")
    t.add_row("feels graph", "monthly bar chart")
    t.add_row("feels graph --from MM-YYYY", "bar chart for a specific month")
    t.add_row("feels stats", "view statistics")
    t.add_row("feels export --format json", "export logs as JSON")
    t.add_row("feels export --format csv", "export logs as CSV")
    t.add_row("feels reset", "delete all data (with confirmation)")
    console.print(t)
    console.print()

    # Reminder
    _section("reminder")
    t = _table()
    t.add_row("feels reminder", "show reminder status")
    t.add_row("feels reminder set HH:MM", "set a daily reminder")
    t.add_row("feels reminder unset", "remove the reminder")
    console.print(t)
    console.print()

    # Settings
    _section("settings")
    t = _table()
    t.add_row("feels config", "update settings")
    t.add_row("feels help", "show this help")
    console.print(t)
    console.print()
