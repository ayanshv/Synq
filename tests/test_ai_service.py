"""Tests for structured AI summary validation.

These tests do not call an external model. They check that invalid payloads
are rejected before anything would be saved.
"""

import pytest

from app.services.ai_service import AISummaryError, work_summary_from_payload


def test_valid_payload_becomes_work_summary():
    summary = work_summary_from_payload(
        {
            "title": "Billing retry fix",
            "summary": "Shipped the retry path.",
            "accomplishments": "• Merged the fix",
            "blockers": "",
        }
    )
    assert summary.title == "Billing retry fix"
    assert "retry" in summary.summary
    assert summary.blockers == ""


def test_list_accomplishments_are_joined():
    summary = work_summary_from_payload(
        {
            "title": "Today",
            "summary": "Made progress.",
            "accomplishments": ["Merged PR", "Wrote tests"],
            "blockers": ["Waiting on review"],
        }
    )
    assert "• Merged PR" in summary.accomplishments
    assert "• Waiting on review" in summary.blockers


def test_missing_field_is_rejected():
    with pytest.raises(AISummaryError):
        work_summary_from_payload({"title": "Only a title"})


def test_empty_title_is_rejected():
    with pytest.raises(AISummaryError):
        work_summary_from_payload(
            {
                "title": "  ",
                "summary": "Text",
                "accomplishments": "",
                "blockers": "",
            }
        )


def test_non_object_payload_is_rejected():
    with pytest.raises(AISummaryError):
        work_summary_from_payload(["not", "an", "object"])
