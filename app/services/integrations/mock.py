"""Offline sample integration data for development and demos."""

import json
from datetime import date

from app.models.work_activity import WorkActivity
from app.services.integrations.base import Integration


class MockIntegration(Integration):
    """Return realistic sample activities without calling any external API."""

    def fetch_activities(
        self,
        user_id: int,
        sources: set[str] | None = None,
    ) -> list[WorkActivity]:
        """Return normalized sample activities, optionally filtered by source."""
        activities = [
            WorkActivity(
                user_id=user_id,
                date=date.today(),
                source="github",
                activity_type="pull_request",
                description="Opened pull request for the onboarding redesign",
                metadata_json=json.dumps({"action": "opened"}),
            ),
            WorkActivity(
                user_id=user_id,
                date=date.today(),
                source="github",
                activity_type="pull_request",
                description="Merged authentication refactor",
                metadata_json=json.dumps({"action": "merged"}),
            ),
            WorkActivity(
                user_id=user_id,
                date=date.today(),
                source="github",
                activity_type="commit",
                description="Committed code for billing integration tests",
                metadata_json=json.dumps({"action": "committed"}),
            ),
            WorkActivity(
                user_id=user_id,
                date=date.today(),
                source="github",
                activity_type="code_review",
                description="Reviewed code for the API rate-limit changes",
                metadata_json=json.dumps({"action": "reviewed"}),
            ),
            WorkActivity(
                user_id=user_id,
                date=date.today(),
                source="gmail",
                activity_type="sent_email",
                description="Sent project update about the launch timeline",
                metadata_json=json.dumps({"direction": "sent"}),
            ),
            WorkActivity(
                user_id=user_id,
                date=date.today(),
                source="gmail",
                activity_type="received_email",
                description="Received project email about launch readiness",
                metadata_json=json.dumps({"direction": "received"}),
            ),
        ]
        if sources is None:
            return activities
        return [activity for activity in activities if activity.source in sources]


def fetch_activities(user_id: int) -> list[WorkActivity]:
    """Convenient function for callers that want all mock sources."""
    return MockIntegration().fetch_activities(user_id)