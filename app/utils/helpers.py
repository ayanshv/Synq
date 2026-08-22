"""Small shared helpers.

Keeping utilities here avoids duplicating small bits of logic across
services and UI modules.
"""

import os
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo


def now_utc() -> datetime:
    """Return the current UTC time as a timezone-aware datetime."""
    return datetime.now(timezone.utc)


def local_today() -> date:
    """Return today's date in the app user's configured local timezone."""
    timezone_name = os.getenv("APP_TIMEZONE", "America/Los_Angeles")
    return datetime.now(ZoneInfo(timezone_name)).date()


def format_datetime(value: datetime) -> str:
    """Format a datetime for display (e.g. "2026-08-21 14:30")."""
    if value is None:
        return ""
    return value.strftime("%Y-%m-%d %H:%M")
