"""Startup data cleanup.

The app no longer seeds fictional teams. If an older local database still
contains the original demo workspace, it is removed so the product starts
from a real onboarding flow.
"""

from sqlmodel import select

from app.database import get_session
from app.models import (
    Goal,
    MeetingRecommendation,
    Team,
    User,
    WorkActivity,
    WorkUpdate,
)

_DEMO_TEAM_NAME = "Northwind Labs"
_DEMO_EMAILS = {
    "anya@northwind.dev",
    "jordan@northwind.dev",
    "mira@northwind.dev",
    "theo@northwind.dev",
}


def run_seed() -> None:
    """Remove leftover demo records. Safe to call on every startup."""
    with get_session() as session:
        team = session.exec(select(Team).where(Team.name == _DEMO_TEAM_NAME)).first()
        users = list(session.exec(select(User)))
        demo_users = [
            user
            for user in users
            if (team is not None and user.team_id == team.id) or user.email in _DEMO_EMAILS
        ]
        if team is None and not demo_users:
            return

        user_ids = {user.id for user in demo_users if user.id is not None}
        team_ids = {team.id} if team is not None and team.id is not None else set()
        team_ids.update(user.team_id for user in demo_users if user.team_id is not None)

        if user_ids:
            for activity in session.exec(select(WorkActivity)):
                if activity.user_id in user_ids:
                    session.delete(activity)
            for update in session.exec(select(WorkUpdate)):
                if update.user_id in user_ids or update.team_id in team_ids:
                    session.delete(update)
        for goal in session.exec(select(Goal)):
            if goal.team_id in team_ids:
                session.delete(goal)
        for rec in session.exec(select(MeetingRecommendation)):
            if rec.team_id in team_ids:
                session.delete(rec)
        for user in demo_users:
            session.delete(user)
        if team is not None:
            session.delete(team)
        session.commit()
