"""GitHub integration boundary.

OAuth is not wired yet. The adapter keeps a stable shape so the rest of the
app can call it, and it returns no records until a real connection exists.
Users log GitHub work themselves from My Work.
"""

from app.models.work_activity import WorkActivity
from app.services.integrations.base import Integration


class GitHubIntegration(Integration):
    source = "github"

    def fetch_activities(self, user_id: int) -> list[WorkActivity]:
        return []


def fetch_activities(user_id: int) -> list[WorkActivity]:
    """Return normalized GitHub activities through the current adapter."""
    return GitHubIntegration().fetch_activities(user_id)
