"""Smoke test for the helpers module.

Runs with `python -m pytest tests/test_helpers.py` once pytest is installed.
Kept dependency-free so it can also run as a plain script.
"""

from app.utils.helpers import format_datetime, now_utc


def test_now_utc_is_timezone_aware():
    assert now_utc().tzinfo is not None


def test_format_datetime_handles_none():
    assert format_datetime(None) == ""
