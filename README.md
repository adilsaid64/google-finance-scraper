# PortfolioTracker

A portfolio tracking project that tracks your portfolio

## Installation

```bash
pip install portfoliotracker
```

## Usage

```python
from portfoliotracker import Portfolio, Position, Stock, display_portfolio_summary

shop = Stock("SHOP", "TSE")
google = Stock("GOOGL", "NASDAQ")
msft = Stock("MSFT", "NASDAQ")
baba = Stock("BABA", "NYSE")
apple = Stock("AAPL", "NASDAQ")
tesla = Stock("TSLA", "NASDAQ")

portfolio = Portfolio(
    [
        Position(shop, 10),
        Position(google, 20),
        Position(apple, 20),
        Position(tesla, 10),
        Position(msft, 23),
        Position(baba, 9),
    ]
)

display_portfolio_summary(portfolio)
```

## License

Apache-2.0 License.
