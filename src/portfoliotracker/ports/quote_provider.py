from typing import Protocol

from portfoliotracker.domain.models import Quote, StockRef


class QuoteProvider(Protocol):
    """Fetches a quote for a symbol. Implemented by HTTP/scraping adapters."""

    def get_quote(self, stock: StockRef) -> Quote:
        ...
