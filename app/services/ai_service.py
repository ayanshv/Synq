"""Work-summary generation boundary.

The rest of the app only calls `generate_work_summary(activities)` and
receives a `WorkSummary`. It never knows whether the summary came from a
local heuristic or a hosted LLM — that decision is made here based on
whether an API key is configured.

Provider: Google Gemini API (gemini-1.5-flash by default). The model is
asked to return strict JSON matching the WorkSummary shape. If the
provider is unavailable, misbehaves, or returns malformed JSON, we raise
AIServiceError so the UI can show a friendly message and let the user
retry without losing their draft.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

import httpx

from app.config import settings
from app.models.work_activity import WorkActivity


# ---------------------------------------------------------------------------
# Public data structure — unchanged from the mock version.
# ---------------------------------------------------------------------------

@dataclass
class WorkSummary:
    """The four editable pieces of a proposed team update."""

    title: str
    summary: str
    accomplishments: str
    blockers: str


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class AIServiceError(Exception):
    """Raised when the LLM provider call cannot produce a usable result.

    The UI catches this to show a friendly message and let the user retry
    without losing the activity data they already reviewed.
    """


# ---------------------------------------------------------------------------
# Public entry point — same signature as the original mock.
# ---------------------------------------------------------------------------

def generate_work_summary(activities: list[WorkActivity]) -> WorkSummary:
    """Generate a WorkSummary from the user's approved activities.

    If a Gemini API key is configured, the real LLM is used. Otherwise we
    fall back to the local heuristic so the app stays usable in dev.

    Args:
        activities: The activity records the user explicitly approved for
            analysis. Only the description / source / type fields are sent
            to the provider — never ids, user ids, or metadata.

    Returns:
        A validated WorkSummary.

    Raises:
        AIServiceError: If the LLM was attempted but failed and no usable
            result could be produced. The caller should catch this, show a
            friendly message, and allow retry.
    """
    if not settings.gemini_api_key:
        return _local_summary(activities)

    return _llm_summary(activities)


# ---------------------------------------------------------------------------
# Local heuristic fallback (the original mock logic, unchanged).
# ---------------------------------------------------------------------------

def _local_summary(activities: list[WorkActivity]) -> WorkSummary:
    """Build a simple summary locally without any external call."""
    descriptions = [
        a.description.strip() for a in activities if a.description.strip()
    ]
    count = len(descriptions)
    if count == 0:
        return WorkSummary("Work update", "No activity was selected for today's update.", "", "")

    accomplishments = "\n".join(f"• {d}" for d in descriptions)
    blocker_lines = [
        d for d in descriptions
        if any(w in d.lower() for w in ("block", "blocked", "waiting", "dependency"))
    ]
    word = "activity" if count == 1 else "activities"
    return WorkSummary(
        title="Progress across today's work",
        summary=f"Made progress across {count} {word} today: {'; '.join(descriptions)}",
        accomplishments=accomplishments,
        blockers="\n".join(f"• {l}" for l in blocker_lines),
    )


# ---------------------------------------------------------------------------
# LLM integration — Google Gemini
# ---------------------------------------------------------------------------

_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
# The Gemini REST endpoint for generateContent. The API key is passed as a
# query parameter per Google's convention.
_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
_TIMEOUT = 30.0


def _build_prompt(activities: list[WorkActivity]) -> str:
    """Build the instruction text sent to the Gemini model.

    The prompt contains ONLY:
      - an instruction describing the desired output schema
      - the activity descriptions the user approved (source, type, text)

    It does NOT include ids, user ids, team ids, metadata_json, or any
    other internal field. This is the privacy boundary: only what the user
    explicitly approved leaves the system.
    """
    activity_lines = [
        f"- [{a.source} / {a.activity_type}] {a.description.strip()}"
        for a in activities
        if a.description.strip()
    ]
    activity_block = "\n".join(activity_lines) or "- (no activities)"

    return (
        "You are a concise work-summary assistant for a software team. "
        "Given a list of work activities, produce a short end-of-day update. "
        "Respond with ONLY a JSON object — no markdown, no prose — with exactly "
        "these string keys: title, summary, accomplishments, blockers. "
        "title: a short headline (max 60 chars). "
        "summary: one or two sentences. "
        "accomplishments: newline-separated bullet points starting with '• '. "
        "blockers: newline-separated bullet points starting with '• ', or empty "
        "string if none.\n\n"
        f"Activities:\n{activity_block}"
    )


def _validate_response(raw: Any) -> WorkSummary:
    """Validate the parsed JSON dict into a WorkSummary.

    We require all four keys to be present and coerce them to strings. If a
    key is missing or the top-level value is not a dict, we raise
    AIServiceError so the caller can fall back or retry.
    """
    if not isinstance(raw, dict):
        raise AIServiceError("AI response was not a JSON object.")

    required = ("title", "summary", "accomplishments", "blockers")
    missing = [k for k in required if k not in raw]
    if missing:
        raise AIServiceError(f"AI response missing keys: {', '.join(missing)}.")

    return WorkSummary(
        title=str(raw["title"]).strip()[:120],
        summary=str(raw["summary"]).strip(),
        accomplishments=str(raw["accomplishments"]).strip(),
        blockers=str(raw["blockers"]).strip(),
    )


def _llm_summary(activities: list[WorkActivity]) -> WorkSummary:
    """Call the Google Gemini generateContent API and return a validated summary.

    API request occurs here via httpx.post to the Gemini REST endpoint. The
    request includes the model name in the URL, the API key as a query
    parameter, and the prompt text inside the `contents` array per Google's
    schema. We also pass a generationConfig asking for a low temperature.

    On any failure (network, HTTP error, malformed JSON, schema mismatch)
    we raise AIServiceError. The caller (UI) catches it, shows a friendly
    message, preserves the activity list, and lets the user retry — no
    draft data is lost.
    """
    url = _API_URL.format(model=_MODEL)
    params = {"key": settings.gemini_api_key}
    payload = {
        "contents": [
            {"parts": [{"text": _build_prompt(activities)}]}
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 600,
            "responseMimeType": "application/json",
        },
    }

    try:
        # --- API request occurs here ---
        response = httpx.post(url, json=payload, params=params, timeout=_TIMEOUT)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise AIServiceError(f"The AI service returned an error (HTTP {exc.response.status_code}).") from exc
    except httpx.HTTPError as exc:
        raise AIServiceError("Could not reach the AI service. Check your connection and try again.") from exc

    try:
        body = response.json()
        # Gemini returns candidates[].content.parts[].text
        content = body["candidates"][0]["content"]["parts"][0]["text"]
        # --- Structured output is parsed and validated here ---
        parsed = json.loads(content)
    except (KeyError, IndexError, json.JSONDecodeError) as exc:
        raise AIServiceError("The AI service returned an unexpected response format.") from exc

    return _validate_response(parsed)


# ---------------------------------------------------------------------------
# Back-compat stub kept for any external caller that imported it.
# ---------------------------------------------------------------------------

def generate_with_llm(activities: list[WorkActivity]) -> WorkSummary:
    """Generate a summary using the configured LLM provider.

    Raises AIServiceError on failure so the caller can show a friendly
    message and allow retry without losing data.
    """
    if not settings.gemini_api_key:
        raise AIServiceError("No AI provider is configured. Set GEMINI_API_KEY to enable AI summaries.")
    return _llm_summary(activities)
