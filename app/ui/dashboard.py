"""Team dashboard.

Shows published updates from the team and a nudge about whether a meeting
seems necessary. This is where the whole team sees async progress.
"""

from nicegui import ui

from app.services import update_service, meeting_service
from app.ui.layout import (
    page_frame, section_heading, h1, body, muted, badge,
    rounded_card, divider, empty_state,
)

# Placeholder team id used until authentication/multi-tenancy is built.
_PLACEHOLDER_TEAM_ID = 1


def render() -> None:
    with page_frame("Dashboard", active_path="/dashboard"):
        h1("Team dashboard")
        body("Progress and updates from your team, in one calm view.")

        needed, reason = meeting_service.should_meet(_PLACEHOLDER_TEAM_ID)
        with rounded_card().classes("flex flex-col gap-2"):
            if needed:
                badge("Meeting suggested", variant="warning")
                body(reason)
            else:
                badge("Async is enough", variant="success")
                body(reason)

        divider()
        section_heading("Recent published updates", "Visible to everyone on the team.")

        updates = update_service.list_published_for_team(_PLACEHOLDER_TEAM_ID)
        if not updates:
            empty_state("No published updates yet", "When your team publishes, updates show up here.")
            return

        for update in updates:
            with rounded_card().classes("flex flex-col gap-2"):
                ui.label(f"Update #{update.id}").classes("synq-h2")
                body(update.summary)
                if update.blockers.strip():
                    muted(f"Blockers: {update.blockers}")
