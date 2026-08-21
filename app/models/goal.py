"""Goal model.

A Goal is something a team is working toward (for example "ship v1 by Q4").
Each goal has a target value and a current value so progress can be measured
concretely rather than as an arbitrary percentage. The meeting service reads
goal status to help decide whether a meeting is warranted.
"""

import datetime

from sqlmodel import Field, SQLModel


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class Goal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="team.id")

    title: str
    description: str = ""

    target_value: float = Field(default=100.0)
    current_value: float = Field(default=0.0)

    # "on_track", "at_risk", or "off_track" - plain string for MVP simplicity.
    status: str = Field(default="on_track")

    created_at: datetime.datetime = Field(default_factory=_now)
