"""Seed data for development.

Creates a fictional startup team with four members, two goals, several
work activities, and several published updates so the dashboard has
realistic data to show on first run.

All data is fictional. `run_seed()` is safe to call repeatedly: it checks
for an existing team by name and does nothing if one is found.
"""

from datetime import date, timedelta

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


def run_seed() -> None:
    """Insert fictional sample data if the database is empty."""
    with get_session() as session:
        # Don't re-seed if the team already exists.
        existing = session.exec(select(Team).where(Team.name == "Northwind Labs")).first()
        if existing is not None:
            return

        _create_team(session)
        _create_users(session)
        _create_goals(session)
        _create_activities(session)
        _create_updates(session)
        _create_recommendation(session)
        session.commit()


def _create_team(session) -> None:
    team = Team(name="Northwind Labs")
    session.add(team)
    session.flush()  # get the team id for the foreign keys below
    # Stash the id on the session so helper functions can read it.
    session.info["team_id"] = team.id


def _create_users(session) -> None:
    team_id = session.info["team_id"]
    users = [
        User(team_id=team_id, name="Anya Kapoor", email="anya@northwind.dev", role="lead"),
        User(team_id=team_id, name="Jordan Diaz", email="jordan@northwind.dev", role="member"),
        User(team_id=team_id, name="Mira Lopez", email="mira@northwind.dev", role="member"),
        User(team_id=team_id, name="Theo Bennett", email="theo@northwind.dev", role="member"),
    ]
    session.add_all(users)
    session.flush()
    # Map name -> id for the update/activity helpers.
    session.info["user_ids"] = {u.name: u.id for u in users}


def _create_goals(session) -> None:
    team_id = session.info["team_id"]
    goals = [
        Goal(
            team_id=team_id,
            title="Ship v1 launch",
            description="Public launch of the Synq v1 product.",
            target_value=100.0,
            current_value=78.0,
            status="on_track",
        ),
        Goal(
            team_id=team_id,
            title="Reduce meeting load by 30%",
            description="Cut weekly meeting hours across the team.",
            target_value=30.0,
            current_value=14.0,
            status="at_risk",
        ),
    ]
    session.add_all(goals)


def _create_activities(session) -> None:
    user_ids = session.info["user_ids"]
    today = date.today()
    activities = [
        WorkActivity(
            user_id=user_ids["Anya Kapoor"], date=today,
            source="github", activity_type="pr",
            description="Merged onboarding redesign (#142)",
        ),
        WorkActivity(
            user_id=user_ids["Anya Kapoor"], date=today,
            source="github", activity_type="commit",
            description="Fixed auth redirect loop",
        ),
        WorkActivity(
            user_id=user_ids["Jordan Diaz"], date=today,
            source="linear", activity_type="issue",
            description="Triaged inbound bug reports",
        ),
        WorkActivity(
            user_id=user_ids["Jordan Diaz"], date=today,
            source="github", activity_type="pr",
            description="Reviewed three pull requests",
        ),
        WorkActivity(
            user_id=user_ids["Mira Lopez"], date=today,
            source="github", activity_type="commit",
            description="Added billing integration tests",
        ),
        WorkActivity(
            user_id=user_ids["Theo Bennett"], date=today,
            source="manual", activity_type="doc",
            description="Drafted API rate-limit docs",
        ),
    ]
    session.add_all(activities)


def _create_updates(session) -> None:
    team_id = session.info["team_id"]
    user_ids = session.info["user_ids"]
    today = date.today()
    yesterday = today - timedelta(days=1)

    updates = [
        WorkUpdate(
            user_id=user_ids["Anya Kapoor"], team_id=team_id, date=today,
            title="Onboarding + auth fixes",
            summary="Shipped the onboarding redesign and fixed three auth bugs.",
            accomplishments="Merged onboarding redesign. Fixed auth redirect loop.",
            blockers="",
            published=True,
        ),
        WorkUpdate(
            user_id=user_ids["Jordan Diaz"], team_id=team_id, date=today,
            title="Bug triage and reviews",
            summary="Reviewed pull requests and triaged the bug backlog.",
            accomplishments="Reviewed three PRs. Triaged inbound bug reports.",
            blockers="Blocked on API rate limit increase from provider.",
            published=True,
        ),
        WorkUpdate(
            user_id=user_ids["Mira Lopez"], team_id=team_id, date=yesterday,
            title="Billing test coverage",
            summary="Wrote integration tests for the billing flow.",
            accomplishments="Added integration tests for billing.",
            blockers="",
            published=True,
        ),
    ]
    session.add_all(updates)


def _create_recommendation(session) -> None:
    team_id = session.info["team_id"]
    rec = MeetingRecommendation(
        team_id=team_id,
        date=date.today(),
        recommendation="async",
        reason="Team is on track. One blocker reported but not blocking others.",
        confidence=0.82,
    )
    session.add(rec)
