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
    else:
        show_home(config, get_stats(config))
