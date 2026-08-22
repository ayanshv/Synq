"""Privacy, tools, and team invite settings."""

from nicegui import ui

from app.services.session_service import get_local_session_or_none
from app.services.workspace_service import (
    KNOWN_TOOLS,
    invite_url,
    update_user_settings,
    update_user_tools,
)
from app.ui.layout import (
    badge,
    body,
    body_large,
    h1,
    muted,
    page_frame,
    rounded_card,
    rounded_panel,
    secondary_button,
    section_heading,
    divider,
)


def render() -> None:
    local_session = get_local_session_or_none()
    if local_session is None:
        ui.navigate.to("/onboarding")
        return
    with page_frame("Settings", active_path="/settings"):
        h1("Settings")
        body_large("You decide what Synq can use and what your team can see.")

        section_heading(
            "Your team",
            f"{local_session.team_name} · invite people with this link.",
        )
        with rounded_card().classes("synq-settings-card"):
            link = invite_url(local_session.invite_code)
            ui.input("Invite link", value=link).props("readonly").classes("synq-editor-field")
            secondary_button(
                "Copy invite link",
                on_click=lambda: _copy(link),
            )
            muted("Teammates use the link to join. They will not see your private activity.")

        section_heading(
            "Connected sources",
            "These are the tools you chose during setup. They appear when you log work.",
        )
        selected = set(local_session.tools)
        boxes = {}
        with rounded_card().classes("synq-settings-card"):
            for key, name, detail in KNOWN_TOOLS:
                with ui.row().classes("synq-settings-row items-center justify-between w-full"):
                    with ui.column().classes("gap-1"):
                        ui.label(name).classes("synq-settings-name")
                        muted(detail)
                    if key == "manual":
                        badge("Always on", "success")
                    else:
                        boxes[key] = ui.switch(value=key in selected)
            if boxes:
                secondary_button(
                    "Save tools",
                    on_click=lambda: _save_tools(local_session.user_id, boxes),
                )

        prefs = local_session.settings
        section_heading(
            "Sharing",
            "Keep raw activity private and choose what may help draft an update.",
        )
        with rounded_card().classes("synq-settings-card"):
            include_ai = _setting_toggle(
                "Include activity in AI analysis",
                "Allow selected activity to inform a private draft summary.",
                bool(prefs.get("include_activity_in_ai", True)),
            )
            include_blockers = _setting_toggle(
                "Include blockers",
                "Let Synq use blockers when preparing a draft for your review.",
                bool(prefs.get("include_blockers", True)),
            )
            include_ai.on(
                "update:model-value",
                lambda _: update_user_settings(
                    local_session.user_id, {"include_activity_in_ai": bool(include_ai.value)}
                ),
            )
            include_blockers.on(
                "update:model-value",
                lambda _: update_user_settings(
                    local_session.user_id, {"include_blockers": bool(include_blockers.value)}
                ),
            )
            divider()
            with ui.column().classes("gap-1"):
                ui.label("Exclude specific activity types").classes("synq-settings-name")
                muted("Excluded activity stays out of future AI drafts.")
            excluded = {str(item) for item in prefs.get("excluded_types") or []}
            type_boxes = {}
            with ui.column().classes("synq-exclusion-list gap-1"):
                for key, label in [
                    ("commit", "Commits"),
                    ("pr", "Pull requests"),
                    ("review", "Code reviews"),
                    ("email", "Project email"),
                    ("note", "Personal notes"),
                ]:
                    type_boxes[key] = ui.checkbox(label, value=key in excluded).props("dense").classes(
                        "synq-settings-checkbox"
                    )
            secondary_button(
                "Save exclusions",
                on_click=lambda: _save_exclusions(local_session.user_id, type_boxes),
            )

        section_heading(
            "Review before sharing",
            "There is always a deliberate pause before anything reaches your team.",
        )
        with rounded_panel().classes("synq-review-settings"):
            with ui.row().classes("items-start justify-between w-full gap-4"):
                with ui.column().classes("gap-2"):
                    ui.label("Always review AI-generated updates").classes("synq-settings-name")
                    body("This safeguard is always on and cannot be turned off.")
                ui.switch(value=True).props("disable")
            with ui.element("div").classes("synq-review-statement"):
                ui.label("You review every AI-generated update before your team sees it.").classes(
                    "synq-review-statement-text"
                )

        section_heading(
            "Data visibility",
            "A simple view of what stays private and what becomes shared.",
        )
        with rounded_card().classes("synq-visibility-grid"):
            _visibility_item("Raw activity is private", "Source details stay with you while you review them.")
            _visibility_item("AI analysis needs confirmation", "A draft is created only within your review flow.")
            _visibility_item("Nothing is published automatically", "You choose whether to save a draft or publish it.")
            _visibility_item("Published information is visible to the team", "Only the update you approve becomes shared.")


def _copy(link: str) -> None:
    ui.clipboard.write(link)
    ui.notify("Invite link copied.", type="positive")


def _save_exclusions(user_id: int, type_boxes) -> None:
    update_user_settings(
        user_id,
        {"excluded_types": [key for key, box in type_boxes.items() if box.value]},
    )
    ui.notify("Exclusions saved.", type="positive")


def _save_tools(user_id: int, boxes) -> None:
    tools = [key for key, box in boxes.items() if box.value]
    update_user_tools(user_id, tools)
    ui.notify("Tools saved. They'll show up the next time you log work.", type="positive")


def _setting_toggle(title: str, description: str, value: bool):
    with ui.row().classes("synq-settings-toggle items-center justify-between w-full gap-4"):
        with ui.column().classes("gap-1"):
            ui.label(title).classes("synq-settings-name")
            muted(description)
        return ui.switch(value=value)


def _visibility_item(title: str, description: str) -> None:
    with ui.column().classes("synq-visibility-item gap-1"):
        ui.label(title).classes("synq-settings-name")
        muted(description)
