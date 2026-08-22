"""Privacy and source-sharing settings.

The controls are intentionally local UI state for this MVP. They demonstrate
the consent model without pretending that provider connections or preferences
are persisted yet.
"""

from nicegui import ui

from app.ui.layout import (
    page_frame, h1, body, body_large, muted, badge,
    rounded_card, rounded_panel, section_heading, divider,
)


def render() -> None:
    with page_frame("Settings", active_path="/settings"):
        h1("Settings")
        body_large("You decide what Synq can use and what your team can see.")
        muted("These settings are a product demonstration. Connection states and preferences are mock data for now.")

        section_heading(
            "Connected sources",
            "Choose the work sources you want available for review.",
        )
        with rounded_card().classes("synq-settings-card"):
            for name, detail, status, variant in [
                ("GitHub", "Pull requests, commits, and code reviews", "Mock connected", "success"),
                ("Gmail", "Project-related sent and received mail", "Mock connected", "success"),
                ("Microsoft 365", "Outlook and Microsoft work activity", "Not connected", "neutral"),
                ("Google Workspace", "Google Calendar, Drive, and Workspace activity", "Not connected", "neutral"),
            ]:
                with ui.row().classes("synq-settings-row items-center justify-between w-full"):
                    with ui.column().classes("gap-1"):
                        ui.label(name).classes("synq-settings-name")
                        muted(detail)
                    badge(status, variant=variant)

        section_heading(
            "Sharing",
            "Keep raw activity private and choose what may help draft an update.",
        )
        with rounded_card().classes("synq-settings-card"):
            _setting_toggle(
                "Include activity in AI analysis",
                "Allow selected activity to inform a private draft summary.",
                True,
            )
            _setting_toggle(
                "Include blockers",
                "Let Synq use blockers when preparing a draft for your review.",
                False,
            )
            divider()
            with ui.column().classes("gap-1"):
                ui.label("Exclude specific activity types").classes("synq-settings-name")
                muted("Excluded activity stays out of future AI drafts.")
            with ui.column().classes("synq-exclusion-list gap-1"):
                for label, description in [
                    ("Commits", "Individual code changes"),
                    ("Pull requests", "Opened or merged changes"),
                    ("Code reviews", "Review activity and feedback"),
                    ("Project email", "Mock project-related messages"),
                ]:
                    ui.checkbox(label, value=False).props("dense").classes("synq-settings-checkbox")
                    muted(description).classes("synq-settings-checkbox-help")

        section_heading(
            "Review before sharing",
            "There is always a deliberate pause before anything reaches your team.",
        )
        with rounded_panel().classes("synq-review-settings"):
            with ui.row().classes("items-start justify-between w-full gap-4"):
                with ui.column().classes("gap-2"):
                    ui.label("Always review AI-generated updates").classes("synq-settings-name")
                    body("This safeguard is always on in the MVP and cannot be turned off.")
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


def _setting_toggle(title: str, description: str, value: bool) -> None:
    with ui.row().classes("synq-settings-toggle items-center justify-between w-full gap-4"):
        with ui.column().classes("gap-1"):
            ui.label(title).classes("synq-settings-name")
            muted(description)
        ui.switch(value=value)


def _visibility_item(title: str, description: str) -> None:
    with ui.column().classes("synq-visibility-item gap-1"):
        ui.label(title).classes("synq-settings-name")
        muted(description)
