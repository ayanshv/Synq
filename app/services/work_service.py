"""Private work-session reads for the My Work page."""

from datetime import date

from sqlmodel import select

from app.database import get_session
from app.models.work_activity import WorkActivity


def list_today_for_user(user_id: int) -> list[WorkActivity]:
    """Return today's private activity records for one user."""
    with get_session() as session:
        statement = (
            select(WorkActivity)
            .where(WorkActivity.user_id == user_id)
            .where(WorkActivity.date == date.today())
            .order_by(WorkActivity.created_at.desc())
        )
        return list(session.exec(statement))