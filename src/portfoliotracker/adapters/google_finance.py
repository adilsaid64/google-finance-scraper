"""Google Finance HTML scraping — implements QuoteProvider."""

from __future__ import annotations

from typing import TypedDict, cast

import requests
from bs4 import BeautifulSoup, Tag

from portfoliotracker.domain.models import Quote, StockRef


def _tag_attr_float(tag: Tag, name: str) -> float:
    return float(str(tag[name]))


def _tag_attr_int(tag: Tag, name: str) -> int:
    return int(str(tag[name]))


def _tag_attr_str(tag: Tag, name: str) -> str:
    return str(tag[name])


class _PriceInformation(TypedDict):
    ticker: str
    exchange: str
    price: float
    currency: str
    timestamp: int
    to_USD: float


class GoogleFinanceQuoteProvider:
    """Fetches quotes from Google Finance public quote pages."""

    def __init__(
        self,
        *,
        session: requests.Session | None = None,
        timeout_s: float = 30.0,
    ) -> None:
        self._session = session or requests.Session()
        self._timeout_s = timeout_s

    def get_quote(self, stock: StockRef) -> Quote:
        info = self._fetch_price_information(stock.ticker, stock.exchange)
        return Quote(
            ticker=info["ticker"],
            exchange=info["exchange"],
            price=info["price"],
            currency=info["currency"],
            usd_price=info["to_USD"],
            timestamp=info["timestamp"],
        )

    def _fetch_html(self, url: str) -> bytes:
        resp = self._session.get(url, timeout=self._timeout_s)
        resp.raise_for_status()
        return cast(bytes, resp.content)

    @staticmethod
    def _parse_price_div(html_content: bytes) -> Tag | None:
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.find("div", attrs={"data-last-price": True})

    def _get_currency_conversion(
        self, from_currency: str, to_currency: str
    ) -> float | None:
        if from_currency == to_currency:
            return None
        url = (
            "https://www.google.com/finance/quote/"
            f"{from_currency.upper()}-{to_currency.upper()}"
        )
        html_content = self._fetch_html(url)
        price_div = self._parse_price_div(html_content)
        if price_div is not None:
            return _tag_attr_float(price_div, "data-last-price")
        return None

    def _fetch_price_information(self, ticker: str, exchange: str) -> _PriceInformation:
        url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
        html_content = self._fetch_html(url)
        price_div = self._parse_price_div(html_content)

        if price_div is None:
            raise ValueError(f"No price information found for {ticker}:{exchange}")

        currency = _tag_attr_str(price_div, "data-currency-code")
        price = _tag_attr_float(price_div, "data-last-price")
        timestamp = _tag_attr_int(price_div, "data-last-normal-market-timestamp")

        to_usd: float
        if currency != "USD":
            conv = self._get_currency_conversion(currency, "USD")
            if conv is None:
                raise ValueError(
                    f"Could not convert {currency} to USD for {ticker}:{exchange}"
                )
            to_usd = price * conv
        else:
            to_usd = price

        result: _PriceInformation = {
            "ticker": ticker,
            "exchange": exchange,
            "price": price,
            "timestamp": timestamp,
            "currency": currency,
            "to_USD": to_usd,
        }
        return result
