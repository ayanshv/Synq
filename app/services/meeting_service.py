"""Meeting service.

Decides whether a meeting seems necessary based on the team's published
updates and goal status. This is intentionally a simple heuristic for the
MVP; the point is to give teams a nudge, not a hard rule.

Current heuristic:
    If any goal is "off_track" or "at_risk" OR any update reports blockers,
    suggest a meeting. Otherwise suggest async.
"""

from app.services.update_service import list_published_for_team
from app.services.goal_service import list_goals_for_team


def should_meet(team_id: int) -> tuple[bool, str]:
    """Return (is_meeting_needed, reason).

    Keeping the return a simple tuple makes this easy to call from the UI
    without introducing a dedicated data class for the MVP.
    """
    goals = list_goals_for_team(team_id)
    updates = list_published_for_team(team_id)

    at_risk = [g for g in goals if g.status in ("at_risk", "off_track")]
    if at_risk:
        titles = ", ".join(g.title for g in at_risk)
        return True, f"Goals need attention: {titles}."

    for update in updates:
        if update.blockers.strip():
            return True, "A team member reported blockers."

    return False, "Team is on track; async updates are enough."
