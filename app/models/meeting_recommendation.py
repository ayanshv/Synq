"""MeetingRecommendation model.

A MeetingRecommendation is the output of the meeting service: a per-team,
per-day nudge about whether a meeting seems necessary. Storing it as a row
lets the team see the history of recommendations over time.
"""

import datetime

from sqlmodel import Field, SQLModel


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class MeetingRecommendation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="team.id")
    date: datetime.date = Field(default_factory=datetime.date.today)

    # "meet" or "async" - the headline recommendation.
    recommendation: str = Field(default="async")
    # Human-readable explanation shown on the dashboard.
    reason: str = ""
    # 0.0 to 1.0 - how confident the heuristic is.
    confidence: float = Field(default=0.5)

    created_at: datetime.datetime = Field(default_factory=_now)
