import cbpro
from flask import Flask, request,
from get_product_historic_rates import get_any_MACD, get_time
from get_accounts import trader_client


app = Flask(__name__)


@app.route("/", methods=['POSt', 'GET'])
def get_webhooks():
    new_request = 'none'
    if request.method == 'POST':
        try:
            new_request = request.json
        except None:
            pass
    return new_request, 200


def get_ticker(new_request):
    ticker = 'none'
    try:
        ticker = new_request['ticker']
    except None:
        pass
    return ticker


def asssess_tradeability(new_request, ticker):
    if new_request['macd'] - new_request < 0.0000001:
        15m_macd = get_any_MACD(product=ticker, period= 15, callback=5580, a_granularity=60)
        5m_macd =  get_any_MACD(product=ticker, period=5, callback=5580, a_granularity=60)
        if (15m_macd[macd] - 15m_macd[hist] < 0.000001) and (5m_macd[macd] and 5m_macd[hist > 0.0])
            return True
        else:
            return False
    else:
        return False

    
def place_order(new_request, ticker, funds):
    if asssess_tradeability(new_request, ticker):
        trader_client.place_market_order(product_id=ticker, side='buy', funds=funds)



