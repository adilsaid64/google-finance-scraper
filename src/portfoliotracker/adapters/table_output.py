"""Render portfolio snapshots as text tables or JSON (CLI / library output)."""

from __future__ import annotations

import json
from typing import Any

from tabulate import tabulate

from portfoliotracker.domain.models import PortfolioSnapshot


def format_table(snapshot: PortfolioSnapshot) -> str:
    position_data: list[list[float | int | str]] = []
    for row in snapshot.rows:
        q = row.quote
        total_usd = row.line_value_usd()
        pct = snapshot.weight_percent(row)
        position_data.append(
            [
                q.ticker,
                q.exchange,
                q.currency,
                row.quantity,
                q.usd_price,
                total_usd,
                pct,
                q.timestamp,
            ]
        )
    table = tabulate(
        position_data,
        headers=[
            "Ticker",
            "Exchange",
            "Currency",
            "Quantity",
            "USD price",
            "Total USD Value",
            "% of Portfolio",
            "Time",
        ],
        tablefmt="psql",
        floatfmt=".3f",
    )
    return f"{table}\n\nTotal Portfolio: {snapshot.total_usd:.3f}\n"


def snapshot_to_json_dict(snapshot: PortfolioSnapshot) -> dict[str, Any]:
    rows_out: list[dict[str, Any]] = []
    for row in snapshot.rows:
        q = row.quote
        rows_out.append(
            {
                "ticker": q.ticker,
                "exchange": q.exchange,
                "currency": q.currency,
                "quantity": row.quantity,
                "usd_price": q.usd_price,
                "native_price": q.price,
                "total_usd": row.line_value_usd(),
                "percent_of_portfolio": snapshot.weight_percent(row),
                "timestamp": q.timestamp,
            }
        )
    return {
        "total_usd": snapshot.total_usd,
        "positions": rows_out,
    }


def format_json(snapshot: PortfolioSnapshot) -> str:
    return json.dumps(snapshot_to_json_dict(snapshot), indent=2) + "\n"
