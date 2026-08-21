"""AI service.

Placeholder for the future AI integration that drafts a work summary from
an activity snapshot. Keeping this behind a single function means the rest
of the app never needs to know whether AI is real or stubbed.

The MVP returns a fixed draft so the review flow can be built and tested
before any external API is wired up.
"""

from app.models.work_update import WorkUpdate


def generate_draft(snapshot: dict) -> WorkUpdate:
    """Return a draft WorkUpdate from an activity snapshot.

    `snapshot` is a dictionary of raw work data the user confirmed sharing.
    In the MVP we ignore its contents and return a placeholder draft; later
    this is where the real AI call will happen.
    """
    return WorkUpdate(
        title="AI draft",
        summary="AI draft: (placeholder summary of today's work).",
        accomplishments="- (placeholder accomplishment)",
        blockers="",
        published=False,
    )
