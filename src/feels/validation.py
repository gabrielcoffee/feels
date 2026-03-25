"""Input validation utilities for feels CLI."""

from datetime import datetime
from rich.console import Console

console = Console()


def validate_date(date_str: str) -> bool:
    """Validate date string in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_score(score: int) -> bool:
    """Validate mood/focus/stress score is between 0-5."""
    return isinstance(score, int) and 0 <= score <= 5


def validate_project_name(name: str) -> bool:
    """Validate project name is not empty."""
    return isinstance(name, str) and len(name.strip()) > 0


def handle_invalid_date(date_str: str, flag_name: str) -> None:
    """Print error message for invalid date."""
    console.print(
        f"[red]Error:[/red] Invalid date format for {flag_name}: '{date_str}'. "
        "Use YYYY-MM-DD format (e.g., 2026-03-25)"
    )


def handle_database_error(error: Exception, operation: str) -> None:
    """Print error message for database operations."""
    console.print(
        f"[red]Error:[/red] Failed to {operation}. {str(error)}"
    )


def handle_file_error(error: Exception, operation: str) -> None:
    """Print error message for file operations."""
    console.print(
        f"[red]Error:[/red] Failed to {operation}. {str(error)}"
    )
