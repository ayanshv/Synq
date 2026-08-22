"""User model.

A User is a single person who belongs to a Team. The MVP stores a name,
email, role, and the onboarding answers used to personalize the workspace.
"""

import datetime

from sqlmodel import Field, SQLModel


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team_id: int | None = Field(default=None, foreign_key="team.id")
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    # "member" or "lead" - kept as a plain string for MVP simplicity.
    role: str = Field(default="member")
    # What the person works on, captured during onboarding.
    work_focus: str = Field(default="")
    # JSON array of tool ids the person said they use, e.g. ["github","gmail"].
    tools_json: str = Field(default="[]")
    # JSON object for sharing / AI-analysis preferences.
    settings_json: str = Field(default="{}")
    created_at: datetime.datetime = Field(default_factory=_now)
