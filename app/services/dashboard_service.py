"""Read model for the team dashboard.

The dashboard needs a few small joins and derived counts. Keeping that work
here lets the page stay focused on presenting the data.
"""

from dataclasses import dataclass
from datetime import date, timedelta

from sqlmodel import select

from app.database import get_session
from app.models import (
    Goal,
    Team,
    User,
    WorkUpdate,
)
from app.services.meeting_service import MeetingSuggestion, recommend_meeting
from app.utils.helpers import local_today


@dataclass
class DashboardUpdate:
    person: str
    date: date
    summary: str
    accomplishments: str
    blockers: str


@dataclass
class DashboardActivity:
    person: str
    date: date
    description: str
    source: str


@dataclass
class DashboardData:
    updates: list[DashboardUpdate]
    goals: list[Goal]
    activities: list[DashboardActivity]
    recommendation: MeetingSuggestion
    updates_this_week: int
    active_goals: int
    completed_goals: int


def get_dashboard_data(team_id: int) -> DashboardData:
    """Load all published dashboard data for a team in one session."""
    with get_session() as session:
        users = session.exec(select(User).where(User.team_id == team_id)).all()
        names = {user.id: user.name for user in users}

        updates = session.exec(
            select(WorkUpdate)
            .where(WorkUpdate.team_id == team_id)
            .where(WorkUpdate.published == True)  # noqa: E712
            .order_by(WorkUpdate.date.desc(), WorkUpdate.created_at.desc())
        ).all()
        goals = session.exec(
            select(Goal).where(Goal.team_id == team_id).order_by(Goal.created_at)
        ).all()
        # Team timeline uses published updates only. Raw activity stays private.
        today = local_today()
        week_start = today - timedelta(days=today.weekday())
        completed = [goal for goal in goals if goal.progress >= 100 or goal.status == "completed"]
        team = session.get(Team, team_id)
        if team is None:
            raise ValueError(f"Team {team_id} does not exist.")
        return DashboardData(
            updates=[
                DashboardUpdate(
                    person=names.get(update.user_id, "Team member"),
                    date=update.date,
                    summary=update.summary,
                    accomplishments=update.accomplishments,
                    blockers=update.blockers,
                )
                for update in updates
            ],
            goals=list(goals),
            activities=[
                DashboardActivity(
                    person=names.get(update.user_id, "Team member"),
                    date=update.date,
                    description=update.title or update.summary,
                    source="update",
                )
                for update in updates[:12]
            ],
            recommendation=recommend_meeting(team),
            updates_this_week=sum(update.date >= week_start for update in updates),
            active_goals=len(goals) - len(completed),
            completed_goals=len(completed),
        )