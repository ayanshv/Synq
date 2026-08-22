"""Private My Work flow: collect, review, edit, and deliberately share."""

from nicegui import ui

from app.models.work_activity import WorkActivity
from app.services import ai_service, update_service, work_service
from app.ui.layout import (
    accent_button,
    accent_panel,
    badge,
    body,
    body_large,
    divider,
    empty_state,
    h1,
    muted,
    page_frame,
    primary_button,
    rounded_card,
    secondary_button,
    section_heading,
)

_TEAM_ID = 1
_USER_ID = 1


def render() -> None:
    with page_frame("My Work", active_path="/review"):
        h1("Your work.")
        body_large("Review what you accomplished before sharing it with your team.")

        with ui.element("div").classes("synq-work-flow w-full flex flex-col gap-6"):
            _render_start()


def _render_start() -> None:
    with accent_panel().classes("synq-work-status"):
        section_heading("Today's work", "A private starting point for your end-of-day review.")
        body("When you're ready, we'll gather today's activity for you to check.")
        primary_button("Finish work", on_click=_show_activity_summary)
        muted("Nothing is shared automatically. You'll review everything before publishing.")


def _show_activity_summary() -> None:
    activities = work_service.list_today_for_user(_USER_ID)
    ui.navigate.to("/review")


def _render_private_summary(activities: list[WorkActivity]) -> None:
    section_heading("Your private activity summary", "Only you can see this until you choose to publish.")
    activity_list = ui.column().classes("synq-activity-list w-full")

    def redraw() -> None:
        activity_list.clear()
        with activity_list:
            if activities:
                for activity in activities:
                    _activity_row(activity, lambda item=activity: remove_activity(item))
            else:
                empty_state("No activities selected", "You can still write a work update from scratch.")

    def remove_activity(activity: WorkActivity) -> None:
        activities.remove(activity)
        redraw()

    with rounded_card().classes("synq-private-card"):
        with ui.element("div").classes("synq-private-heading"):
            badge("Private", "neutral")
            muted("These records are not visible to your team.")
        redraw()

    with ui.element("div").classes("synq-work-consent"):
        body("Allow AI to prepare a work update from these activities?")
        with ui.row().classes("gap-3 flex-wrap"):
            accent_button("Analyze my work", on_click=lambda: _show_editor(activities))
            secondary_button("Cancel", on_click=_render_start)


def _activity_row(activity: WorkActivity, on_remove) -> None:
    with ui.element("div").classes("synq-activity-row"):
        with ui.element("div").classes("synq-activity-copy"):
            ui.label(activity.description).classes("synq-activity-title")
            muted(f"{activity.source.title()} · {activity.activity_type.title()}")
        ui.button(icon="close", on_click=on_remove).props("flat round").classes("synq-remove-button")


def _show_editor(activities: list[WorkActivity]) -> None:
    try:
        draft = ai_service.generate_work_summary(activities)
    except ai_service.AIServiceError as exc:
        ui.notify(str(exc), type="negative")
        _render_private_summary(activities)
        return
    _render_editor(draft, activities)


def _render_editor(draft, activities: list[WorkActivity]) -> None:
    section_heading("Review your update", "Choose what feels useful, then make it sound like you.")
    with ui.element("div").classes("synq-review-notice"):
        ui.label("Nothing will appear on the team dashboard until you publish it.").classes(
            "synq-review-notice-title"
        )
        muted("You are in control of every word your team sees.")

    with rounded_card().classes("synq-private-card"):
        section_heading("Included activity", "Remove anything you do not want this update to reflect.")
        activity_review = ui.column().classes("synq-activity-list w-full")

        def redraw_activity() -> None:
            activity_review.clear()
            with activity_review:
                if activities:
                    for activity in activities:
                        _activity_row(activity, remove_activity)
                else:
                    muted("No activity items selected. Your edited update can still be saved.")

        def remove_activity(activity: WorkActivity) -> None:
            activities.remove(activity)
            redraw_activity()
            ui.notify("Removed from this private activity set.", type="info")

        redraw_activity()

    with rounded_card().classes("synq-editor-card"):
        title_input = ui.input("Suggested title", value=draft.title).classes("synq-editor-field")
        summary_input = ui.textarea("Summary", value=draft.summary).props("autogrow").classes(
            "synq-editor-field"
        )
        with ui.element("div").classes("synq-include-grid"):
            summary_enabled = ui.checkbox("Include summary", value=True)
            accomplishments_enabled = ui.checkbox("Include accomplishments", value=True)
            blockers_enabled = ui.checkbox("Include blockers", value=False)
        accomplishments_input = ui.textarea(
            "Accomplishments", value=draft.accomplishments
        ).props("autogrow").classes("synq-editor-field")
        blockers_input = ui.textarea("Blockers", value=draft.blockers).props("autogrow").classes(
            "synq-editor-field"
        )

    with ui.element("div").classes("synq-editor-actions"):
        accent_button(
            "Publish update",
            on_click=lambda: _persist(
                title_input,
                summary_input,
                accomplishments_input,
                blockers_input,
                summary_enabled,
                accomplishments_enabled,
                blockers_enabled,
                True,
            ),
        )
        secondary_button(
            "Save as draft",
            on_click=lambda: _persist(
                title_input,
                summary_input,
                accomplishments_input,
                blockers_input,
                summary_enabled,
                accomplishments_enabled,
                blockers_enabled,
                False,
            ),
        )
        muted("Your draft stays private until you decide otherwise.")


def _persist(
    title_input,
    summary_input,
    accomplishments_input,
    blockers_input,
    summary_enabled,
    accomplishments_enabled,
    blockers_enabled,
    publish: bool,
) -> None:
    update_service.save_update(
        user_id=_USER_ID,
        team_id=_TEAM_ID,
        title=title_input.value or "",
        summary=summary_input.value or "" if summary_enabled.value else "",
        accomplishments=(
            accomplishments_input.value or "" if accomplishments_enabled.value else ""
        ),
        blockers=blockers_input.value or "" if blockers_enabled.value else "",
        published=publish,
    )
    if publish:
        ui.navigate.to("/dashboard")
    else:
        ui.notify("Saved privately as a draft.", type="positive")