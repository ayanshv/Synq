"""Create and join real workspaces from onboarding answers."""

from __future__ import annotations

import json

from sqlmodel import select

from app.config import settings
from app.database import get_session
from app.models import Team, User
from app.models.team import new_invite_code
from app.services.session_service import LocalSession, set_current_user_id

# Tools the wizard can offer. "manual" is always available for typed notes.
KNOWN_TOOLS = (
    ("github", "GitHub", "Pull requests, commits, and code reviews"),
    ("gmail", "Gmail", "Project-related email"),
    ("linear", "Linear", "Issues and cycle work"),
    ("slack", "Slack", "Decisions and follow-ups from chat"),
    ("calendar", "Calendar", "Meetings you want to remember"),
    ("docs", "Docs", "Specs, notes, and writing"),
    ("manual", "Personal notes", "Anything you log yourself"),
)

DEFAULT_SETTINGS = {
    "include_activity_in_ai": True,
    "include_blockers": True,
    "excluded_types": [],
}


class WorkspaceError(Exception):
    """User-safe workspace setup failure."""


def invite_url(code: str) -> str:
    """Absolute link teammates can use to join this workspace."""
    return f"{settings.app_base_url}/join/{code}"


def create_workspace(
    name: str,
    email: str,
    team_name: str,
    work_focus: str,
    tools: list[str],
) -> LocalSession:
    """Create a team and its first member (the person running the wizard)."""
    name = name.strip()
    email = email.strip().lower()
    team_name = team_name.strip()
    work_focus = work_focus.strip()
    tools = _normalize_tools(tools)
    if not name or not email or not team_name:
        raise WorkspaceError("Name, email, and team name are required.")

    with get_session() as session:
        existing = session.exec(select(User).where(User.email == email)).first()
        if existing is not None:
            raise WorkspaceError(
                "That email is already in a workspace. Sign in from the same "
                "browser or join with a different email."
            )
        team = Team(name=team_name, invite_code=new_invite_code())
        session.add(team)
        session.flush()
        user = User(
            team_id=team.id,
            name=name,
            email=email,
            role="lead",
            work_focus=work_focus,
            tools_json=json.dumps(tools),
            settings_json=json.dumps(DEFAULT_SETTINGS),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        session.refresh(team)
        user_id = user.id
        team_id = team.id
        invite_code = team.invite_code

    set_current_user_id(user_id)
    return LocalSession(
        user_id=user_id,
        team_id=team_id,
        user_name=name,
        team_name=team_name,
        user_email=email,
        role="lead",
        work_focus=work_focus,
        tools=tuple(tools),
        invite_code=invite_code,
        settings=dict(DEFAULT_SETTINGS),
    )


def join_workspace(code: str, name: str, email: str, work_focus: str, tools: list[str]) -> LocalSession:
    """Add a teammate to an existing workspace from an invite link."""
    name = name.strip()
    email = email.strip().lower()
    work_focus = work_focus.strip()
    tools = _normalize_tools(tools)
    code = (code or "").strip()
    if not name or not email or not code:
        raise WorkspaceError("Name, email, and a valid invite link are required.")

    with get_session() as session:
        team = session.exec(select(Team).where(Team.invite_code == code)).first()
        if team is None or team.id is None:
            raise WorkspaceError("That invite link is not valid.")
        existing = session.exec(select(User).where(User.email == email)).first()
        if existing is not None:
            if existing.team_id == team.id and existing.id is not None:
                set_current_user_id(existing.id)
                from app.services.session_service import get_local_session

                return get_local_session()
            raise WorkspaceError("That email already belongs to another workspace.")
        user = User(
            team_id=team.id,
            name=name,
            email=email,
            role="member",
            work_focus=work_focus,
            tools_json=json.dumps(tools),
            settings_json=json.dumps(DEFAULT_SETTINGS),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        user_id = user.id
        team_name = team.name
        invite_code = team.invite_code
        team_id = team.id

    set_current_user_id(user_id)
    return LocalSession(
        user_id=user_id,
        team_id=team_id,
        user_name=name,
        team_name=team_name,
        user_email=email,
        role="member",
        work_focus=work_focus,
        tools=tuple(tools),
        invite_code=invite_code,
        settings=dict(DEFAULT_SETTINGS),
    )


def get_team_by_invite(code: str) -> Team | None:
    with get_session() as session:
        return session.exec(select(Team).where(Team.invite_code == code)).first()


def update_user_tools(user_id: int, tools: list[str]) -> None:
    tools = _normalize_tools(tools)
    with get_session() as session:
        user = session.get(User, user_id)
        if user is None:
            return
        user.tools_json = json.dumps(tools)
        session.add(user)
        session.commit()


def update_user_settings(user_id: int, settings_patch: dict) -> None:
    with get_session() as session:
        user = session.get(User, user_id)
        if user is None:
            return
        try:
            current = json.loads(user.settings_json or "{}")
        except json.JSONDecodeError:
            current = {}
        if not isinstance(current, dict):
            current = {}
        current.update(settings_patch)
        user.settings_json = json.dumps(current)
        session.add(user)
        session.commit()


def _normalize_tools(tools: list[str]) -> list[str]:
    known = {key for key, _title, _detail in KNOWN_TOOLS}
    cleaned = []
    for tool in tools:
        key = str(tool).strip().lower()
        if key in known and key not in cleaned:
            cleaned.append(key)
    if "manual" not in cleaned:
        cleaned.append("manual")
    return cleaned
