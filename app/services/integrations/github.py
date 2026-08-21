"""GitHub integration boundary.

There is deliberately no GitHub API call here yet. The adapter currently
returns the GitHub slice of the offline mock data, so the rest of the app can
already depend on the future integration shape.
"""

from app.models.work_activity import WorkActivity
from app.services.integrations.base import Integration
from app.services.integrations.mock import MockIntegration


class GitHubIntegration(Integration):
    source = "github"

    def fetch_activities(self, user_id: int) -> list[WorkActivity]:
        # TODO: Replace this mock with authenticated GitHub API requests.
        return MockIntegration().fetch_activities(user_id, sources={"github"})


def fetch_activities(user_id: int) -> list[WorkActivity]:
    """Return normalized GitHub activities through the current adapter."""
    return GitHubIntegration().fetch_activities(user_id)