# feels

A local-first CLI mood tracker for developers. Log how you're feeling, track focus and stress, organize by project, all from your terminal.

**All data stays on your machine.** No cloud. No accounts. No tracking.

## Installation

```bash
# From PyPI (when published)
pip install feels

# From source
git clone https://github.com/gabrielpereira/feels.git
cd feels
pip install -e .
```

## Quick Start

```bash
# First run — interactive setup
feels

# Log an entry (interactive prompts)
feels add

# View logs (last 7 days by default)
feels logs

# View all logs
feels logs --all

# See all commands
feels help
```

## Commands

### Logging
- **`feels add`** — Log a new entry with mood (0–5), optional focus/stress scores, tags, and a note
- **`feels logs`** — View logs grouped by day
  - `--all` — Show all logs ever
  - `--oldest` — Reverse sort (oldest first)
  - `--from YYYY-MM-DD` — Start date
  - `--to YYYY-MM-DD` — End date
  - `--project <name>` — Filter by project
- **`feels edit <id>`** — Edit an existing log entry
- **`feels delete <id>`** — Delete a log entry (with confirmation)

### Organization
- **`feels config`** — Update settings (enable/disable focus, stress, projects)
- **`feels project add <name>`** — Add a project
- **`feels project list`** — Show all projects
- **`feels project delete <name>`** — Remove a project

### Insights
- **`feels stats`** — View statistics
  - Overall: total logs, average mood, best/worst mood
  - Optional: focus and stress averages (if enabled)
  - Last 7 days: logs this week and weekly average
- **`feels export`** — Export logs
  - `--format json` — JSON format (full details)
  - `--format csv` — CSV format (spreadsheet-friendly)

### Help
- **`feels help`** — Show all available commands
- **`feels`** — Show home screen with quick stats and command list

## Features

✅ **Log mood entries** with optional focus and stress scores (0–5)
✅ **Add tags and notes** to logs for context
✅ **Organize by project** (optional) to keep work separated
✅ **View logs grouped by day** with flexible filtering
✅ **Edit & delete** entries anytime
✅ **Home dashboard** showing total logs, current streak, last 7-days average
✅ **Statistics** — overall and weekly mood/focus/stress analysis
✅ **Export data** as JSON (full) or CSV (spreadsheet)
✅ **Local storage only** — everything at `~/.feels/`, completely private
✅ **Comprehensive tests** — 23 tests covering core functionality
✅ **Robust error handling** — validates input and reports clear errors

## Configuration

Settings are interactive. On first run, choose your defaults:
- **Mood score** — always enabled
- **Focus score** — optional
- **Stress score** — optional
- **Projects** — optional (organize logs by project)
- **Tags** — always enabled
- **Notes** — always enabled

Run `feels config` anytime to revisit and change these settings.

## Data Storage

All your data lives locally:
- `~/.feels/config.json` — your configuration
- `~/.feels/data.db` — your log entries (SQLite database)

**No internet required.** No servers. No tracking. No data leaves your machine.

## Examples

### Log your first entry
```bash
$ feels add
  Project: work
  Mood (0–5): 4
  Focus (0–5): 3
  Stress (0–5): 2
  Tags: #meetings #productive
  Note: Good progress on the project

✓ Logged 4/5 mood #1
```

### View logs from the last week
```bash
$ feels logs
──────────────────── March 25, 2026 ────────────────────
#1  ·  14:30  ·  work
4/5  3/5 focus  2/5 stress  #meetings  #productive
Good progress on the project
```

### View statistics
```bash
$ feels stats

Overall
   total logs          42
   avg mood            3.8/5
   best               5/5
   worst              1/5

Focus
   avg                3.5/5
   best               5/5
   worst              1/5

Last 7 days
   logs this week     12
   avg mood           4.1/5
```

### Export your logs
```bash
$ feels export --format json
✓ Exported 42 logs to feels_20260325_170013.json

$ feels export --format csv
✓ Exported 42 logs to feels_20260325_170014.csv
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install -e ".[test]"

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/feels --cov-report=html
```

Current test coverage:
- **100%** config module
- **84%** database module
- **85%** utils module
- **21%** overall

### Project Structure

```
feels/
├── src/feels/
│   ├── cli.py           # CLI entry point and argument routing
│   ├── config.py        # Configuration management
│   ├── database.py      # SQLite database operations
│   ├── utils.py         # Shared utilities (colors, formatting)
│   ├── validation.py    # Input validation
│   ├── add.py           # Log entry command
│   ├── logs.py          # View logs command
│   ├── edit.py          # Edit log command
│   ├── delete.py        # Delete log command
│   ├── config_cmd.py    # Settings command
│   ├── project_cmd.py   # Project management command
│   ├── stats_cmd.py     # Statistics command
│   ├── export_cmd.py    # Export command
│   ├── help_cmd.py      # Help command
│   ├── home.py          # Home screen display
│   └── onboarding.py    # First-run setup
├── tests/               # Test suite
├── pyproject.toml       # Package configuration
└── README.md            # This file
```

## Roadmap

- [ ] Theme customization (light/dark, custom colors)
- [ ] Mood trends over time
- [ ] Daily/weekly/monthly summaries
- [ ] Best/worst times of day analysis
- [ ] Export to other formats (PDF, Excel)
- [ ] Data import from CSV
- [ ] Cloud sync option (optional, default local)
- [ ] Plugin system for custom commands

## License

MIT License — see LICENSE file for details.

## Contributing

Contributions welcome! Feel free to open issues or submit PRs.
