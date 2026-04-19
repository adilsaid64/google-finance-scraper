import json
from pathlib import Path

from portfoliotracker.adapters.json_positions import JsonFilePositionsSource


def test_parse_positions_payload(tmp_path: Path) -> None:
    p = tmp_path / "c.json"
    p.write_text(
        json.dumps(
            {
                "positions": [
                    {"ticker": "A", "exchange": "NASDAQ", "quantity": 3},
                    {"ticker": "X", "exchange": "TSE", "quantity": 1},
                ]
            }
        ),
        encoding="utf-8",
    )
    src = JsonFilePositionsSource(p)
    rows = src.load_positions()
    assert len(rows) == 2
    assert rows[0].stock.ticker == "A"
    assert rows[0].quantity == 3
    assert rows[1].stock.exchange == "TSE"
