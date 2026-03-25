# feels

A local-first CLI mood tracker for developers. Log how you're feeling, track focus and stress, organize by project, all from your terminal.

## Installation

```bash
pip install feels
```

## Quick Start

```bash
# First run — choose your settings
feels

# Log an entry
feels add

# View your logs
feels logs

# See other commands
feels help
```

## Features

- **Log entries** — mood (0–5), optional focus and stress scores, tags, and notes
- **Organize by project** — separate logs by project if enabled
- **View logs** — grouped by day with filtering options (`--all`, `--oldest`, `--project`, `--from`, `--to`)
- **Edit & delete** — update or remove entries
- **Home dashboard** — see your total logs, current streak, and last 7 days averages
- **Local data** — everything stored at `~/.feels/` — no cloud, no accounts

## Configuration

Run `feels config` to revisit your settings anytime.

## Future Updates & Features

- `feels config` — revisit and update settings (enable/disable focus, stress, projects, colors)
- `feels project` — manage projects (add, list, delete)
- `feels help` — detailed help for all commands
- Statistics — weekly/monthly summaries, mood trends, best/worst times of day
- Themes — light/dark mode, custom colors
- Export — save logs as JSON or CSV

## Data

All data is stored locally:
- `~/.feels/config.json` — your settings
- `~/.feels/data.db` — your log entries (SQLite)

No internet required. No tracking. Just you and your mood data.
