# feels

A mood tracker for developers. Runs entirely in your terminal.

**All data stays on your machine.** No cloud. No accounts. No tracking.

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

## License

MIT
