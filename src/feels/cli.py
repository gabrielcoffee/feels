import argparse
import os
import sys

from .config import config_exists, load_config, save_config
from .database import db_exists, ensure_columns, get_stats, get_weekly_mood_by_day, init_db
from .home import show_home
from .onboarding import run_onboarding


def main():
    try:
        _run()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        sys.exit(0)


def _run():
    if not config_exists():
        run_onboarding()
        return

    config = load_config()

    # Track first fls usage so the tip can be hidden afterwards
    if os.path.basename(sys.argv[0]) == "fls" and not config.get("used_fls"):
        config["used_fls"] = True
        save_config(config)

    if not db_exists():
        init_db(config)
    else:
        ensure_columns(config)

    parser = argparse.ArgumentParser(prog="feels", add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("log")
    add_p.add_argument("--date", dest="date", metavar="DD-MM-YYYY", help="Log for a specific date")
    add_p.add_argument("--yesterday", action="store_true", help="Log for yesterday")

    logs_p = subparsers.add_parser("logs")
    logs_p.add_argument("--all", dest="all", action="store_true")
    logs_p.add_argument("--oldest", action="store_true")
    logs_p.add_argument("--from", dest="from_date")
    logs_p.add_argument("--to", dest="to_date")
    logs_p.add_argument("--project")

    edit_p = subparsers.add_parser("edit")
    edit_p.add_argument("id", type=int)

    delete_p = subparsers.add_parser("delete")
    delete_p.add_argument("ids", nargs='+', type=int, metavar="id")

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

    subparsers.add_parser("reset")

    subparsers.add_parser("dashboard")

    reminder_p = subparsers.add_parser("reminder")
    reminder_sub = reminder_p.add_subparsers(dest="action")
    set_r = reminder_sub.add_parser("set")
    set_r.add_argument("time", metavar="HH:MM")
    reminder_sub.add_parser("unset")

    subparsers.add_parser("help")

    args = parser.parse_args()

    if args.command == "log":
        from .add import run_add
        run_add(config, date=args.date, yesterday=args.yesterday)
    elif args.command == "logs":
        from .logs import run_logs
        run_logs(config, args)
    elif args.command == "edit":
        from .edit import run_edit
        run_edit(config, args.id)
    elif args.command == "delete":
        from .delete import run_delete
        run_delete(config, args.ids)
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
    elif args.command == "reset":
        from .reset_cmd import run_reset
        run_reset()
    elif args.command == "dashboard":
        from .dashboard_cmd import run_dashboard
        run_dashboard(config)
    elif args.command == "reminder":
        from .reminder_cmd import run_reminder
        run_reminder(config, args)
    elif args.command == "help":
        from .help_cmd import run_help
        run_help()
    else:
        seq = config.get("logo_seq", 0)
        config["logo_seq"] = seq + 1
        save_config(config)
        weekly_moods = get_weekly_mood_by_day()
        show_home(config, get_stats(config), weekly_moods, logo_seq=seq)
