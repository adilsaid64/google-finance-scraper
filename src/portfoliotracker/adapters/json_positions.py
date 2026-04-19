"""Load positions from JSON config files — implements PositionsSource."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from portfoliotracker.domain.models import Position, StockRef


def _parse_positions_payload(data: Any) -> tuple[Position, ...]:
    if not isinstance(data, dict):
        raise ValueError("Root JSON must be an object")
    raw = data.get("positions")
    if not isinstance(raw, list):
        raise ValueError('JSON must contain a "positions" array')
    out: list[Position] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"positions[{i}] must be an object")
        ticker = item.get("ticker")
        exchange = item.get("exchange")
        quantity = item.get("quantity")
        if not isinstance(ticker, str) or not isinstance(exchange, str):
            raise ValueError(f'positions[{i}] needs string "ticker" and "exchange"')
        if not isinstance(quantity, int):
            raise ValueError(f'positions[{i}] "quantity" must be an integer')
        out.append(Position(StockRef(ticker=ticker, exchange=exchange), quantity))
    return tuple(out)


class JsonFilePositionsSource:
    """Reads `{"positions": [{"ticker","exchange","quantity"}, ...]}`."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def load_positions(self) -> tuple[Position, ...]:
        text = self._path.read_text(encoding="utf-8")
        data = json.loads(text)
        return _parse_positions_payload(data)
