
f_request = {"exchange": "COINBASE", "ticker": "STORJUSD", "price": "2054.43", "volume": "975.23", "hist": "0.23", "macd": "-20.28", "signal": "-20.52"}


def get_ticker_product(new_request):
    new_ticker = new_request['ticker']
    new_coin = new_ticker[0:-3]
    coin_currency = new_ticker[-3:]
    ticker_product = new_coin + "-" + coin_currency
    return ticker_product


print(get_ticker_product(f_request))

