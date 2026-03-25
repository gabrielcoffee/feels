# Changes

## Bug fixes — live home stats + entry format

- **Home screen was static** — added `get_stats()` to `database.py` that computes total log count, current streak (consecutive days going back from today), last-7-days score averages, and whether the user has logged today. `show_home()` now takes `config` and `stats` and renders real data.
- **Entry format simplified** — removed the date from each log line in `format_entry`. The day header rule already shows the date, so each entry now shows only `#id · time · project`. Less redundancy, cleaner look.
- **Nudge logic** — home screen shows "run feels add to log your first entry" when total is 0, or "haven't logged today yet" when there are logs but none today.

---

## Commands — add, logs, edit, delete

### What was built
- `src/feels/database.py` — extended with `insert_log`, `get_log`, `get_logs`, `update_log`, `delete_log`
- `src/feels/utils.py` — shared helpers: `score_color`, `prompt_score`, `format_entry`
- `src/feels/add.py` — interactive log entry prompt
- `src/feels/logs.py` — displays entries grouped by day with day-rule separators
- `src/feels/edit.py` — re-prompts each field with current value as default
- `src/feels/delete.py` — shows entry, asks confirmation, then deletes
- `src/feels/cli.py` — argparse routing for all subcommands

### Why these choices

**`argparse` subparsers** — handles `feels logs --all --from ... --project ...` flags cleanly without rolling a custom parser.

**`utils.py` as shared module** — `format_entry` and `score_color` are used by `logs`, `edit`, and `delete`. Keeping them in one place avoids duplication.

**Score colors** — red→orange→yellow→green gradient (indices 0–5) applied via Rich color names. Used on every score display so visual feedback is consistent everywhere.

**`get_logs` default 7-day filter** — only suppressed when `--all` is passed or an explicit `--from` date is given, matching the spec exactly.

**Edit uses defaults** — Rich's `Prompt.ask(default=...)` pre-fills the current value so the user just hits Enter to keep it. No re-entry needed for unchanged fields.

**`last_project` stored in config** — when projects are enabled, the last used project is persisted to `config.json` so `feels add` can pre-fill it on the next run.

### How it connects

All commands flow through `cli.py → argparse → command module`. Every command module imports from `database.py` for persistence and `utils.py` for display. The config dict is passed into each command so they know which optional fields (focus, stress, project) are active.

---

## UI polish — home screen borders + green "feels"

- **Home screen** now renders inside a `Panel` with `bright_black` border, matching the welcome panel style
- **"feels"** is always `bold green` in both the welcome message and the home screen — removed the random rainbow
- Added **"commands:"** label above the command list so it's clear what those rows are
- Added **`feels help`** to the command list
- Used Rich's `Group` to stack title, stats, and the commands table inside a single Panel renderable

---

## Rename: mood → feels

**Why:** `feels` is a unique name not found on PyPI. Better than alternatives (`flow`, `peak`, etc.) that are already taken.

**What changed:**
- Renamed package from `mood` to `feels`
- Updated `pyproject.toml`: `name = "feels"`, entry point `feels = "feels.cli:main"`
- Renamed directory: `src/mood/` → `src/feels/`
- Updated CLI output to reflect new name

---

## Step 1 — Project Skeleton

### What was built
- `pyproject.toml` — package metadata, dependencies, and CLI entry point
- `src/feels/__init__.py` — marks the directory as a Python package
- `src/feels/cli.py` — contains `main()`, the single entry point for the `feels` command

### Why these choices

**`src/` layout** — keeps the package source separate from project root files like `pyproject.toml` and config. This prevents accidental imports from the working directory and is the recommended structure for modern Python packages.

**`pyproject.toml` over `setup.py`** — `pyproject.toml` is the current standard (PEP 621). No need for a legacy `setup.py`.

**`setuptools` as build backend** — widely supported and works with both `pip install -e .` (for development) and `pipx install .` (for end users).

**`rich` as the only dependency** — declared now since the spec calls for it. Not used yet, but it's ready for Step 2.

**Entry point `feels = "feels.cli:main"`** — this tells Python's packaging system to create a `feels` shell command that calls the `main()` function in `src/feels/cli.py`. This is how CLI tools are distributed as Python packages.

### How it connects

`cli.py:main` is the front door. Every future command (`feels add`, `feels logs`, etc.) will be routed from this function. Right now it just prints a confirmation string — the routing and real logic come in later steps.

---

## Step 2 — Onboarding + Config

### What was built
- `src/feels/config.py` — reads and writes `~/.feels/config.json`
- `src/feels/onboarding.py` — the interactive first-run setup flow
- `src/feels/cli.py` — updated to detect first run and route accordingly

### Why these choices

**`~/.feels/` directory** — storing data in the user's home directory is the Unix convention for per-user app data. It survives reinstalls and is independent of where the package is installed.

**`config.json` over other formats** — simple, readable, no extra dependencies. The config is small (just a few booleans) so there's no need for anything heavier.

**Default config path (`y`)** — the spec calls for defaulting to the simplest setup (mood + tags + note only). New users shouldn't be overwhelmed. They can revisit via `feels config` later.

**Rich `Confirm.ask`** — handles the `y/n` prompt rendering, input parsing, and default value display automatically. No need to roll our own input loop.

**Summary table before saving** — lets the user see exactly what they chose before anything is written to disk. Reduces surprise.

### How it connects

`config.py` is the single source of truth for user settings. Every future module (`mood add`, `mood logs`, the database setup) will import `load_config()` to know which fields are enabled. The onboarding runs exactly once — after that, `cli.py` routes straight to the home screen.

### How it connects

`config.py` is the single source of truth for user settings. Every future module (`feels add`, `feels logs`) will import `load_config()` to know which fields are enabled.

---

## Step 3 — Database Setup

### What was built
- `src/feels/database.py` — creates and manages `~/.feels/data.db`
- `src/feels/home.py` — the home screen (static placeholder for now)
- `src/feels/cli.py` — updated to init the DB on first post-onboarding run, then show home

### Why these choices

**SQLite** — zero setup, no server, single file. Perfect for a local-first tool. The DB lives at `~/.feels/data.db` alongside the config.

**Schema derived from config** — only the columns the user enabled are created. If focus/stress/projects are off, those columns simply don't exist. This keeps the schema honest and avoids storing data that was never meant to be collected.

**`tags` and `note` always included** — they're always-on fields per the spec, so they're always in the schema regardless of config.

**DB init happens on first run after onboarding** — not during onboarding itself. This separates concerns: onboarding is about choosing settings, the first home screen visit is when the app becomes "ready to use."

### How it connects

`database.py` reads `config` to decide the schema — it's downstream of `config.py`. `cli.py` now follows a clean three-state flow: no config → onboarding; config but no DB → init DB then home; everything ready → home. Future commands (`feels add`, `feels logs`) will connect to the same DB file.

### Progress

- [x] Step 1 — Project skeleton
- [x] Step 2 — Onboarding flow + config
- [x] Step 3 — Database setup
