"""Settings page.

Placeholder for future account/tool-connection settings. For the MVP it
simply shows which integrations are not yet connected.
"""

from nicegui import ui

from app.ui.layout import (
    page_frame, h1, body, muted, badge,
    rounded_card, section_heading,
)


def render() -> None:
    with page_frame("Settings", active_path="/settings"):
        h1("Settings")
        body("Manage your account and connected tools.")

        section_heading("Connected tools", "Integrations that feed your work updates.")
        with rounded_card().classes("flex flex-col gap-3"):
            with ui.row().classes("items-center justify-between w-full"):
                body("GitHub")
                badge("Not connected", variant="neutral")
            with ui.row().classes("items-center justify-between w-full"):
                body("AI provider")
                badge("Not configured", variant="neutral")
