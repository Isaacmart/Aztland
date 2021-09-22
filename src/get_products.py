from get_currencies import trader_robot
from get_indicators import GetAnyMACD
from app_methods import *


'''
Methods to create a list of the currencies with the greatest 
change of yielding the highest return. 

The list will display products that are traded in US dollars, e.g. 'CGLD-USD'. 
To do that we should get the 'quote_currency' key and
if it returns 'USD', the product can be added to the list
However, we must also check that the product can be traded at the time of
the analysis by getting the key 'trading_disabled' and if it is 'False'
then the product can be applied an indicator. 
The name passed to the indicator is the key 'id'
For the purpose of this experiment, we will get the MACD, however a better
indicator to measure the volativity of the prodcuts.
The file will run as an executable, every hour it will apply the 
indicator to the product, e.g. 1h_period.set_candles(product="ETH-USD", callback=get_time(n), new_gra=x)
if the hist > 0, then the product is added to the list.
When a POST request is received from Tradingview, the first thing the system
will do after making sure that there is not a long position is to make 
sure that the 'ticker' key is a valid product in the volativity list, if the 
ticker is a valid product, the system can continue and hopefully place
a buy order. 

Example of data:
        {
         'id': 'CGLD-BTC', 
         'base_currency': 'CGLD', 
         'quote_currency': 'BTC', 
         'base_min_size': '0.1', 
         'base_max_size': '34000', 
         'quote_increment': '0.00000001', 
         'base_increment': '0.01', 
         'display_name': 'CGLD/BTC', 
         'min_market_funds': '0.0001', 
         'max_market_funds': '10', 
         'margin_enabled': False, 
         'post_only': False, 
         'limit_only': False, 
         'cancel_only': False, 
         'trading_disabled': False, 
         'status': 'online', 
         'status_message': ''
         }
'''

data = trader_robot.get_products()

txt_file = open('txt_files/get_products.txt', 'w')
#data_file = open('txt_files/cb_tickers.txt', 'w')
data_file = open('txt_files/stat_tickers.txt', 'w')
data_list = [46]
index = 0


def get_products(value):

    if (value["quote_currency"] == 'USD') and (value["trading_disabled"] is False):

        token_for_data = str(value['id'])
        # new_token = token_for_data.replace('-', '')
        # data_file.write(new_token + '\n')
        data_file.write(token_for_data + '\n')

        value_macd = GetAnyMACD()
        value_macd.set_candles(product=value['id'], callback=get_time(2012040), begin_here=get_time(0),
                                   new_gra=21600)
        value_macd.set_any_MACD()
        if value_macd.get_hist() > 0:
            txt_file.write(str(value) + str(value_macd.get_hist()) + "\n")
            data_list.append(value_macd.get_hist())


data_list.sort()
print(data_list[-1])
