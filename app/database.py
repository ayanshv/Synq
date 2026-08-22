"""Database setup.

Creates the SQLModel engine for SQLite and a helper that yields sessions.
Other modules import `init_db` (to create tables) and `get_session` (to talk
to the database) instead of constructing their own engines.
"""

from sqlalchemy import inspect, text
from sqlmodel import Session, SQLModel, create_engine, select

from app.config import settings

# `check_same_thread=False` lets NiceGUI's request handlers share a SQLite
# engine. PostgreSQL does not accept that SQLite-only connection option.
connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)
engine = create_engine(settings.database_url, echo=False, connect_args=connect_args)


def init_db() -> None:
    """Create all tables defined by SQLModel models, then add new columns."""
    from app import models  # noqa: F401

    SQLModel.metadata.create_all(engine)
    _migrate_schema()


def get_session() -> Session:
    """Yield a database session.

    Used as a dependency or called directly. The caller is responsible for
    committing/closing; using a context manager (`with get_session() as s:`)
    handles both automatically.
    """
    return Session(engine)


def _migrate_schema() -> None:
    """Add columns introduced after the first local database was created."""
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    if "team" in tables:
        _add_column_if_missing("team", "invite_code", "TEXT DEFAULT ''")
    if "user" in tables:
        _add_column_if_missing("user", "work_focus", "TEXT DEFAULT ''")
        _add_column_if_missing("user", "tools_json", "TEXT DEFAULT '[]'")
        _add_column_if_missing("user", "settings_json", "TEXT DEFAULT '{}'")
    _backfill_invite_codes()


def _add_column_if_missing(table: str, column: str, ddl: str) -> None:
    inspector = inspect(engine)
    existing = {col["name"] for col in inspector.get_columns(table)}
    if column in existing:
        return
    with engine.begin() as connection:
        connection.execute(text(f'ALTER TABLE "{table}" ADD COLUMN {column} {ddl}'))


def _backfill_invite_codes() -> None:
    from app.models.team import Team, new_invite_code

    with Session(engine) as session:
        for team in session.exec(select(Team)):
            if not (team.invite_code or "").strip():
                team.invite_code = new_invite_code()
                session.add(team)
        session.commit()
