# Google-Finance-Scraper

A simple scraping project that scrapes real-time stock data from Google Finance using *BeautifulSoup*. Data structuring is done through the use of *dataclasses*. The script calculates portfolio valuation and stores data into a SQLite database using *sqlite3* for future analysis.

# Features
- **Real-Time Price Updates**: The script fetches the latest prices from Google Finance.
- **Currency Conversion**: The script standardizes all prices to USD. This allows portfolios to be evaluated more easily regardless of the original stock currency.
- **SQLite Database Integration**: Stores portfolio information in a SQLite database for future analysis of historical data. Using SQLite databases is also a more scalable alternative to traditional methods like csv.