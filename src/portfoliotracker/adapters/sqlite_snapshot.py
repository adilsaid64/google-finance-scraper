"""SQLite persistence for portfolio snapshots — implements SnapshotSink."""

from __future__ import annotations

import sqlite3

from portfoliotracker.domain.models import PortfolioSnapshot


class SqliteSnapshotSink:
    """Stores one row per position per run (legacy schema: `precentage` column name)."""

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def save(self, snapshot: PortfolioSnapshot) -> None:
        conn = sqlite3.connect(self._db_path)
        try:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS positions(
                    id INTEGER PRIMARY KEY,
                    ticker TEXT,
                    exchange TEXT,
                    currency TEXT,
                    quantity INTEGER,
                    usd_price FLOAT,
                    total_usd_price FLOAT,
                    precentage FLOAT,
                    date INTEGER
                )
                """
            )
            for row in snapshot.rows:
                q = row.quote
                total_usd = row.line_value_usd()
                pct = snapshot.weight_percent(row)
                cur.execute(
                    """
                    INSERT INTO positions
                    (ticker, exchange, currency, quantity, usd_price,
                     total_usd_price, precentage, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        q.ticker,
                        q.exchange,
                        q.currency,
                        row.quantity,
                        q.usd_price,
                        total_usd,
                        pct,
                        q.timestamp,
                    ),
                )
            conn.commit()
        finally:
            conn.close()
