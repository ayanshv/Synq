"""Team model.

A Team groups users together. Updates, goals, and meeting recommendations
are scoped to a team so the dashboard can show "what my team worked on"
without cross-team leakage.
"""

import datetime
import secrets

from sqlmodel import Field, SQLModel


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def new_invite_code() -> str:
    """Return a short, URL-safe code teammates can use to join."""
    return secrets.token_urlsafe(8)


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    invite_code: str = Field(default_factory=new_invite_code, index=True)
    created_at: datetime.datetime = Field(default_factory=_now)
