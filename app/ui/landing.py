"""Landing page.

Public-facing explanation of Synq. Communicates the product in under 10
seconds with an oversized centered hero, minimal copy, and a visual product
preview showing team progress, recent updates, goals, and a meeting
recommendation.
"""

from nicegui import ui

from app.services.session_service import get_local_session_or_none
from app.ui.layout import (
    page_frame, display_heading, eyebrow, body_large,
    primary_button, secondary_button, badge, divider,
)


def render() -> None:
    with page_frame("Home", active_path="/", public=True):
        _hero()
        _product_preview()


def _hero() -> None:
    """Oversized centered hero with the headline, subheadline, and CTAs."""
    signed_in = get_local_session_or_none() is not None
    with ui.element("section").classes("synq-hero"):
        eyebrow("Async updates for software teams")
        display_heading("Fewer meetings. Better work.")
        body_large(
            "Your team's work speaks for itself. Turn daily progress into "
            "clear async updates, shared goals, and meetings that actually matter."
        )
        with ui.element("div").classes("synq-hero-cta"):
            if signed_in:
                primary_button("Open workspace", on_click=lambda: ui.navigate.to("/dashboard"))
            else:
                primary_button("Get started", on_click=lambda: ui.navigate.to("/onboarding"))
            secondary_button("See how it works", on_click=lambda: ui.navigate.to("/review" if signed_in else "/onboarding"))


def _product_preview() -> None:
    """Visual preview of the Synq dashboard below the hero.

    Illustrative product chrome only — not live workspace data.
    """
    with ui.element("div").classes("synq-preview"):
        with ui.element("div").classes("synq-preview-bar"):
            ui.element("span").classes("synq-preview-dot")
            ui.element("span").classes("synq-preview-dot")
            ui.element("span").classes("synq-preview-dot")
            ui.label("synq.app/dashboard").classes("synq-muted").style("margin-left: 8px; font-size: 0.82rem;")

        with ui.element("div").classes("synq-preview-body"):
            with ui.element("div").classes("synq-preview-col"):
                _updates_card()
            with ui.element("div").classes("synq-preview-col"):
                _goals_card()
                _meeting_card()


def _updates_card() -> None:
    with ui.element("div").classes("synq-preview-card"):
        ui.label("Recent updates").classes("synq-preview-card-title")
        divider()
        _update_row("You", "You", "Shipped the change you reviewed this afternoon.")
        _update_row("TM", "Teammate", "Closed the issue that was blocking launch.")
        _update_row("TL", "Team lead", "Set the goal for the next two weeks.")


def _update_row(initials: str, name: str, text: str) -> None:
    with ui.element("div").classes("synq-preview-row"):
        with ui.element("div").classes("flex items-center gap-2"):
            ui.label(initials[:2]).classes("synq-preview-avatar")
            with ui.element("div").classes("flex flex-col"):
                ui.label(name).style("font-weight: 600; font-size: 0.88rem; color: var(--synq-ink);")
                ui.label(text).style("font-size: 0.82rem; color: var(--synq-ink-2); max-width: 28ch;")
        badge("Published", variant="success")


def _goals_card() -> None:
    with ui.element("div").classes("synq-preview-card"):
        ui.label("Team goals").classes("synq-preview-card-title")
        divider()
        _goal_row("Ship the current milestone", 0)
        _goal_row("Keep meetings optional", 0)
        _goal_row("Publish updates daily", 0)


def _goal_row(title: str, progress: int) -> None:
    with ui.element("div").classes("flex flex-col gap-1"):
        with ui.element("div").classes("synq-preview-row"):
            ui.label(title).style("font-size: 0.86rem; color: var(--synq-ink); font-weight: 500;")
            ui.label(f"{progress}%").style("font-size: 0.8rem; color: var(--synq-ink-3); font-weight: 600;")
        ui.element("div").classes("synq-progress-track").style(
            f"background: linear-gradient(90deg, var(--synq-accent) {progress}%, var(--synq-surface-2) {progress}%);"
        )


def _meeting_card() -> None:
    with ui.element("div").classes("synq-preview-meeting"):
        with ui.element("div").classes("synq-preview-row"):
            ui.label("Meeting check").classes("synq-preview-card-title")
            badge("Async is enough", variant="success")
        ui.label(
            "Start with published updates. Synq will recommend a meeting only when blockers or stalled goals show up."
        ).style("font-size: 0.84rem; color: var(--synq-ink-2); line-height: 1.5;")
