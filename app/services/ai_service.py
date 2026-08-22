"""Work-summary generation boundary.

The UI only needs a structured WorkSummary. Callers should keep using
`generate_work_summary`; they do not need to know which provider is used.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import httpx

from app.config import settings
from app.models.work_activity import WorkActivity

# Fields the UI already depends on. The provider must return exactly these.
_REQUIRED_FIELDS = ("title", "summary", "accomplishments", "blockers")
_TITLE_MAX = 160
_TEXT_MAX = 4000


@dataclass
class WorkSummary:
    """The four editable pieces of a proposed team update."""

    title: str
    summary: str
    accomplishments: str
    blockers: str


class AISummaryError(Exception):
    """A user-safe failure while drafting a summary.

    `str(error)` is suitable to show in the UI. Provider names and raw
    HTTP details stay inside this module.
    """


def generate_work_summary(activities: list[WorkActivity]) -> WorkSummary:
    """Draft a structured work summary from activity the user approved.

    Args:
        activities: The user's selected WorkActivity records for the work
            period. These records are not published by this function.

    Returns:
        A WorkSummary containing suggested title, summary, accomplishments,
        and blockers for the user to review and edit.

    Raises:
        AISummaryError: The draft could not be produced. The caller's
            activity list and any existing editor draft must be kept.
    """
    return generate_with_llm(activities)


def generate_with_llm(activities: list[WorkActivity]) -> WorkSummary:
    """Send approved activity to the configured model and validate the result."""
    if not settings.gemini_api_key.strip():
        raise AISummaryError(
            "AI drafting is not configured yet. Add an API key to your "
            "environment, then try again. Your activity is unchanged."
        )

    if not activities:
        return WorkSummary(title="Work update", summary="", accomplishments="", blockers="")

    # The prompt contains only activity the user kept for analysis, plus
    # instructions to return the four WorkSummary fields as JSON.
    prompt = _build_prompt(activities)

    try:
        raw_text = _request_completion(prompt)
    except AISummaryError:
        raise
    except httpx.TimeoutException as exc:
        raise AISummaryError(
            "The AI service took too long to respond. Your activity is still "
            "here — try again in a moment."
        ) from exc
    except httpx.HTTPError as exc:
        raise AISummaryError(
            "The AI service could not be reached. Check your connection and "
            "retry. Nothing was saved."
        ) from exc

    return _work_summary_from_response(raw_text)


def _approved_activity_payload(activities: list[WorkActivity]) -> list[dict[str, str]]:
    """Include only fields the user could see and explicitly kept.

    user_id, email, and integration metadata are omitted on purpose.
    """
    payload = []
    for activity in activities:
        description = (activity.description or "").strip()
        if not description:
            continue
        payload.append(
            {
                "date": activity.date.isoformat(),
                "source": activity.source,
                "activity_type": activity.activity_type,
                "description": description,
            }
        )
    return payload


def _build_prompt(activities: list[WorkActivity]) -> str:
    """Compose the model instructions and the approved activity JSON."""
    approved = _approved_activity_payload(activities)
    return (
        "You draft a private end-of-day work update for a software teammate.\n"
        "Use only the activity list provided. Do not invent work.\n"
        "If something looks unfinished or waiting on others, mention it in blockers.\n"
        "If there are no blockers, return an empty string for blockers.\n"
        "Return a JSON object with exactly these string keys:\n"
        "title, summary, accomplishments, blockers.\n"
        "title: a short headline (max 12 words).\n"
        "summary: 1-3 sentences in first person.\n"
        "accomplishments: bullet lines separated by newlines, each starting with •\n"
        "blockers: bullet lines separated by newlines, or an empty string.\n\n"
        "Approved activity:\n"
        f"{json.dumps(approved, ensure_ascii=False, indent=2)}"
    )


def _request_completion(prompt: str) -> str:
    """Perform the HTTP request to the configured model.

    This is the only place an external AI API is called. The UI and other
    services never import the provider client or see the API key.
    """
    model = settings.gemini_model.strip() or "gemini-2.0-flash"
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent"
    )
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json",
        },
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": settings.gemini_api_key.strip(),
    }
    with httpx.Client(timeout=45.0) as client:
        response = client.post(url, headers=headers, json=body)

    # API errors are translated into AISummaryError so the UI can retry
    # without losing the user's activity or any in-progress draft.
    if response.status_code == 401 or response.status_code == 403:
        raise AISummaryError(
            "The AI service rejected the request. Check that the API key is "
            "valid, then retry. Your activity was not sent to your team."
        )
    if response.status_code == 429:
        raise AISummaryError(
            "The AI service is busy right now. Wait a moment and retry. "
            "Your activity is still here."
        )
    if response.status_code >= 400:
        raise AISummaryError(
            "The AI service returned an error. Retry when you are ready. "
            "Your activity has been kept."
        )

    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        raise AISummaryError(
            "The AI service returned an unreadable response. Retry to try again."
        ) from exc

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AISummaryError(
            "The AI service did not return any draft text. Retry to try again."
        ) from exc


def _work_summary_from_response(raw_text: str) -> WorkSummary:
    """Parse and validate the model output before anything is saved.

    Validation rules:
    - the payload must be JSON object (markdown fences are stripped)
    - title, summary, accomplishments, and blockers must all be present
    - each field must coerce to a string
    - empty titles are rejected; extra keys are ignored
    Invalid payloads never reach the database.
    """
    payload = _parse_json_object(raw_text)
    return work_summary_from_payload(payload)


def work_summary_from_payload(payload: object) -> WorkSummary:
    """Validate a parsed object into WorkSummary. Used by tests and the client."""
    if not isinstance(payload, dict):
        raise AISummaryError(
            "The AI draft was not valid structured data. Retry to generate a new draft."
        )

    missing = [field for field in _REQUIRED_FIELDS if field not in payload]
    if missing:
        raise AISummaryError(
            "The AI draft was missing required fields. Retry to generate a new draft."
        )

    values: dict[str, str] = {}
    for field in _REQUIRED_FIELDS:
        values[field] = _as_clean_text(payload[field], field)

    if not values["title"]:
        raise AISummaryError(
            "The AI draft did not include a usable title. Retry to generate a new draft."
        )

    values["title"] = values["title"][:_TITLE_MAX]
    for field in ("summary", "accomplishments", "blockers"):
        values[field] = values[field][:_TEXT_MAX]

    return WorkSummary(
        title=values["title"],
        summary=values["summary"],
        accomplishments=values["accomplishments"],
        blockers=values["blockers"],
    )


def _parse_json_object(raw_text: str) -> object:
    text = (raw_text or "").strip()
    if text.startswith("```"):
        text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise AISummaryError(
            "The AI draft could not be read as structured data. Retry to try again."
        ) from exc


def _as_clean_text(value: object, field: str) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        lines = []
        for item in value:
            piece = str(item).strip()
            if piece:
                lines.append(piece if piece.startswith("•") else f"• {piece}")
        return "\n".join(lines)
    if isinstance(value, (int, float, bool)):
        return str(value).strip()
    raise AISummaryError(
        f"The AI draft had an invalid {field} value. Retry to generate a new draft."
    )
