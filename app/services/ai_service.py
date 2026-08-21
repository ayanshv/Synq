"""AI service.

Placeholder for the future AI integration that drafts a work summary from
an activity snapshot. Keeping this behind a single function means the rest
of the app never needs to know whether AI is real or stubbed.

The MVP returns a fixed draft so the review flow can be built and tested
before any external API is wired up.
"""

from app.models.work_activity import WorkActivity
from app.models.work_update import WorkUpdate


def generate_draft(snapshot: list[WorkActivity]) -> WorkUpdate:
    """Return a draft WorkUpdate from an activity snapshot.

    This intentionally uses simple deterministic transformations so the
    review flow can be used without an external provider or secret.
    """
    descriptions = [activity.description for activity in snapshot if activity.description]
    accomplishments = "\n".join(f"• {description}" for description in descriptions)
    blocker_lines = [
        description
        for description in descriptions
        if any(word in description.lower() for word in ("block", "blocked", "waiting"))
    ]
    return WorkUpdate(
        title="Progress across today's work",
        summary=(
            f"Made progress on {len(descriptions)} "
            f"{'activity' if len(descriptions) == 1 else 'activities'} today."
        ),
        accomplishments=accomplishments or "No accomplishments selected yet.",
        blockers="\n".join(f"• {line}" for line in blocker_lines) or "No blockers reported.",
        published=False,
    )
