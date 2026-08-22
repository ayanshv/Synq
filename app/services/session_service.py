"""Local development session.

Authentication is intentionally out of scope for the MVP. This module gives
the application one clear place to resolve the fictional local user and team
from SQLite, so pages do not scatter placeholder IDs through their code.
"""

from dataclasses import dataclass

from sqlmodel import select

from app.database import get_session
from app.models import Team, User

LOCAL_USER_EMAIL = "anya@northwind.dev"


@dataclass(frozen=True)
class LocalSession:
    """The development user's database-backed workspace context."""

    user_id: int
    team_id: int
    user_name: str
    team_name: str


def get_local_session() -> LocalSession:
    """Resolve the seeded local user and team.

    This is a development convenience, not an authentication mechanism. A
    clear error is better than silently using the wrong team if seed data is
    missing or changed.
    """
    with get_session() as session:
        user = session.exec(
            select(User).where(User.email == LOCAL_USER_EMAIL)
        ).first()
        if user is None or user.id is None or user.team_id is None:
            raise RuntimeError(
                f"Local development user {LOCAL_USER_EMAIL!r} is not seeded."
            )
        team = session.get(Team, user.team_id)
        if team is None or team.id is None:
            raise RuntimeError(f"Local development team for {LOCAL_USER_EMAIL!r} is missing.")
        return LocalSession(
            user_id=user.id,
            team_id=team.id,
            user_name=user.name,
            team_name=team.name,
        )