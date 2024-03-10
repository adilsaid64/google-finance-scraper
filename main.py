import requests as r
from bs4 import BeautifulSoup

# https://www.google.com/finance/quote/TSLA:NASDAQ]

def parse_request(url):
    resp = r.get(url)
    print(resp.status_code)
    soup = BeautifulSoup(resp.content, 'html.parser')
    return soup


def convert_currency(cur1, cur2):
    url = f'https://www.google.com/finance/quote/{cur1.upper()}-{cur2.upper()}'
    soup = parse_request(url)

    price_div = soup.find('div', attrs={'data-last-price':True})
    print(price_div)
    # return {'cur1':cur1, 
    #         'cur2':cur2,
    #         'conversion':float(price_div['data-last-price'])}
    

def get_price_information(ticker, exchange):
    url = f'https://www.google.com/finance/quote/{ticker}:{exchange}'
    soup = parse_request(url)

    # we want to target the div that has the data we want. which is 'data-last-price'
    price_div = soup.find('div', attrs={'data-last-price':True}) # get the first div that has the data-last-price attribute. True means, this attribute is set to some value.
    
    return {'ticker':ticker, 
            'exchange':exchange, 
            'price' : float(price_div['data-last-price']), 
            'timestamp' : int(price_div['data-last-normal-market-timestamp']),
            'currency' : str(price_div['data-currency-code']),
            'to_USD' : convert_currency(str(price_div['data-currency-code']), 'USD')
            }


if __name__ == '__main__':
    print(get_price_information('TSLA', 'NASDAQ'))
    print(convert_currency('USD', 'CAD'))