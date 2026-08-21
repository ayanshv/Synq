"""Update service.

Handles creating, fetching, and publishing WorkUpdates. The UI calls these
functions instead of touching the database session directly, which keeps the
visibility rule (published = True/False) in one place.
"""

from sqlmodel import select

from app.database import get_session
from app.models.work_update import WorkUpdate


def create_update(user_id: int, team_id: int, title: str = "") -> WorkUpdate:
    """Create a fresh draft update for a user and return it."""
    with get_session() as session:
        update = WorkUpdate(user_id=user_id, team_id=team_id, title=title, published=False)
        session.add(update)
        session.commit()
        session.refresh(update)
        return update


def get_update(update_id: int) -> WorkUpdate | None:
    """Return a single update by id, or None if it does not exist."""
    with get_session() as session:
        return session.get(WorkUpdate, update_id)


def list_published_for_team(team_id: int) -> list[WorkUpdate]:
    """Return all published updates for a team, newest first."""
    with get_session() as session:
        statement = (
            select(WorkUpdate)
            .where(WorkUpdate.team_id == team_id)
            .where(WorkUpdate.published == True)  # noqa: E712
            .order_by(WorkUpdate.date.desc(), WorkUpdate.created_at.desc())
        )
        return list(session.exec(statement))


def publish_update(update_id: int) -> WorkUpdate | None:
    """Mark an update as published so it becomes visible to the team."""
    with get_session() as session:
        update = session.get(WorkUpdate, update_id)
        if update is None:
            return None
        update.published = True
        session.add(update)
        session.commit()
        session.refresh(update)
        return update


def hide_update(update_id: int) -> WorkUpdate | None:
    """Mark an update as unpublished so it is hidden from the team."""
    with get_session() as session:
        update = session.get(WorkUpdate, update_id)
        if update is None:
            return None
        update.published = False
        session.add(update)
        session.commit()
        session.refresh(update)
        return update
