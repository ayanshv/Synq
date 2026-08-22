"""Gmail integration boundary.

This module never reads a real inbox. It exposes the same adapter shape that
a future Gmail implementation will use and currently returns no records.
"""

from app.models.work_activity import WorkActivity
from app.services.integrations.base import Integration


class GmailIntegration(Integration):
    source = "gmail"

    def fetch_activities(self, user_id: int) -> list[WorkActivity]:
        return []


def fetch_activities(user_id: int) -> list[WorkActivity]:
    """Return normalized Gmail activities through the current adapter."""
    return GmailIntegration().fetch_activities(user_id)
