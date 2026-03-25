import argparse

from .config import config_exists, load_config
from .database import db_exists, get_stats, init_db
from .home import show_home
from .onboarding import run_onboarding


def main():
    if not config_exists():
        run_onboarding()
        return

    config = load_config()

    if not db_exists():
        init_db(config)

    parser = argparse.ArgumentParser(prog="feels", add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("add")

    logs_p = subparsers.add_parser("logs")
    logs_p.add_argument("--all", dest="all", action="store_true")
    logs_p.add_argument("--oldest", action="store_true")
    logs_p.add_argument("--from", dest="from_date")
    logs_p.add_argument("--to", dest="to_date")
    logs_p.add_argument("--project")

    edit_p = subparsers.add_parser("edit")
    edit_p.add_argument("id", type=int)

    delete_p = subparsers.add_parser("delete")
    delete_p.add_argument("id", type=int)

    subparsers.add_parser("config")

    project_p = subparsers.add_parser("project")
    project_sub = project_p.add_subparsers(dest="action")
    add_proj = project_sub.add_parser("add")
    add_proj.add_argument("name")
    list_proj = project_sub.add_parser("list")
    del_proj = project_sub.add_parser("delete")
    del_proj.add_argument("name")

    subparsers.add_parser("stats")

    export_p = subparsers.add_parser("export")
    export_p.add_argument("--format", default="json", help="json or csv")

    subparsers.add_parser("help")

    args = parser.parse_args()

    if args.command == "add":
        from .add import run_add
        run_add(config)
    elif args.command == "logs":
        from .logs import run_logs
        run_logs(config, args)
    elif args.command == "edit":
        from .edit import run_edit
        run_edit(config, args.id)
    elif args.command == "delete":
        from .delete import run_delete
        run_delete(config, args.id)
    elif args.command == "config":
        from .config_cmd import run_config
        run_config(config)
    elif args.command == "project":
        from .project_cmd import run_project
        run_project(config, args)
    elif args.command == "stats":
        from .stats_cmd import run_stats
        run_stats(config)
    elif args.command == "export":
        from .export_cmd import run_export
        run_export(config, args)
    elif args.command == "help":
        from .help_cmd import run_help
        run_help()
    else:
        show_home(config, get_stats(config))
