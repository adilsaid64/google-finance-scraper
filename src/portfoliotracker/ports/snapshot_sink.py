from typing import Protocol

from portfoliotracker.domain.models import PortfolioSnapshot


class SnapshotSink(Protocol):
    """Persists a snapshot (e.g. SQLite history). Optional for read-only flows."""

    def save(self, snapshot: PortfolioSnapshot) -> None:
        ...
