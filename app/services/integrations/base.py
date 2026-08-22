"""The small contract every activity integration follows."""

from abc import ABC, abstractmethod

from app.models.work_activity import WorkActivity


class Integration(ABC):
    """Base interface for a source that produces normalized activities."""

    source: str

    @abstractmethod
    def fetch_activities(self, user_id: int) -> list[WorkActivity]:
        """Return activity records for one user."""
        raise NotImplementedError