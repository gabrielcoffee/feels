# feels

[![PyPI](https://img.shields.io/pypi/v/feels)](https://pypi.org/project/feels/)
[![Python](https://img.shields.io/pypi/pyversions/feels)](https://pypi.org/project/feels/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A mood tracker for developers. Runs entirely in your terminal.

**All data stays on your machine.** No cloud. No accounts. No tracking.

![feels demo: logging an entry, the home screen, logs, graph and calendar](https://raw.githubusercontent.com/gabrielcoffee/feels/main/.github/assets/demo.gif)

## Why

Most mood trackers are phone apps that want an account and your data. `feels` lives where developers already spend the day, the terminal. Logging takes ten seconds, a daily reminder opens it for you, and the graphs make a bad stretch obvious before it becomes a bad month.

## Highlights

- **Ten-second logging.** Mood, optional focus and stress scores, an ASCII emoji and a note.
- **Graphs and a calendar in the terminal**, colored by score, built with [Rich](https://github.com/Textualize/rich).
- **Streaks and a weekly mood chart** on the home screen.
- **Daily reminders** that open your terminal at a set time. It detects Ghostty, iTerm2 and Terminal.app.
- **Local-first.** One SQLite file and one JSON config in `~/.feels`. Export to JSON or CSV any time.
- **Published on PyPI**, with releases built and uploaded by GitHub Actions on every push to `main`.

## Install

```bash
pip install feels
```

First run walks you through a quick setup. Then just type `feels`.

You can also use `fls` as a shorter alias — same thing.

## Commands

### Logging

```bash
feels log                        # log how you're feeling
feels log --yesterday            # log for yesterday
feels log --date DD-MM-YYYY      # log for a specific date
```

### Viewing logs

```bash
feels logs                       # last 7 days
feels logs --all                 # everything
feels logs --oldest              # oldest first
feels logs --from DD-MM-YYYY     # from a date
feels logs --to DD-MM-YYYY       # up to a date
feels logs --project <name>      # filter by project
```

### Visualizing

```bash
feels graph                      # monthly bar chart
feels graph --from MM            # specific month this year
feels graph --from MM-YYYY       # specific month and year

feels calendar                   # monthly calendar view
feels calendar --from MM-YYYY    # navigate to any month
```

### Editing

```bash
feels edit <id>                  # edit an entry
feels delete <id>                # delete one or more entries
```

### Projects

```bash
feels project add <name>         # add a project
feels project list               # list all projects
feels project delete <name>      # remove a project
```

### Data

```bash
feels stats                      # view statistics
feels export --format json       # export as JSON
feels export --format csv        # export as CSV
feels reset                      # delete all data
```

### Reminder

```bash
feels reminder                   # show reminder status
feels reminder set HH:MM         # set a daily reminder
feels reminder unset             # remove the reminder
```

The reminder opens your terminal running `feels` at the set time. Detects Ghostty, iTerm2, and Terminal.app automatically.

### Other

```bash
feels config                     # update settings
feels help                       # all commands
feels                            # home screen
```

## Configuration

On first run you choose your setup. Defaults are **mood + asciimoji + note**. You can optionally enable:

- **Focus score** — 0–5, how locked in you were
- **Stress score** — 0–5, lower is better
- **Projects** — separate logs by what you're working on

Run `feels config` anytime to change these.

## Data

Everything lives at `~/.feels/`:

- `config.json` — your settings
- `data.db` — your entries (SQLite)

No internet required. Nothing leaves your machine.

## Project structure

```
src/feels/
├── cli.py           # routing
├── config.py        # config management
├── database.py      # SQLite operations
├── utils.py         # colors, formatting, prompts
├── home.py          # home screen
├── add.py           # feels log
├── logs.py          # feels logs
├── edit.py          # feels edit
├── delete.py        # feels delete
├── graph_cmd.py     # feels graph
├── calendar_cmd.py  # feels calendar
├── stats_cmd.py     # feels stats
├── export_cmd.py    # feels export
├── reminder_cmd.py  # feels reminder
├── project_cmd.py   # feels project
├── config_cmd.py    # feels config
├── onboarding.py    # first-run setup
└── help_cmd.py      # feels help
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

The demo GIF is recorded with [VHS](https://github.com/charmbracelet/vhs): `vhs trailer.tape`.

## License

MIT
