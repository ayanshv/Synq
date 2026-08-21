"""SQLModel data models for Synq.

Importing this package registers all models with SQLModel's metadata, which
`database.init_db()` relies on to create tables. Each model lives in its own
module so the schema stays easy to read and extend.
"""

from app.models.team import Team
from app.models.user import User
from app.models.work_update import WorkUpdate
from app.models.goal import Goal
from app.models.work_activity import WorkActivity
from app.models.meeting_recommendation import MeetingRecommendation

__all__ = [
    "Team",
    "User",
    "WorkUpdate",
    "Goal",
    "WorkActivity",
    "MeetingRecommendation",
]
