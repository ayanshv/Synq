"""Local browser session.

Authentication is intentionally lightweight for the MVP: onboarding stores
the current user id in NiceGUI browser storage, and pages resolve that id
against SQLite. This is not a production auth system.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from sqlmodel import select

from app.database import get_session
from app.models import Team, User


@dataclass(frozen=True)
class LocalSession:
    """The signed-in user's workspace context."""

    user_id: int
    team_id: int
    user_name: str
    team_name: str
    user_email: str = ""
    role: str = "member"
    work_focus: str = ""
    tools: tuple[str, ...] = field(default_factory=tuple)
    invite_code: str = ""
    settings: dict = field(default_factory=dict)


def get_stored_user_id() -> int | None:
    """Read the current user id from browser storage, if any."""
    try:
        from nicegui import app

        raw = app.storage.user.get("user_id")
    except RuntimeError:
        return None
    if raw is None:
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def set_current_user_id(user_id: int) -> None:
    """Remember the signed-in user in this browser."""
    from nicegui import app

    app.storage.user["user_id"] = user_id


def clear_current_user() -> None:
    """Sign out of this browser without deleting workspace data."""
    from nicegui import app

    app.storage.user.clear()


def get_local_session_or_none() -> LocalSession | None:
    """Return the current workspace session, or None if nobody is signed in."""
    user_id = get_stored_user_id()
    if user_id is None:
        return None
    with get_session() as session:
        user = session.get(User, user_id)
        if user is None or user.id is None or user.team_id is None:
            return None
        team = session.get(Team, user.team_id)
        if team is None or team.id is None:
            return None
        return LocalSession(
            user_id=user.id,
            team_id=team.id,
            user_name=user.name,
            team_name=team.name,
            user_email=user.email,
            role=user.role,
            work_focus=user.work_focus or "",
            tools=tuple(_parse_tools(user.tools_json)),
            invite_code=team.invite_code or "",
            settings=_parse_settings(user.settings_json),
        )


def get_local_session() -> LocalSession:
    """Resolve the current user and team, or raise if the browser is unsigned."""
    local = get_local_session_or_none()
    if local is None:
        raise RuntimeError("No signed-in workspace user. Complete onboarding first.")
    return local


def _parse_tools(raw: str) -> list[str]:
    try:
        data = json.loads(raw or "[]")
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return [str(item) for item in data if str(item).strip()]


def _parse_settings(raw: str) -> dict:
    try:
        data = json.loads(raw or "{}")
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}
