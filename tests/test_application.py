from portfoliotracker.application.portfolio import build_snapshot
from portfoliotracker.domain.models import Position, Quote, StockRef
from portfoliotracker.ports.quote_provider import QuoteProvider


class FakeQuoteProvider:
    def __init__(self) -> None:
        self._q = {
            ("AAA", "NASDAQ"): Quote("AAA", "NASDAQ", 100.0, "USD", 100.0, 1),
            ("BBB", "NYSE"): Quote("BBB", "NYSE", 50.0, "USD", 50.0, 2),
        }

    def get_quote(self, stock: StockRef) -> Quote:
        key = (stock.ticker, stock.exchange)
        return self._q[key]


def test_build_snapshot_uses_provider() -> None:
    positions = (
        Position(StockRef("AAA", "NASDAQ"), 2),
        Position(StockRef("BBB", "NYSE"), 1),
    )
    provider: QuoteProvider = FakeQuoteProvider()
    snap = build_snapshot(positions, provider)
    assert snap.total_usd == 250.0
    assert len(snap.rows) == 2
    assert snap.rows[0].quote.usd_price == 100.0
