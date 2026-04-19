from typing import Protocol

from portfoliotracker.domain.models import Position


class PositionsSource(Protocol):
    """Loads portfolio positions from config or storage."""

    def load_positions(self) -> tuple[Position, ...]:
        ...
