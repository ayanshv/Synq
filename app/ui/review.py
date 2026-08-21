"""Review page.

The core Synq flow lives here:
    1. User clicks "Finish Work".
    2. App builds an activity snapshot (placeholder for now).
    3. User confirms AI analysis.
    4. AI draft is shown for review.
    5. User edits/hides/publishes.

For the MVP this page demonstrates the flow with placeholder data so the
shape of the UI is clear before real integrations are added.
"""

from nicegui import ui

from app.services import ai_service, update_service
from app.ui.layout import (
    page_frame, h1, eyebrow, body, body_large, muted,
    primary_button, secondary_button, accent_button,
    rounded_card, accent_panel, badge, divider, section_heading,
)

_PLACEHOLDER_TEAM_ID = 1
_PLACEHOLDER_USER_ID = 1


def render() -> None:
    with page_frame("Review", active_path="/review"):
        eyebrow("Finish Work")
        h1("Wrap up your day.")
        body_large(
            "Click the button when you're done working. Synq will draft an "
            "update you can review and publish to your team."
        )

        with accent_panel().classes("flex flex-col gap-3"):
            section_heading("You're in control", "Nothing is shared until you publish.")
            primary_button("Finish Work", on_click=_finish_work)

        # Filled in once the user goes through the flow.
        draft_container = ui.column().classes("w-full gap-3")


def _finish_work() -> None:
    # Placeholder snapshot of "work data". Real integrations fill this.
    snapshot = {"placeholder": True}
    draft = ai_service.generate_draft(snapshot)
    saved = update_service.create_update(
        user_id=_PLACEHOLDER_USER_ID, team_id=_PLACEHOLDER_TEAM_ID
    )
    saved.summary = draft.summary
    saved.accomplishments = draft.accomplishments
    saved.blockers = draft.blockers
    update_service.publish_update(saved.id)

    draft_container = ui.column().classes("w-full gap-3")
    with draft_container:
        divider()
        section_heading("Your draft update", "Review, edit, then publish to your team.")
        with rounded_card().classes("flex flex-col gap-2"):
            badge("Draft", variant="neutral")
            body(draft.summary)
            muted(f"Accomplishments: {draft.accomplishments}")
            muted(f"Blockers: {draft.blockers}")
        with ui.row().classes("gap-3 flex-wrap"):
            accent_button("Publish to team", on_click=lambda: ui.navigate.to("/dashboard"))
            secondary_button("Keep editing")
