"""Portfolio quotes and summaries (domain + ports; I/O in adapters)."""

from __future__ import annotations

from portfoliotracker.application.portfolio import build_snapshot
from portfoliotracker.domain.models import (
    Portfolio,
    PortfolioSnapshot,
    Position,
    Quote,
    QuotedPosition,
    StockRef,
)
from portfoliotracker.ports.quote_provider import QuoteProvider

__version__ = "1.1.0"

# Backward-compatible alias: previously `Stock(ticker, exchange)` triggered fetch.
Stock = StockRef

__all__ = [
    "Portfolio",
    "PortfolioSnapshot",
    "Position",
    "Quote",
    "QuoteProvider",
    "QuotedPosition",
    "Stock",
    "StockRef",
    "build_snapshot",
    "display_portfolio_summary",
]


def display_portfolio_summary(
    portfolio: Portfolio,
    *,
    quote_provider: QuoteProvider | None = None,
    db_path: str | None = "positions.db",
) -> None:
    """Print a tabulated summary and optionally persist rows to SQLite."""
    from portfoliotracker.adapters.google_finance import GoogleFinanceQuoteProvider
    from portfoliotracker.adapters.sqlite_snapshot import SqliteSnapshotSink
    from portfoliotracker.adapters.table_output import format_table

    qp = quote_provider or GoogleFinanceQuoteProvider()
    snapshot = build_snapshot(portfolio.positions, qp)
    print(format_table(snapshot), end="")
    if db_path is not None:
        SqliteSnapshotSink(db_path).save(snapshot)
