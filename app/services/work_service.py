"""Private work-session reads and writes for the My Work page."""

from sqlmodel import select

from app.database import get_session
from app.models.work_activity import WorkActivity
from app.utils.helpers import local_today


def list_today_for_user(user_id: int, excluded_types: list[str] | None = None) -> list[WorkActivity]:
    """Return today's private activity records for one user."""
    excluded = {item.lower() for item in (excluded_types or [])}
    with get_session() as session:
        statement = (
            select(WorkActivity)
            .where(WorkActivity.user_id == user_id)
            .where(WorkActivity.date == local_today())
            .order_by(WorkActivity.created_at.desc())
        )
        rows = list(session.exec(statement))
    if not excluded:
        return rows
    return [row for row in rows if row.activity_type.lower() not in excluded]


def add_activity(
    user_id: int,
    description: str,
    source: str = "manual",
    activity_type: str = "note",
) -> WorkActivity:
    """Store a private activity the user entered or confirmed."""
    description = description.strip()
    if not description:
        raise ValueError("Describe the work first.")
    with get_session() as session:
        activity = WorkActivity(
            user_id=user_id,
            date=local_today(),
            source=source.strip() or "manual",
            activity_type=activity_type.strip() or "note",
            description=description,
        )
        session.add(activity)
        session.commit()
        session.refresh(activity)
        return activity


def delete_activity(activity_id: int, user_id: int) -> None:
    """Remove a private activity that still belongs to this user."""
    with get_session() as session:
        activity = session.get(WorkActivity, activity_id)
        if activity is None or activity.user_id != user_id:
            return
        session.delete(activity)
        session.commit()
