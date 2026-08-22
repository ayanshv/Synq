"""Calm, shared strategy view for team goals."""

from nicegui import ui

from app.models.goal import Goal
from app.services import goal_service
from app.services.session_service import get_local_session
from app.ui.layout import (
    badge,
    body,
    empty_state,
    h1,
    muted,
    page_frame,
    primary_button,
    rounded_card,
    section_heading,
)

def render() -> None:
    local_session = get_local_session()
    with page_frame("Goals", active_path="/goals"):
        h1("What are we moving toward?")
        body("A shared view of progress, without turning the work into a project plan.")

        goals = goal_service.list_goals_for_team(local_session.team_id)
        if goals:
            with ui.element("div").classes("synq-goals-list"):
                for goal in goals:
                    _goal_card(goal)
        else:
            empty_state("No goals yet", "Add a clear outcome to start tracking progress.")

        _add_goal_form()


def _goal_card(goal: Goal) -> None:
    progress = goal.progress
    with rounded_card().classes("synq-goal-card"):
        with ui.element("div").classes("synq-goal-card-top"):
            with ui.element("div").classes("synq-goal-card-copy"):
                ui.label(goal.title).classes("synq-goal-card-title")
                muted(goal.description or "No description yet.")
            with ui.element("div").classes("synq-goal-card-actions"):
                badge(_status_label(goal.status), _status_variant(goal.status))
                ui.button(icon="edit", on_click=lambda: _edit_goal(goal)).props(
                    "flat round"
                ).classes("synq-goal-edit")

        with ui.element("div").classes("synq-goal-progress-block"):
            with ui.element("div").classes("synq-goal-progress-heading"):
                ui.label(f"{progress:.0f}%").classes("synq-goal-progress-value")
                muted(f"{goal.current_value:g} of {goal.target_value:g}")
            ui.element("div").classes("synq-goal-progress-track").style(
                f"background: linear-gradient(90deg, var(--synq-accent) "
                f"{progress}%, var(--synq-surface-2) {progress}%);"
            )

        with ui.element("div").classes("synq-goal-details"):
            muted(f"Target · {goal.target_value:g}")
            muted(f"Status · {_status_label(goal.status)}")


def _add_goal_form() -> None:
    section_heading("Add a goal", "Name the outcome clearly; progress can be updated over time.")
    with rounded_card().classes("synq-goal-form"):
        title_input = ui.input("Goal title", placeholder="e.g. Ship the first public release")
        description_input = ui.textarea(
            "Short description",
            placeholder="What will be different when this is complete?",
        ).props("autogrow")
        with ui.row().classes("items-center gap-3 flex-wrap"):
            target_input = ui.number("Target", value=100, min=1)
            primary_button(
                "Add goal",
                on_click=lambda: _create_goal(
                    title_input, description_input, target_input
                ),
            )


def _create_goal(title_input, description_input, target_input) -> None:
    title = (title_input.value or "").strip()
    if not title:
        ui.notify("Give your goal a title first.", type="warning")
        return
    target = max(1, float(target_input.value or 100))
    local_session = get_local_session()
    goal_service.create_goal(
        team_id=local_session.team_id,
        title=title,
        description=(description_input.value or "").strip(),
        target_value=target,
    )
    ui.navigate.to("/goals")


def _edit_goal(goal: Goal) -> None:
    with ui.dialog() as dialog, ui.card().classes("synq-goal-dialog"):
        ui.label("Edit goal").classes("synq-h2")
        title_input = ui.input("Goal title", value=goal.title)
        description_input = ui.textarea("Short description", value=goal.description).props(
            "autogrow"
        )
        progress_input = ui.number(
            "Current progress",
            value=goal.current_value,
            min=0,
            max=goal.target_value,
        )
        status_input = ui.select(
            {
                "on_track": "On track",
                "at_risk": "At risk",
                "off_track": "Off track",
                "completed": "Complete",
            },
            label="Status",
            value=goal.status,
        )
        completed_input = ui.checkbox(
            "Mark this goal complete",
            value=goal.status == "completed",
        )
        with ui.row().classes("justify-end gap-3 w-full"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            primary_button(
                "Save changes",
                on_click=lambda: _save_goal(
                    dialog,
                    goal,
                    title_input,
                    description_input,
                    progress_input,
                    status_input,
                    completed_input,
                ),
            )
    dialog.open()


def _save_goal(
    dialog,
    goal: Goal,
    title_input,
    description_input,
    progress_input,
    status_input,
    completed_input,
) -> None:
    title = (title_input.value or "").strip()
    if not title:
        ui.notify("Give your goal a title first.", type="warning")
        return
    status = "completed" if completed_input.value else status_input.value
    current_value = goal.target_value if completed_input.value else float(
        progress_input.value or 0
    )
    goal_service.update_goal(
        goal_id=goal.id,
        title=title,
        description=(description_input.value or "").strip(),
        current_value=current_value,
        status=status,
    )
    dialog.close()
    ui.navigate.to("/goals")


def _status_label(status: str) -> str:
    return {
        "on_track": "On track",
        "at_risk": "At risk",
        "off_track": "Off track",
        "completed": "Complete",
    }.get(status, status.replace("_", " ").title())


def _status_variant(status: str) -> str:
    if status == "on_track" or status == "completed":
        return "success"
    return "warning"