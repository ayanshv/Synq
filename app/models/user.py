"""User model.

A User is a single person who belongs to a Team. In the MVP, users are
created without authentication; the model stores a name, email, and role so
published updates can be attributed to a person and permissions can vary
later.
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
    created_at: datetime.datetime = Field(default_factory=_now)
