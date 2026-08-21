"""Team dashboard page.

This page only renders the dashboard; dashboard_service owns database reads
and the shared layout/theme owns the visual language.
"""

from nicegui import ui

from app.services.dashboard_service import DashboardData, get_dashboard_data
from app.ui.layout import (
    badge,
    body,
    empty_state,
    h1,
    muted,
    page_frame,
    rounded_card,
    section_heading,
    stat_card,
)

_TEAM_ID = 1


def render() -> None:
    data = get_dashboard_data(_TEAM_ID)
    with page_frame("Dashboard", active_path="/dashboard"):
        _intro()
        _team_progress(data)
        with ui.element("div").classes("synq-dashboard-grid"):
            with ui.element("div").classes("synq-dashboard-main"):
                _goal_progress(data)
                _recent_updates(data)
            with ui.element("div").classes("synq-dashboard-side"):
                _meeting_recommendation(data)
                _activity_timeline(data)


def _intro() -> None:
    with ui.element("div").classes("synq-dashboard-intro"):
        h1("Good morning, team.")
        body("Here's where the work stands.")


def _team_progress(data: DashboardData) -> None:
    with ui.element("section").classes("synq-dashboard-section"):
        section_heading("Team progress", "A quiet read on the week so far.")
        with ui.element("div").classes("synq-stat-grid"):
            stat_card(str(data.updates_this_week), "Updates this week")
            stat_card(str(data.active_goals), "Active goals")
            stat_card(str(data.completed_goals), "Completed goals")
            recommendation = data.recommendation
            stat_card(
                "Meet" if recommendation and recommendation.recommendation == "meet" else "Async",
                "Meeting recommendation",
                "Based on the latest team check",
            )


def _goal_progress(data: DashboardData) -> None:
    with ui.element("section").classes("synq-dashboard-section"):
        section_heading("Team goal progress", "Progress toward the outcomes that matter.")
        if not data.goals:
            empty_state("No goals yet", "Add a goal to start tracking team progress.")
            return
        with rounded_card().classes("synq-goal-list"):
            for goal in data.goals:
                progress = min(100, max(0, goal.progress))
                with ui.element("div").classes("synq-goal-row"):
                    with ui.element("div").classes("synq-goal-heading"):
                        with ui.element("div").classes("flex flex-col gap-1"):
                            ui.label(goal.title).classes("synq-goal-title")
                            muted(goal.description)
                        with ui.element("div").classes("synq-goal-meta"):
                            ui.label(f"{progress:.0f}%").classes("synq-goal-percent")
                            badge(_goal_status(goal.status), _goal_variant(goal.status))
                    ui.element("div").classes("synq-progress-track").style(
                        f"background: linear-gradient(90deg, var(--synq-accent) "
                        f"{progress}%, var(--synq-surface-2) {progress}%);"
                    )


def _recent_updates(data: DashboardData) -> None:
    with ui.element("section").classes("synq-dashboard-section"):
        section_heading("Recent updates", "Published by your team.")
        if not data.updates:
            empty_state("No published updates yet", "When your team publishes, updates show up here.")
            return
        with ui.element("div").classes("synq-update-list"):
            for update in data.updates:
                with rounded_card().classes("synq-update-card"):
                    with ui.element("div").classes("synq-update-topline"):
                        with ui.element("div").classes("synq-person"):
                            ui.label(_initials(update.person)).classes(
                                "synq-avatar synq-avatar-small"
                            )
                            with ui.element("div").classes("flex flex-col gap-1"):
                                ui.label(update.person).classes("synq-update-name")
                                muted(update.date.strftime("%B %-d, %Y"))
                        badge("Published", "success")
                    body(update.summary)
                    _detail("Accomplishments", update.accomplishments)
                    if update.blockers.strip():
                        _detail("Blockers", update.blockers, "synq-blocker")


def _detail(label: str, text: str, extra_class: str = "") -> None:
    with ui.element("div").classes(f"synq-update-detail {extra_class}"):
        ui.label(label).classes("synq-detail-label")
        ui.label(text).classes("synq-detail-text")


def _meeting_recommendation(data: DashboardData) -> None:
    recommendation = data.recommendation
    needs_meeting = recommendation and recommendation.recommendation == "meet"
    title = "Meeting recommended." if needs_meeting else "No meeting recommended."
    reason = (
        recommendation.reason
        if recommendation and recommendation.reason
        else (
            "There are unresolved blockers or goals that need synchronous discussion."
            if needs_meeting
            else "All active work has recent updates and there are no unresolved blockers requiring synchronous discussion."
        )
    )
    with ui.element("section").classes("synq-dashboard-section"):
        section_heading("Meeting recommendation")
        with ui.element("div").classes(
            "synq-meeting-card synq-meeting-alert" if needs_meeting else "synq-meeting-card"
        ):
            with ui.element("div").classes("synq-meeting-title-row"):
                ui.label(title).classes("synq-meeting-title")
                badge("Discuss together" if needs_meeting else "Async is enough",
                      "warning" if needs_meeting else "success")
            body(reason)


def _activity_timeline(data: DashboardData) -> None:
    with ui.element("section").classes("synq-dashboard-section"):
        section_heading("Team activity", "A chronological view of recent work.")
        if not data.activities:
            empty_state("No activity yet", "Connected work will appear here.")
            return
        with rounded_card().classes("synq-timeline"):
            for activity in data.activities:
                with ui.element("div").classes("synq-timeline-item"):
                    ui.element("span").classes("synq-timeline-dot")
                    with ui.element("div").classes("synq-timeline-copy"):
                        with ui.element("div").classes("synq-timeline-heading"):
                            ui.label(activity.person).classes("synq-timeline-person")
                            muted(activity.date.strftime("%b %-d"))
                        body(activity.description)
                        muted(activity.source.title())


def _initials(name: str) -> str:
    return "".join(part[0] for part in name.split()[:2]).upper()


def _goal_status(status: str) -> str:
    return {"on_track": "On track", "at_risk": "At risk", "off_track": "Off track", "completed": "Complete"}.get(
        status, status.replace("_", " ").title()
    )


def _goal_variant(status: str) -> str:
    return "success" if status == "on_track" else "warning"