"""Private My Work flow: collect, review, edit, and deliberately share."""

from nicegui import ui

from app.models.work_activity import WorkActivity
from app.services import ai_service, update_service, work_service
from app.services.ai_service import AISummaryError, WorkSummary
from app.services.session_service import get_local_session_or_none
from app.services.workspace_service import KNOWN_TOOLS
from app.ui.layout import (
    accent_button,
    accent_panel,
    badge,
    body,
    body_large,
    empty_state,
    h1,
    muted,
    page_frame,
    primary_button,
    rounded_card,
    secondary_button,
    section_heading,
)

_TYPE_BY_SOURCE = {
    "github": [("pr", "Pull request"), ("commit", "Commit"), ("review", "Code review")],
    "gmail": [("email", "Email")],
    "linear": [("issue", "Issue"), ("cycle", "Cycle work")],
    "slack": [("decision", "Decision"), ("follow_up", "Follow-up")],
    "calendar": [("meeting", "Meeting")],
    "docs": [("doc", "Doc")],
    "manual": [("note", "Note"), ("task", "Task")],
}


def render() -> None:
    local_session = get_local_session_or_none()
    if local_session is None:
        ui.navigate.to("/onboarding")
        return
    with page_frame("My Work", active_path="/review"):
        h1("Your work.")
        subtitle = "Log what you did, then decide what the team should see."
        if local_session.work_focus:
            subtitle = f"{local_session.work_focus.rstrip('.')} — then decide what to share."
        body_large(subtitle)

        flow = ui.column().classes("synq-work-flow w-full gap-6")
        with flow:
            _render_start(flow)


def _excluded_types() -> list[str]:
    session = get_local_session_or_none()
    if session is None:
        return []
    raw = session.settings.get("excluded_types") or []
    return [str(item) for item in raw]


def _load_today() -> list[WorkActivity]:
    local_session = get_local_session_or_none()
    if local_session is None:
        return []
    return work_service.list_today_for_user(local_session.user_id, _excluded_types())


def _render_start(flow: ui.element) -> None:
    local_session = get_local_session_or_none()
    tools = list(local_session.tools) if local_session else ["manual"]
    activities = _load_today()

    with accent_panel().classes("synq-work-status"):
        section_heading("Today's work", "Private until you publish. Add the work you want considered.")
        _activity_form(flow, tools)
        body("When the list looks right, finish work to review it.")
        primary_button("Finish work", on_click=lambda: _show_activity_summary(flow))
        muted("Nothing is shared automatically. You'll review everything before publishing.")

    _activity_card(activities, removable=False)


def _activity_form(flow: ui.element, tools: list[str]) -> None:
    labels = {key: title for key, title, _detail in KNOWN_TOOLS}
    source_options = {key: labels.get(key, key.title()) for key in tools}
    if not source_options:
        source_options = {"manual": "Personal notes"}
    default_source = next(iter(source_options))
    with ui.element("div").classes("synq-activity-form"):
        description = ui.input("What did you get done?", placeholder="Merged the billing retry fix")
        with ui.row().classes("synq-activity-form-meta"):
            source = ui.select(source_options, label="Source", value=default_source)
            type_options = dict(_TYPE_BY_SOURCE.get(default_source, _TYPE_BY_SOURCE["manual"]))
            activity_type = ui.select(type_options, label="Type", value=next(iter(type_options)))

            def on_source_change(_event=None) -> None:
                key = source.value or "manual"
                options = dict(_TYPE_BY_SOURCE.get(key, _TYPE_BY_SOURCE["manual"]))
                activity_type.set_options(options, value=next(iter(options)))

            source.on("update:model-value", on_source_change)
            secondary_button(
                "Add to today",
                on_click=lambda: _add_activity(flow, description, source, activity_type),
            )


def _add_activity(flow, description, source, activity_type) -> None:
    local_session = get_local_session_or_none()
    if local_session is None:
        return
    try:
        work_service.add_activity(
            user_id=local_session.user_id,
            description=description.value or "",
            source=source.value or "manual",
            activity_type=activity_type.value or "note",
        )
    except ValueError as error:
        ui.notify(str(error), type="warning")
        return
    description.value = ""
    ui.notify("Saved privately for today.", type="positive")
    flow.clear()
    with flow:
        _render_start(flow)


def _activity_card(activities: list[WorkActivity], removable: bool, on_change=None) -> None:
    with rounded_card().classes("synq-private-card"):
        with ui.element("div").classes("synq-private-heading"):
            badge("Private", "neutral")
            muted("These records are not visible to your team.")
        activity_list = ui.column().classes("synq-activity-list w-full")

        def redraw() -> None:
            activity_list.clear()
            with activity_list:
                if activities:
                    for activity in list(activities):
                        if removable:
                            _activity_row(activity, lambda item=activity: remove_activity(item))
                        else:
                            _activity_row(activity, None)
                else:
                    empty_state("Nothing logged yet", "Add a note above, then finish work.")

        def remove_activity(activity: WorkActivity) -> None:
            local_session = get_local_session_or_none()
            activities.remove(activity)
            if local_session is not None and activity.id is not None:
                work_service.delete_activity(activity.id, local_session.user_id)
            redraw()
            if on_change:
                on_change()
            ui.notify("Removed from this private activity set.", type="info")

        redraw()


def _show_activity_summary(flow: ui.element) -> None:
    activities = _load_today()
    flow.clear()
    with flow:
        _render_private_summary(flow, activities)


def _render_private_summary(
    flow: ui.element,
    activities: list[WorkActivity],
    error: str | None = None,
) -> None:
    section_heading("Your private activity summary", "Only you can see this until you choose to publish.")
    _activity_card(activities, removable=True)

    if error:
        with ui.element("div").classes("synq-error-banner"):
            ui.label("We couldn't draft an update.").classes("synq-review-notice-title")
            muted(error)
            muted("Your activity is still here. You can retry or write the update yourself.")

    include_ai = True
    local_session = get_local_session_or_none()
    if local_session is not None:
        include_ai = bool(local_session.settings.get("include_activity_in_ai", True))

    with ui.element("div").classes("synq-work-consent"):
        if include_ai:
            body("Allow AI to prepare a work update from these activities?")
            muted("Only the items still listed above are sent. Raw activity is never published.")
            with ui.row().classes("gap-3 flex-wrap"):
                accent_button(
                    "Analyze my work" if not error else "Try again",
                    on_click=lambda: _show_editor(flow, activities),
                )
                secondary_button("Write it myself", on_click=lambda: _show_blank_editor(flow, activities))
                secondary_button("Cancel", on_click=lambda: _render_start_again(flow))
        else:
            body("AI analysis is turned off in Settings. You can still write the update yourself.")
            with ui.row().classes("gap-3 flex-wrap"):
                accent_button("Write update", on_click=lambda: _show_blank_editor(flow, activities))
                secondary_button("Cancel", on_click=lambda: _render_start_again(flow))


def _activity_row(activity: WorkActivity, on_remove) -> None:
    with ui.element("div").classes("synq-activity-row"):
        with ui.element("div").classes("synq-activity-copy"):
            ui.label(activity.description).classes("synq-activity-title")
            muted(f"{activity.source.title()} · {activity.activity_type.replace('_', ' ').title()}")
        if on_remove is not None:
            ui.button(icon="close", on_click=on_remove).props("flat round").classes("synq-remove-button")


def _render_start_again(flow: ui.element) -> None:
    flow.clear()
    with flow:
        _render_start(flow)


def _show_blank_editor(flow: ui.element, activities: list[WorkActivity]) -> None:
    draft = WorkSummary(title="Work update", summary="", accomplishments="", blockers="")
    _open_editor(flow, draft, activities)


def _show_editor(flow: ui.element, activities: list[WorkActivity]) -> None:
    # Keep the activity view on screen until a valid draft comes back.
    try:
        draft = ai_service.generate_work_summary(activities)
        local_session = get_local_session_or_none()
        if local_session is not None and not local_session.settings.get("include_blockers", True):
            draft.blockers = ""
    except AISummaryError as error:
        flow.clear()
        with flow:
            _render_private_summary(flow, activities, error=str(error))
        return
    _open_editor(flow, draft, activities)


def _open_editor(flow: ui.element, draft: WorkSummary, activities: list[WorkActivity]) -> None:
    flow.clear()
    with flow:
        _render_editor(flow, draft, activities)


def _render_editor(flow: ui.element, draft: WorkSummary, activities: list[WorkActivity]) -> None:
    section_heading("Review your update", "Choose what feels useful, then make it sound like you.")
    with ui.element("div").classes("synq-review-notice"):
        ui.label("Nothing will appear on the team dashboard until you publish it.").classes(
            "synq-review-notice-title"
        )
        muted("You are in control of every word your team sees.")

    error_slot = ui.column().classes("w-full")

    with rounded_card().classes("synq-private-card"):
        section_heading("Included activity", "Remove anything you do not want this update to reflect.")
        activity_review = ui.column().classes("synq-activity-list w-full")

        def redraw_activity() -> None:
            activity_review.clear()
            with activity_review:
                if activities:
                    for activity in list(activities):
                        _activity_row(activity, lambda item=activity: remove_activity(item))
                else:
                    muted("No activity items selected. Your edited update can still be saved.")

        def remove_activity(activity: WorkActivity) -> None:
            local_session = get_local_session_or_none()
            activities.remove(activity)
            if local_session is not None and activity.id is not None:
                work_service.delete_activity(activity.id, local_session.user_id)
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
            blockers_enabled = ui.checkbox(
                "Include blockers",
                value=bool(draft.blockers.strip()),
            )
        accomplishments_input = ui.textarea(
            "Accomplishments", value=draft.accomplishments
        ).props("autogrow").classes("synq-editor-field")
        blockers_input = ui.textarea("Blockers", value=draft.blockers).props("autogrow").classes(
            "synq-editor-field"
        )

    def retry_ai() -> None:
        # On failure the current field values stay put so the draft is not lost.
        try:
            new_draft = ai_service.generate_work_summary(activities)
        except AISummaryError as error:
            error_slot.clear()
            with error_slot:
                with ui.element("div").classes("synq-error-banner"):
                    ui.label(str(error)).classes("synq-review-notice-title")
                    muted("Your current draft was kept. You can edit it or retry.")
            return
        title_input.value = new_draft.title
        summary_input.value = new_draft.summary
        accomplishments_input.value = new_draft.accomplishments
        blockers_input.value = new_draft.blockers
        error_slot.clear()
        ui.notify("Draft updated. Review it before publishing.", type="positive")

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
        secondary_button("Retry AI draft", on_click=retry_ai)
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
    local_session = get_local_session_or_none()
    if local_session is None:
        ui.navigate.to("/onboarding")
        return
    title = title_input.value or ""
    if not title.strip():
        ui.notify("Give the update a title before saving.", type="warning")
        return
    update_service.save_update(
        user_id=local_session.user_id,
        team_id=local_session.team_id,
        title=title,
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
