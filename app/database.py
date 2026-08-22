"""Database setup.

Creates the SQLModel engine for SQLite and a helper that yields sessions.
Other modules import `init_db` (to create tables) and `get_session` (to talk
to the database) instead of constructing their own engines.
"""

from sqlmodel import Session, SQLModel, create_engine

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
    """Create all tables defined by SQLModel models.

    Importing the models package here ensures every model is registered with
    SQLModel's metadata before `create_all` runs.
    """
    # Import so SQLModel knows about the tables before creating them.
    from app import models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Yield a database session.

    Used as a dependency or called directly. The caller is responsible for
    committing/closing; using a context manager (`with get_session() as s:`)
    handles both automatically.
    """
    return Session(engine)
