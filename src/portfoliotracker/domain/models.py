from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class StockRef:
    """Identifies a listed instrument (ticker + exchange)."""

    ticker: str
    exchange: str


@dataclass(frozen=True)
class Position:
    """A held quantity of a stock; no market data."""

    stock: StockRef
    quantity: int


@dataclass(frozen=True)
class Quote:
    """A point-in-time quote in native currency and USD."""

    ticker: str
    exchange: str
    price: float
    currency: str
    usd_price: float
    timestamp: int


@dataclass(frozen=True)
class QuotedPosition:
    """Position with an attached quote."""

    stock: StockRef
    quantity: int
    quote: Quote

    def line_value_usd(self) -> float:
        return float(self.quantity) * self.quote.usd_price


@dataclass(frozen=True, init=False)
class Portfolio:
    """A set of positions (identifiers + quantities only)."""

    positions: tuple[Position, ...]

    def __init__(self, positions: Sequence[Position]) -> None:
        object.__setattr__(self, "positions", tuple(positions))


@dataclass(frozen=True)
class PortfolioSnapshot:
    """All positions with quotes and aggregate total in USD."""

    rows: tuple[QuotedPosition, ...]
    total_usd: float

    @staticmethod
    def from_quoted(rows: Sequence[QuotedPosition]) -> PortfolioSnapshot:
        total = sum(r.line_value_usd() for r in rows)
        return PortfolioSnapshot(rows=tuple(rows), total_usd=total)

    def weight_percent(self, row: QuotedPosition) -> float:
        if self.total_usd <= 0:
            return 0.0
        return 100.0 * row.line_value_usd() / self.total_usd
