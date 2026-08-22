"""Landing page.

Public-facing explanation of Synq. Communicates the product in under 10
seconds with an oversized centered hero, minimal copy, and a visual product
preview showing team progress, recent updates, goals, and a meeting
recommendation.
"""

from nicegui import ui

from app.ui.layout import (
    page_frame, display_heading, eyebrow, body_large,
    primary_button, secondary_button, badge, divider,
)


def render() -> None:
    with page_frame("Home", active_path="/"):
        _hero()
        _product_preview()


def _hero() -> None:
    """Oversized centered hero with the headline, subheadline, and CTAs."""
    with ui.element("section").classes("synq-hero"):
        eyebrow("Async updates for software teams")
        display_heading("Fewer meetings. Better work.")
        body_large(
            "Your team's work speaks for itself. Turn daily progress into "
            "clear async updates, shared goals, and meetings that actually matter."
        )
        with ui.element("div").classes("synq-hero-cta"):
            primary_button("Try the workspace", on_click=lambda: ui.navigate.to("/dashboard"))
            secondary_button("See how it works", on_click=lambda: ui.navigate.to("/review"))


def _product_preview() -> None:
    """Fake visual preview of the Synq dashboard below the hero.

    Purely visual - no real data. Shows the shape of the product so visitors
    immediately understand what they're signing up for.
    """
    with ui.element("div").classes("synq-preview"):
        # Faux browser bar
        with ui.element("div").classes("synq-preview-bar"):
            ui.element("span").classes("synq-preview-dot")
            ui.element("span").classes("synq-preview-dot")
            ui.element("span").classes("synq-preview-dot")
            ui.label("synq.app/dashboard").classes("synq-muted").style("margin-left: 8px; font-size: 0.82rem;")

        with ui.element("div").classes("synq-preview-body"):
            # Left column: recent updates
            with ui.element("div").classes("synq-preview-col"):
                _updates_card()

            # Right column: goals + meeting recommendation
            with ui.element("div").classes("synq-preview-col"):
                _goals_card()
                _meeting_card()


def _updates_card() -> None:
    """Recent published updates from the team."""
    with ui.element("div").classes("synq-preview-card"):
        ui.label("Recent updates").classes("synq-preview-card-title")
        divider()
        _update_row("AK", "Anya K.", "Shipped onboarding redesign. Fixed three auth bugs.")
        _update_row("JD", "Jordan D.", "Reviewed pull requests. Blocked on API rate limit.")
        _update_row("ML", "Mira L.", "Wrote integration tests for billing flow.")


def _update_row(initials: str, name: str, text: str) -> None:
    with ui.element("div").classes("synq-preview-row"):
        with ui.element("div").classes("flex items-center gap-2"):
            ui.label(initials).classes("synq-preview-avatar")
            with ui.element("div").classes("flex flex-col gap-1"):
                ui.label(name).classes("synq-update-name")
                ui.label(text).classes("synq-muted").style("max-width: 30ch;")
        badge("Published", variant="success")


def _goals_card() -> None:
    """Team goals with progress bars."""
    with ui.element("div").classes("synq-preview-card"):
        ui.label("Team goals").classes("synq-preview-card-title")
        divider()
        _goal_row("Ship v1 launch", 78)
        _goal_row("Reduce meeting load", 45)
        _goal_row("Improve test coverage", 62)


def _goal_row(title: str, progress: int) -> None:
    with ui.element("div").classes("flex flex-col gap-2"):
        with ui.element("div").classes("synq-preview-row"):
            ui.label(title).classes("synq-goal-title").style("font-size: 0.88rem;")
            ui.label(f"{progress}%").classes("synq-muted").style("font-weight: 600; font-size: 0.82rem;")
        ui.element("div").classes("synq-progress-track").style(
            f"background: linear-gradient(90deg, var(--synq-accent) {progress}%, var(--synq-surface-2) {progress}%);"
        )


def _meeting_card() -> None:
    """Meeting recommendation nudge."""
    with ui.element("div").classes("synq-preview-meeting"):
        with ui.element("div").classes("synq-preview-row"):
            ui.label("Meeting check").classes("synq-preview-card-title")
            badge("Async is enough", variant="success")
        ui.label(
            "Team is on track. No blockers reported. Skip the standup and keep building."
        ).classes("synq-muted").style("line-height: 1.5;")
