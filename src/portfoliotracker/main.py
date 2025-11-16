import sqlite3
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Optional, Union

import requests as r
from bs4 import BeautifulSoup, Tag
from tabulate import tabulate

conn: sqlite3.Connection = sqlite3.connect("positions.db")
c: sqlite3.Cursor = conn.cursor()

c.execute(
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
)"""
)


@dataclass
class Stock:
    ticker: str
    exchange: str
    price: float = 0.0
    currency: str = "USD"
    usd_price: float = 0.0
    timestamp: int = 0

    def __post_init__(self) -> None:
        price_info: dict[str, Any] = get_price_information(self.ticker, self.exchange)

        if price_info["ticker"] == self.ticker:
            self.price = price_info["price"]
            self.currency = price_info["currency"]
            self.timestamp = price_info["timestamp"]
            self.usd_price = price_info["to_USD"]


@dataclass
class Position:
    stock: Stock
    quantity: int


@dataclass
class Portfolio:
    positions: Sequence[Position]

    def get_total_value(self) -> float:
        total_value: float = 0.0
        for position in self.positions:
            total_value += position.quantity * position.stock.usd_price
        return total_value


def fetch_html(url: str) -> bytes:
    """Fetch HTML content."""
    resp = r.get(url)
    return resp.content


def parse_html_for_price_info(html_content: bytes) -> Optional[Tag]:
    """Gets Price Information from the HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    price_div: Optional[Tag] = soup.find("div", attrs={"data-last-price": True})
    return price_div


def get_currency_conversion(from_currency: str, to_currency: str) -> Optional[float]:
    """Converts currency from one to another."""
    if from_currency == to_currency:
        return None
    url = f"https://www.google.com/finance/quote/{from_currency.upper()}-{to_currency.upper()}"
    html_content = fetch_html(url)
    price_div = parse_html_for_price_info(html_content)
    if price_div is not None:
        return float(price_div["data-last-price"])
    else:
        return None


def get_price_information(ticker: str, exchange: str) -> dict[str, Any]:
    """Gets price information for a given ticker and exchange."""
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    html_content = fetch_html(url)
    price_div = parse_html_for_price_info(html_content)

    if price_div is None:
        raise ValueError(f"No price information found for {ticker}:{exchange}")

    currency: str = price_div["data-currency-code"]

    return {
        "ticker": ticker,
        "exchange": exchange,
        "price": float(price_div["data-last-price"]),
        "timestamp": int(price_div["data-last-normal-market-timestamp"]),
        "currency": currency,
        "to_USD": get_currency_conversion(currency, "USD")
        if currency != "USD"
        else float(price_div["data-last-price"]),
    }


def display_portfolio_summary(portfolio: Portfolio) -> None:
    if not isinstance(portfolio, Portfolio):
        raise TypeError("Provide an instance of the Portfolio type.")

    portfolio_value: float = portfolio.get_total_value()

    position_data: list[list[Union[float, int, str]]] = []

    for position in portfolio.positions:
        total_usd: float = position.stock.usd_price * position.quantity
        pct: float = 100 * total_usd / portfolio_value

        data: list[Union[float, int, str]] = [
            position.stock.ticker,
            position.stock.exchange,
            position.stock.currency,
            position.quantity,
            position.stock.usd_price,
            total_usd,
            pct,
            position.stock.timestamp,
        ]

        position_data.append(data)

        c.execute(
            """INSERT INTO positions
               (ticker, exchange, currency, quantity, usd_price, total_usd_price, precentage, date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
            ),
        )

    conn.commit()
    conn.close()

    print(
        tabulate(
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
    )

    print("Total Portfolio: ", portfolio_value)
