import requests as r
from bs4 import BeautifulSoup
from dataclasses import dataclass
from tabulate import tabulate
from datetime import datetime

@dataclass
class Stock:
    ticker:str
    exchange:str
    price:float=0
    currency:str = 'USD'
    usd_price:float=0
    timestamp :int = 0

    def __post_init__(self):
        price_info = get_price_information(self.ticker, self.exchange)

        if price_info['ticker']== self.ticker:
            self.price = price_info['price']
            self.currency = price_info['currency']
            self.timestamp = price_info['timestamp']
            self.usd_price = price_info['to_USD']
@dataclass
class Position:
    stock:Stock
    quantity:int

@dataclass
class Portfolio:
    positions : list[Position]


    def get_total_value(self):
        total_value = 0
        for position in self.positions:
            total_value += position.quantity * position.stock.usd_price # get value in usd.

        return total_value

def fetch_html(url):
    """Fetch HTML content."""
    resp = r.get(url)
    return resp.content

def parse_html_for_price_info(html_content):
    """Gets Price Information from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    # we want to target the div that has the data we want. which is 'data-last-price'
    # get the first div that has the data-last-price attribute. True means, this attribute is set to some value.
    price_div = soup.find('div', attrs={'data-last-price':True}) 
    return price_div

def get_currency_conversion(from_currency, to_currency):
    """Converts currency from one to another."""
    if from_currency==to_currency:
        return None
    url = f'https://www.google.com/finance/quote/{from_currency.upper()}-{to_currency.upper()}'
    html_content = fetch_html(url)
    price_div = parse_html_for_price_info(html_content)
    if price_div is not None:
        return float(price_div['data-last-price'])
    else: return None

def get_price_information(ticker, exchange):
    """Gets price information for a given ticker and exchange."""
    url = f'https://www.google.com/finance/quote/{ticker}:{exchange}'
    html_content = fetch_html(url)
    price_div = parse_html_for_price_info(html_content)
    return {
        'ticker': ticker,
        'exchange': exchange,
        'price': float(price_div['data-last-price']),
        'timestamp': int(price_div['data-last-normal-market-timestamp']),
        'currency': price_div['data-currency-code'],
        'to_USD': get_currency_conversion(price_div['data-currency-code'], 'USD') if price_div['data-currency-code']!='USD' else float(price_div['data-last-price'])
    }

def display_portfolio_summary(portfolio):
    if not isinstance(portfolio, Portfolio):
        raise TypeError('Provide an instance of the Portfolio type.')
    
    portfolio_value = portfolio.get_total_value()

    position_data = []

    for position in portfolio.positions:
        position_data.append([
            position.stock.ticker,
            position.stock.exchange,
            position.stock.currency,
            position.quantity,
            position.stock.usd_price,
            position.stock.usd_price * position.quantity,
            100*position.stock.usd_price * position.quantity/portfolio_value,
            datetime.fromtimestamp(position.stock.timestamp)
            
        ])

    print(tabulate(position_data, 
                   headers=['Ticker', 'Exchange', 'Currency', 'Quantity', 'USD price', 'Total USD Value', '% of Portfolio', 'Time'], 
                   tablefmt='psql',
                   floatfmt='.3f'
                   ))
    
    print('Total Portfolio: ', portfolio_value)


if __name__ == '__main__':    
    shop = Stock('SHOP', 'TSE')
    google = Stock('GOOGL', 'NASDAQ')
    msft = Stock('MSFT', 'NASDAQ') 
    baba = Stock('BABA', 'NYSE') 
    apple = Stock('AAPL', 'NASDAQ')    
    tesla = Stock('TSLA', 'NASDAQ')    

    portfolio = Portfolio([Position(shop, 10), Position(google, 20), Position(apple, 20), Position(tesla, 10), Position(msft, 23), Position(baba, 9)])
#    
    display_portfolio_summary(portfolio)