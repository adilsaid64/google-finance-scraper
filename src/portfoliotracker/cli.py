"""Command-line entry point: `portfoliotracker`."""

from __future__ import annotations

import argparse
import sys

from portfoliotracker.adapters.google_finance import GoogleFinanceQuoteProvider
from portfoliotracker.adapters.json_positions import JsonFilePositionsSource
from portfoliotracker.adapters.sqlite_snapshot import SqliteSnapshotSink
from portfoliotracker.adapters.table_output import format_json, format_table
from portfoliotracker.application.portfolio import build_snapshot, quote_single
from portfoliotracker.domain.models import StockRef


def _cmd_show(args: argparse.Namespace) -> int:
    source = JsonFilePositionsSource(args.config)
    positions = source.load_positions()
    quotes = GoogleFinanceQuoteProvider(timeout_s=args.timeout)
    snapshot = build_snapshot(positions, quotes)
    if args.format == "json":
        sys.stdout.write(format_json(snapshot))
    else:
        sys.stdout.write(format_table(snapshot))
    if not args.no_save:
        SqliteSnapshotSink(args.db).save(snapshot)
    return 0


def _cmd_quote(args: argparse.Namespace) -> int:
    quotes = GoogleFinanceQuoteProvider(timeout_s=args.timeout)
    q = quote_single(quotes, StockRef(args.ticker, args.exchange))
    if args.format == "json":
        import json

        sys.stdout.write(
            json.dumps(
                {
                    "ticker": q.ticker,
                    "exchange": q.exchange,
                    "price": q.price,
                    "currency": q.currency,
                    "usd_price": q.usd_price,
                    "timestamp": q.timestamp,
                },
                indent=2,
            )
            + "\n"
        )
    else:
        sys.stdout.write(
            f"{q.ticker}:{q.exchange}  {q.price} {q.currency}  "
            f"(USD {q.usd_price:.4f})  t={q.timestamp}\n"
        )
    return 0


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="portfoliotracker",
        description="Portfolio quotes via Google Finance (scraping).",
    )
    sub = p.add_subparsers(dest="command", required=True)

    show = sub.add_parser("show", help="Load positions from JSON and print a summary")
    show.add_argument(
        "--config",
        "-c",
        default="positions.json",
        help="Path to JSON config (default: positions.json)",
    )
    show.add_argument(
        "--db",
        default="positions.db",
        help="SQLite file for snapshot history (default: positions.db)",
    )
    show.add_argument(
        "--no-save",
        action="store_true",
        help="Do not write rows to SQLite",
    )
    show.add_argument(
        "--format",
        choices=("table", "json"),
        default="table",
        help="Output format",
    )
    show.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds",
    )
    show.set_defaults(func=_cmd_show)

    quote = sub.add_parser("quote", help="Fetch a single quote")
    quote.add_argument("ticker", help="Ticker symbol, e.g. AAPL")
    quote.add_argument("exchange", help="Exchange code, e.g. NASDAQ")
    quote.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )
    quote.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds",
    )
    quote.set_defaults(func=_cmd_quote)

    return p


def run(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    # Allow: portfoliotracker path/to.json as shorthand for `show -c path/to.json`
    if len(argv) == 1 and argv[0].endswith(".json"):
        ns = argparse.Namespace(
            config=argv[0],
            db="positions.db",
            no_save=False,
            format="table",
            timeout=30.0,
        )
        return _cmd_show(ns)

    args = _build_parser().parse_args(argv)
    return int(args.func(args))


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
