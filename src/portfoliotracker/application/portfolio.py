from collections.abc import Sequence

from portfoliotracker.domain.models import (
    PortfolioSnapshot,
    Position,
    Quote,
    QuotedPosition,
    StockRef,
)
from portfoliotracker.ports.quote_provider import QuoteProvider


def build_snapshot(
    positions: Sequence[Position],
    provider: QuoteProvider,
) -> PortfolioSnapshot:
    rows: list[QuotedPosition] = []
    for pos in positions:
        q = provider.get_quote(pos.stock)
        rows.append(QuotedPosition(stock=pos.stock, quantity=pos.quantity, quote=q))
    return PortfolioSnapshot.from_quoted(rows)


def quote_single(provider: QuoteProvider, stock: StockRef) -> Quote:
    return provider.get_quote(stock)
