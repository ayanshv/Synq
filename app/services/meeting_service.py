"""Explainable meeting suggestions for a team.

This is intentionally a small rules engine, not an AI decision-maker. Each
rule is visible below so the suggestion can be studied and changed safely.
"""

from dataclasses import dataclass
from datetime import date, timedelta
import re

from sqlmodel import select

from app.database import get_session
from app.models import Goal, Team, User, WorkUpdate


@dataclass(frozen=True)
class MeetingSuggestion:
    """The assistant's recommendation and the explanation behind it."""

    recommendation: str
    reason: str
    confidence: float


def recommend_meeting(team: Team) -> MeetingSuggestion:
    """Return a deterministic meeting suggestion for one team.

    Rules:
    - Recent coverage means a published update in the last seven days.
    - A blocker is significant when it contains useful text, rather than
      phrases such as "No blockers".
    - At-risk and off-track goals are treated as stalled for this MVP.
    - Two similar blocker reports indicate a shared unresolved issue.
    - A meeting is recommended when any of those risks is present, or when
      fewer than half of the team has recent published coverage.
    - Otherwise, the assistant recommends continuing asynchronously.

    The confidence is only a rough explanation of how much evidence the
    simple rules found. It is not a probability or an automatic decision.
    """
    if team.id is None:
        return MeetingSuggestion(
            "Meeting recommended",
            "This team has not been saved yet, so there is not enough shared data to assess progress.",
            0.35,
        )

    with get_session() as session:
        users = list(session.exec(select(User).where(User.team_id == team.id)))
        updates = list(
            session.exec(
                select(WorkUpdate)
                .where(WorkUpdate.team_id == team.id)
                .where(WorkUpdate.published == True)  # noqa: E712
            )
        )
        goals = list(session.exec(select(Goal).where(Goal.team_id == team.id)))

    recent_start = date.today() - timedelta(days=7)
    recent_updates = [update for update in updates if update.date >= recent_start]
    recent_members = {update.user_id for update in recent_updates}
    coverage = len(recent_members) / len(users) if users else 0
    blockers = [
        update.blockers.strip()
        for update in recent_updates
        if _is_significant_blocker(update.blockers)
    ]
    stalled_goals = [
        goal for goal in goals if goal.status in {"at_risk", "off_track"}
    ]
    shared_issue = _shared_issue(blockers)

    # Shared blockers are the strongest signal: synchronous discussion can
    # unblock several people at once.
    if shared_issue:
        return MeetingSuggestion(
            "Meeting recommended",
            f"Multiple team members reported blockers related to {shared_issue}.",
            0.92,
        )

    # Several independent blockers still justify a conversation, even when
    # they do not share the same wording.
    if len(blockers) >= 2:
        return MeetingSuggestion(
            "Meeting recommended",
            f"{len(blockers)} team members reported unresolved blockers.",
            0.84,
        )

    # At-risk or off-track goals are the MVP's understandable definition of
    # a stalled goal.
    if stalled_goals:
        titles = ", ".join(goal.title for goal in stalled_goals)
        return MeetingSuggestion(
            "Meeting recommended",
            f"These goals may need synchronous attention: {titles}.",
            0.78,
        )

    # Low recent coverage means the team does not yet have enough async
    # context to confidently skip a conversation.
    if users and coverage < 0.5:
        return MeetingSuggestion(
            "Meeting recommended",
            f"Only {len(recent_members)} of {len(users)} team members have recent published updates.",
            0.68,
        )

    member_phrase = (
        f"All {len(users)} team members"
        if len(recent_members) == len(users) and users
        else f"{len(recent_members)} of {len(users)} team members"
    )
    return MeetingSuggestion(
        "No meeting needed",
        f"{member_phrase} have recent updates, the active goals are progressing, "
        "and no unresolved blockers were reported.",
        0.88,
    )


def _is_significant_blocker(text: str) -> bool:
    """Ignore empty blocker fields and reassuring 'none' statements."""
    normalized = text.strip().lower()
    return bool(normalized) and normalized not in {
        "none",
        "no blockers",
        "no blockers reported.",
    }


def _shared_issue(blockers: list[str]) -> str | None:
    """Find a small shared phrase in two blocker reports."""
    if len(blockers) < 2:
        return None

    stop_words = {"about", "blocked", "blocker", "from", "need", "the", "with"}
    first_words = set(re.findall(r"[a-z0-9]+", blockers[0].lower())) - stop_words
    for blocker in blockers[1:]:
        common = first_words & (set(re.findall(r"[a-z0-9]+", blocker.lower())) - stop_words)
        if common:
            return "the same issue (" + ", ".join(sorted(common)[:3]) + ")"
    return None