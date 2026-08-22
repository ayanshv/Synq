"""Onboarding wizard for a new workspace."""

from nicegui import ui

from app.services.session_service import get_local_session_or_none
from app.services.workspace_service import (
    KNOWN_TOOLS,
    WorkspaceError,
    create_workspace,
    invite_url,
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
    secondary_button,
    section_heading,
)


def render() -> None:
    existing = get_local_session_or_none()
    with page_frame("Get started", active_path="/onboarding", public=True):
        if existing is not None:
            h1("You're already set up.")
            body_large(f"You're in {existing.team_name} as {existing.user_name}.")
            primary_button("Go to dashboard", on_click=lambda: ui.navigate.to("/dashboard"))
            return

        h1("Set up Synq.")
        body_large("A few questions so the workspace matches how your team actually works.")
        flow = ui.column().classes("synq-wizard w-full")
        state = {
            "step": 1,
            "name": "",
            "email": "",
            "work_focus": "",
            "tools": ["manual"],
            "team_name": "",
        }
        with flow:
            _render_step(flow, state)


def _render_step(flow: ui.element, state: dict) -> None:
    flow.clear()
    with flow:
        muted(f"Step {state['step']} of 4")
        if state["step"] == 1:
            _step_you(flow, state)
        elif state["step"] == 2:
            _step_work(flow, state)
        elif state["step"] == 3:
            _step_tools(flow, state)
        else:
            _step_team(flow, state)


def _step_you(flow: ui.element, state: dict) -> None:
    section_heading("You", "So updates and the dashboard can use your real name.")
    with rounded_card().classes("synq-wizard-card"):
        name_input = ui.input("Your name", value=state["name"], placeholder="Jordan Chen")
        email_input = ui.input("Work email", value=state["email"], placeholder="you@company.com")
        with ui.row().classes("synq-wizard-actions"):
            primary_button(
                "Continue",
                on_click=lambda: _advance_you(flow, state, name_input, email_input),
            )


def _advance_you(flow, state, name_input, email_input) -> None:
    name = (name_input.value or "").strip()
    email = (email_input.value or "").strip()
    if not name or "@" not in email:
        ui.notify("Enter your name and a valid email to continue.", type="warning")
        return
    state["name"] = name
    state["email"] = email
    state["step"] = 2
    _render_step(flow, state)


def _step_work(flow: ui.element, state: dict) -> None:
    section_heading("Your work", "We'll use this to tailor empty states and activity types.")
    with rounded_card().classes("synq-wizard-card"):
        work_input = ui.textarea(
            "What do you work on?",
            value=state["work_focus"],
            placeholder="e.g. Backend for billing, plus reviewing frontend PRs",
        ).props("autogrow")
        with ui.row().classes("synq-wizard-actions"):
            secondary_button("Back", on_click=lambda: _go(flow, state, 1))
            primary_button(
                "Continue",
                on_click=lambda: _advance_work(flow, state, work_input),
            )


def _advance_work(flow, state, work_input) -> None:
    work = (work_input.value or "").strip()
    if not work:
        ui.notify("A short description of your work helps Synq stay useful.", type="warning")
        return
    state["work_focus"] = work
    state["step"] = 3
    _render_step(flow, state)


def _step_tools(flow: ui.element, state: dict) -> None:
    section_heading("Your tools", "Pick the sources you want available when you log work.")
    selected = set(state["tools"])
    boxes = {}
    with rounded_card().classes("synq-wizard-card"):
        with ui.element("div").classes("synq-tool-grid"):
            for key, title, detail in KNOWN_TOOLS:
                with ui.column().classes("synq-tool-option gap-1"):
                    boxes[key] = ui.checkbox(title, value=key in selected)
                    if key == "manual":
                        boxes[key].props("disable")
                        boxes[key].value = True
                    muted(detail)
        with ui.row().classes("synq-wizard-actions"):
            secondary_button("Back", on_click=lambda: _go(flow, state, 2))
            primary_button(
                "Continue",
                on_click=lambda: _advance_tools(flow, state, boxes),
            )


def _advance_tools(flow, state, boxes) -> None:
    state["tools"] = [key for key, box in boxes.items() if box.value]
    state["step"] = 4
    _render_step(flow, state)


def _step_team(flow: ui.element, state: dict) -> None:
    section_heading("Your team", "Create the workspace, then share an invite link.")
    with rounded_card().classes("synq-wizard-card"):
        team_input = ui.input(
            "Team name",
            value=state["team_name"],
            placeholder="e.g. Platform",
        )
        with ui.row().classes("synq-wizard-actions"):
            secondary_button("Back", on_click=lambda: _go(flow, state, 3))
            accent_button(
                "Create workspace",
                on_click=lambda: _finish(flow, state, team_input),
            )


def _finish(flow, state, team_input) -> None:
    team_name = (team_input.value or "").strip()
    if not team_name:
        ui.notify("Give your team a name.", type="warning")
        return
    state["team_name"] = team_name
    try:
        session = create_workspace(
            name=state["name"],
            email=state["email"],
            team_name=team_name,
            work_focus=state["work_focus"],
            tools=state["tools"],
        )
    except WorkspaceError as error:
        ui.notify(str(error), type="negative")
        return
    flow.clear()
    with flow:
        section_heading("Invite your team", "Nothing is shared until they join and publish their own updates.")
        with rounded_card().classes("synq-wizard-card"):
            body(f"{session.team_name} is ready. Send this link to the rest of the team.")
            link = invite_url(session.invite_code)
            ui.input(value=link).props("readonly").classes("synq-editor-field")
            with ui.row().classes("synq-wizard-actions"):
                secondary_button(
                    "Copy link",
                    on_click=lambda: _copy(link),
                )
                primary_button("Open dashboard", on_click=lambda: ui.navigate.to("/dashboard"))
            muted("You can copy this link again anytime from Settings.")


def _copy(link: str) -> None:
    ui.clipboard.write(link)
    ui.notify("Invite link copied.", type="positive")


def _go(flow, state, step: int) -> None:
    state["step"] = step
    _render_step(flow, state)
