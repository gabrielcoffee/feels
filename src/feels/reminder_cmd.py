import importlib.resources
import plistlib
import re
import subprocess
from pathlib import Path

from rich.console import Console

from .config import save_config

console = Console()

_LAUNCH_AGENTS = Path.home() / "Library" / "LaunchAgents"
_PLIST = _LAUNCH_AGENTS / "com.feels.reminder.plist"
_REMIND_SCRIPT = Path.home() / ".feels" / "remind.sh"
_OPEN_SCRIPT = Path.home() / ".feels" / "open_feels.sh"
_LABEL = "com.feels.reminder"

_MESSAGES = [
    "Hey, how's it going? Time to log your mood.",
    "Take a moment — log how you're feeling.",
    "Your daily mood check-in is waiting.",
    "It's feels time. How are you doing today?",
    "Quick mood check — what's your score today?",
    "Don't forget to log your day in feels!",
    "How's your energy? Log it in feels.",
    "A few seconds to reflect — log your mood.",
    "Check in with yourself. How are you doing?",
    "Mood log time. How's the vibe today?",
    "Time to track your feels. How are you really doing?",
    "Just a moment to check in — log your mood now.",
    "Your past self will thank you. Log your mood.",
    "Pause, reflect, log. feels is waiting.",
    "How are you feeling right now? Take note of it.",
]

# Common install paths for terminal-notifier and Homebrew (Intel + Apple Silicon)
_NOTIFIER_PATHS = [
    "/opt/homebrew/bin/terminal-notifier",
    "/usr/local/bin/terminal-notifier",
]
_BREW_PATHS = [
    "/opt/homebrew/bin/brew",
    "/usr/local/bin/brew",
]


def _find_notifier() -> str:
    """Return path to terminal-notifier binary: system install first, then bundled."""
    for p in _NOTIFIER_PATHS:
        if Path(p).is_file():
            return p
    # Fall back to the binary bundled inside the feels package
    bundled = _bundled_notifier()
    if bundled:
        return bundled
    return ""


def _bundled_notifier() -> str:
    """Return path to the terminal-notifier binary bundled with feels, or empty string."""
    try:
        pkg_dir = Path(__file__).parent
        binary = pkg_dir / "bin" / "terminal-notifier.app" / "Contents" / "MacOS" / "terminal-notifier"
        if binary.exists():
            # Strip Gatekeeper quarantine on first encounter so macOS doesn't block it
            subprocess.run(["xattr", "-rd", "com.apple.quarantine", str(binary.parent.parent.parent)],
                           capture_output=True)
            binary.chmod(0o755)
            return str(binary)
    except Exception:
        pass
    return ""


def _find_brew() -> str:
    for p in _BREW_PATHS:
        if Path(p).is_file():
            return p
    return ""


def _write_scripts() -> None:
    """Write ~/.feels/open_feels.sh (terminal detection) and ~/.feels/remind.sh (notification)."""
    _OPEN_SCRIPT.parent.mkdir(parents=True, exist_ok=True)

    # open_feels.sh — detects and opens feels in the user's preferred terminal
    open_script = """\
#!/bin/bash
if [ -d "/Applications/Ghostty.app" ] || [ -d "$HOME/Applications/Ghostty.app" ]; then
    GHOSTTY_BIN=""
    for p in /opt/homebrew/bin/ghostty /usr/local/bin/ghostty "$HOME/.local/bin/ghostty"; do
        [ -x "$p" ] && GHOSTTY_BIN="$p" && break
    done
    if [ -n "$GHOSTTY_BIN" ]; then
        "$GHOSTTY_BIN" --command=feels &
    else
        open -a "Ghostty"
    fi
elif [ -d "/Applications/iTerm.app" ] || [ -d "$HOME/Applications/iTerm.app" ]; then
    /usr/bin/osascript <<'APPLESCRIPT'
tell application "iTerm"
    activate
    create window with default profile command "feels"
end tell
APPLESCRIPT
else
    /usr/bin/osascript -e 'tell application "Terminal" to do script "feels"' \\
                       -e 'tell application "Terminal" to activate'
fi
"""
    _OPEN_SCRIPT.write_text(open_script)
    _OPEN_SCRIPT.chmod(0o755)

    # remind.sh — picks a random message and fires the notification
    msgs_lines = "\n".join(f'  "{m}"' for m in _MESSAGES)
    open_path = str(_OPEN_SCRIPT)

    # Build the full list of notifier paths to check: system installs + bundled fallback
    notifier_search_paths = list(_NOTIFIER_PATHS)
    bundled = _bundled_notifier()
    if bundled:
        notifier_search_paths.append(bundled)

    remind_script = f"""\
#!/bin/bash
msgs=(
{msgs_lines}
)
msg="${{msgs[$RANDOM % ${{#msgs[@]}}]}}"

# Prefer terminal-notifier (click opens feels); fall back to display notification + auto-open
NOTIFIER=""
for p in {" ".join(notifier_search_paths)}; do
    [ -x "$p" ] && NOTIFIER="$p" && break
done

if [ -n "$NOTIFIER" ]; then
    "$NOTIFIER" -message "$msg" -title "feels" -execute "/bin/bash \\"{open_path}\\""
else
    /usr/bin/osascript -e "display notification \\"$msg\\" with title \\"feels\\""
    /bin/bash "{open_path}"
fi
"""
    _REMIND_SCRIPT.write_text(remind_script)
    _REMIND_SCRIPT.chmod(0o755)


def run_reminder(config: dict, args) -> None:
    action = getattr(args, "action", None)
    if action == "set":
        _set(config, args.time)
    elif action == "unset":
        _unset(config)
    else:
        _status(config)


def _set(config: dict, time_str: str) -> None:
    if not re.match(r"^\d{1,2}:\d{2}$", time_str):
        console.print("\n[red]Error:[/red] Use HH:MM format (e.g. 09:00)\n")
        return

    hour, minute = map(int, time_str.split(":"))
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        console.print("\n[red]Error:[/red] Invalid time — hour 0–23, minute 0–59.\n")
        return

    _write_scripts()

    plist = {
        "Label": _LABEL,
        "ProgramArguments": ["/bin/bash", str(_REMIND_SCRIPT)],
        "StartCalendarInterval": {"Hour": hour, "Minute": minute},
        "StandardOutPath": "/dev/null",
        "StandardErrorPath": "/dev/null",
    }

    _LAUNCH_AGENTS.mkdir(parents=True, exist_ok=True)

    if _PLIST.exists():
        subprocess.run(["launchctl", "unload", str(_PLIST)], capture_output=True)

    with open(_PLIST, "wb") as f:
        plistlib.dump(plist, f)

    result = subprocess.run(["launchctl", "load", str(_PLIST)], capture_output=True)

    console.print()
    if result.returncode == 0:
        config["reminder_time"] = f"{hour:02d}:{minute:02d}"
        save_config(config)
        console.print(f"[green]✓[/green] Reminder set for [bold]{hour:02d}:{minute:02d}[/bold] every day.")
    else:
        console.print(f"[red]Error:[/red] Could not load reminder. {result.stderr.decode().strip()}")
    console.print()


def _unset(config: dict) -> None:
    console.print()
    if not _PLIST.exists():
        console.print("[dim]No reminder is set.[/dim]")
        console.print()
        return

    subprocess.run(["launchctl", "unload", str(_PLIST)], capture_output=True)
    _PLIST.unlink()
    for f in (_REMIND_SCRIPT, _OPEN_SCRIPT):
        if f.exists():
            f.unlink()
    config.pop("reminder_time", None)
    save_config(config)
    console.print("[green]✓[/green] Reminder removed.")
    console.print()


def _status(config: dict) -> None:
    console.print()
    time = config.get("reminder_time")
    if time and _PLIST.exists():
        console.print(f"  Reminder set for [bold]{time}[/bold] every day.")
        console.print()
        console.print("  [bold]feels reminder set HH:MM[/bold]    update the time")
        console.print("  [bold]feels reminder unset[/bold]        remove the reminder")
    else:
        console.print("  [dim]No reminder set.[/dim]")
        console.print()
        console.print("  [bold]feels reminder set HH:MM[/bold]    set a daily reminder")
        console.print("  [bold]feels reminder unset[/bold]        remove the reminder")
    console.print()
