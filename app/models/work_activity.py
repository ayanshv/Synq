"""WorkActivity model.

A WorkActivity is a single raw event pulled from an integration (GitHub,
Linear, etc.) or entered manually. Activities are the input the AI uses to
draft a WorkUpdate. They are private to the user until the user chooses to
include them in a published update.

`metadata_json` stores integration-specific details as a JSON string so the
table stays flat and simple for the MVP.
"""

import datetime

from sqlmodel import Field, SQLModel

from app.utils.helpers import local_today


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class WorkActivity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: datetime.date = Field(default_factory=local_today)

    # Where the activity came from: "github", "linear", "manual", etc.
    source: str = Field(default="manual", index=True)
    # What kind of activity: "commit", "pr", "issue", "doc", etc.
    activity_type: str = Field(default="task")
    description: str = ""
    # Free-form JSON string for extra fields the UI may need later.
    metadata_json: str = Field(default="{}")

    created_at: datetime.datetime = Field(default_factory=_now)
