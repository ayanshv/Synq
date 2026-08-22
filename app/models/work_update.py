"""WorkUpdate model.

A WorkUpdate is the core object in Synq. It is created when a user clicks
"Finish Work", holds the AI-drafted summary, and is published to the team
once the user confirms.

The `published` boolean is the single gate that controls team visibility:
False = private draft, True = visible to the team. Keeping it as a boolean
(rather than a status string) makes the visibility rule obvious.
"""

import datetime

from sqlmodel import Field, SQLModel

from app.utils.helpers import local_today


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class WorkUpdate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    team_id: int = Field(foreign_key="team.id")

    # The work day this update describes (not the moment it was created).
    # Using `datetime.date` so the type is unambiguous from the field name.
    date: datetime.date = Field(default_factory=local_today)

    title: str = ""
    # The AI-drafted summary the user reviews and edits.
    summary: str = ""
    accomplishments: str = ""
    blockers: str = ""

    # False = private draft, True = visible to the team.
    published: bool = Field(default=False, index=True)

    created_at: datetime.datetime = Field(default_factory=_now)
