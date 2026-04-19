from portfoliotracker.domain.models import (
    PortfolioSnapshot,
    Position,
    Quote,
    QuotedPosition,
    StockRef,
)


def test_portfolio_snapshot_total_and_weights() -> None:
    a = StockRef("AAA", "NASDAQ")
    b = StockRef("BBB", "NYSE")
    q1 = Quote("AAA", "NASDAQ", 10.0, "USD", 10.0, 1)
    q2 = Quote("BBB", "NYSE", 20.0, "USD", 20.0, 2)
    rows = (
        QuotedPosition(a, 2, q1),
        QuotedPosition(b, 1, q2),
    )
    snap = PortfolioSnapshot.from_quoted(rows)
    assert snap.total_usd == 40.0
    assert snap.weight_percent(snap.rows[0]) == 50.0
    assert snap.weight_percent(snap.rows[1]) == 50.0


def test_weight_zero_total() -> None:
    a = StockRef("X", "NASDAQ")
    q = Quote("X", "NASDAQ", 0.0, "USD", 0.0, 0)
    snap = PortfolioSnapshot.from_quoted((QuotedPosition(a, 0, q),))
    assert snap.total_usd == 0.0
    assert snap.weight_percent(snap.rows[0]) == 0.0


def test_position_tuple_from_portfolio() -> None:
    p = Position(StockRef("A", "NASDAQ"), 5)
    assert p.stock.ticker == "A"
    assert p.quantity == 5
