"""Small shared helpers.

Keeping utilities here avoids duplicating small bits of logic across
services and UI modules.
"""

from datetime import datetime, timezone


def now_utc() -> datetime:
    """Return the current UTC time as a timezone-aware datetime."""
    return datetime.now(timezone.utc)


def format_datetime(value: datetime) -> str:
    """Format a datetime for display (e.g. "2026-08-21 14:30")."""
    if value is None:
        return ""
    return value.strftime("%Y-%m-%d %H:%M")
