"""Goals page.

Lets a team view and add goals. Goals feed the meeting service's heuristic
about whether a meeting is needed.
"""

from nicegui import ui

from app.services import goal_service
from app.ui.layout import (
    page_frame, h1, body, muted, field_label,
    primary_button, rounded_card, divider, empty_state, section_heading, badge,
)

_PLACEHOLDER_TEAM_ID = 1


def render() -> None:
    with page_frame("Goals", active_path="/goals"):
        h1("Team goals")
        body("What your team is working toward. Progress helps decide if a meeting is needed.")

        goals = goal_service.list_goals_for_team(_PLACEHOLDER_TEAM_ID)
        if not goals:
            empty_state("No goals yet", "Add your first goal to start tracking progress.")
        else:
            for goal in goals:
                with rounded_card().classes("flex flex-col gap-2"):
                    ui.label(goal.title).classes("synq-h2")
                    muted(goal.description)
                    badge(f"{goal.progress}% complete", variant="accent")

        divider()
        section_heading("Add a goal", "Give it a clear title and optional context.")
        title_input = ui.input(label="Title")
        desc_input = ui.textarea(label="Description")

        def add_goal():
            if not title_input.value:
                return
            goal_service.create_goal(
                team_id=_PLACEHOLDER_TEAM_ID,
                title=title_input.value,
                description=desc_input.value or "",
            )
            ui.navigate.to("/goals")

        primary_button("Add goal", on_click=add_goal)
