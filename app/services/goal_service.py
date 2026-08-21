"""Goal service.

Simple CRUD for team goals. Goals let a team state what they are working
toward; the meeting service reads goal status to help decide if a meeting
is needed.
"""

from sqlmodel import select

from app.database import get_session
from app.models.goal import Goal


def create_goal(
    team_id: int,
    title: str,
    description: str = "",
    target_value: float = 100.0,
    current_value: float = 0.0,
    status: str = "on_track",
) -> Goal:
    """Create a new goal for a team."""
    with get_session() as session:
        goal = Goal(
            team_id=team_id,
            title=title,
            description=description,
            target_value=target_value,
            current_value=current_value,
            status=status,
        )
        session.add(goal)
        session.commit()
        session.refresh(goal)
        return goal


def list_goals_for_team(team_id: int) -> list[Goal]:
    """Return all goals for a team."""
    with get_session() as session:
        statement = select(Goal).where(Goal.team_id == team_id)
        return list(session.exec(statement))


def update_progress(goal_id: int, current_value: float) -> Goal | None:
    """Set a goal's current value (clamped to 0..target_value)."""
    with get_session() as session:
        goal = session.get(Goal, goal_id)
        if goal is None:
            return None
        goal.current_value = max(0.0, min(goal.target_value, current_value))
        session.add(goal)
        session.commit()
        session.refresh(goal)
        return goal
