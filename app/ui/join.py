"""Join an existing team from an invite link."""

from nicegui import ui

from app.services.session_service import get_local_session_or_none
from app.services.workspace_service import (
    KNOWN_TOOLS,
    WorkspaceError,
    get_team_by_invite,
    join_workspace,
)
from app.ui.layout import (
    accent_button,
    body,
    body_large,
    h1,
    muted,
    page_frame,
    primary_button,
    rounded_card,
    section_heading,
)


def render(code: str) -> None:
    team = get_team_by_invite(code)
    existing = get_local_session_or_none()
    with page_frame("Join team", active_path="/onboarding", public=True):
        if team is None:
            h1("Invite not found.")
            body_large("Ask a teammate to send a fresh link from Settings.")
            primary_button("Get started instead", on_click=lambda: ui.navigate.to("/onboarding"))
            return

        if existing is not None and existing.invite_code == code:
            h1("You're already on this team.")
            body_large(f"Signed in as {existing.user_name} on {existing.team_name}.")
            primary_button("Go to dashboard", on_click=lambda: ui.navigate.to("/dashboard"))
            return

        h1(f"Join {team.name}.")
        body_large("Tell us who you are so your updates show up with your name.")
        with rounded_card().classes("synq-wizard-card"):
            name_input = ui.input("Your name", placeholder="Alex Rivera")
            email_input = ui.input("Work email", placeholder="you@company.com")
            work_input = ui.textarea(
                "What do you work on?",
                placeholder="e.g. Product design for the mobile app",
            ).props("autogrow")
            muted("Tools you use — we'll show these when you log work.")
            boxes = {}
            with ui.element("div").classes("synq-tool-grid"):
                for key, title, detail in KNOWN_TOOLS:
                    with ui.column().classes("synq-tool-option gap-1"):
                        boxes[key] = ui.checkbox(title, value=key == "manual")
                        if key == "manual":
                            boxes[key].props("disable")
                            boxes[key].value = True
                        muted(detail)
            accent_button(
                "Join workspace",
                on_click=lambda: _join(code, name_input, email_input, work_input, boxes),
            )


def _join(code, name_input, email_input, work_input, boxes) -> None:
    try:
        join_workspace(
            code=code,
            name=name_input.value or "",
            email=email_input.value or "",
            work_focus=work_input.value or "",
            tools=[key for key, box in boxes.items() if box.value],
        )
    except WorkspaceError as error:
        ui.notify(str(error), type="negative")
        return
    ui.navigate.to("/dashboard")
