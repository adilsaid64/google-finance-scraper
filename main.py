import requests as r
from bs4 import BeautifulSoup

def fetch_html(url):
    '''Fetch HTML content.'''
    resp = r.get(url)
    return resp.content

def parse_html_for_price_info(html_content):
    '''Gets Price Information from the HTML content.'''
    soup = BeautifulSoup(html_content, 'html.parser')
    # we want to target the div that has the data we want. which is 'data-last-price'
    # get the first div that has the data-last-price attribute. True means, this attribute is set to some value.
    price_div = soup.find('div', attrs={'data-last-price':True}) 
    return price_div

def get_currency_conversion(from_currency, to_currency):
    """Converts currency from one to another."""
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
        'to_USD': get_currency_conversion(price_div['data-currency-code'], 'USD')
    }

if __name__ == '__main__':
    print(get_price_information('TSLA', 'NASDAQ'))