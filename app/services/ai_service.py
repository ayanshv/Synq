"""Work-summary generation boundary.

The UI only needs a structured WorkSummary. The implementation can later
switch from this mock to an external model without changing that UI code.
"""

from dataclasses import dataclass

from app.models.work_activity import WorkActivity


@dataclass
class WorkSummary:
    """The four editable pieces of a proposed team update."""

    title: str
    summary: str
    accomplishments: str
    blockers: str


def generate_work_summary(activities: list[WorkActivity]) -> WorkSummary:
    """Create a believable mock summary from private activity records.

    Args:
        activities: The user's selected WorkActivity records for the work
            period. These records are not published by this function.

    Returns:
        A WorkSummary containing suggested title, summary, accomplishments,
        and blockers for the user to review and edit.
    """
    descriptions = [
        activity.description.strip()
        for activity in activities
        if activity.description.strip()
    ]
    count = len(descriptions)
    activity_word = "activity" if count == 1 else "activities"
    accomplishments = "\n".join(f"• {description}" for description in descriptions)
    blocker_lines = [
        description
        for description in descriptions
        if any(
            word in description.lower()
            for word in ("block", "blocked", "waiting", "dependency")
        )
    ]

    if count == 0:
        return WorkSummary(
            title="Work update",
            summary="No activity was selected for today's update.",
            accomplishments="",
            blockers="",
        )

    return WorkSummary(
        title="Progress across today's work",
        summary=f"Made progress across {count} {activity_word} today: "
        f"{'; '.join(descriptions)}",
        accomplishments=accomplishments,
        blockers="\n".join(f"• {line}" for line in blocker_lines),
    )


def generate_with_llm(activities: list[WorkActivity]) -> WorkSummary:
    """Future provider implementation for OpenAI, Gemini, or another model."""
    # TODO: Send the selected activities to the configured AI provider,
    # validate its response into WorkSummary, and handle provider failures.
    raise NotImplementedError("LLM summary generation is not implemented yet.")