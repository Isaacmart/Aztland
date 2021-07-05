from get_currencies import trader_robot
import talib
import numpy
from app_methods import *

data = trader_robot.get_products()
txt_file = open('get_products.txt', 'w')

top_token = 0.0
macd_product = None

for value in data:

    data_list = []

    #verifies that the product is quoted in usd and that is is available for trading
    if (value["quote_currency"] == 'USD') and (value["trading_disabled"] is False):

        #Gets candlesticks for the product
        values_bb = trader_robot.get_product_historic_rates(product_id=value['id'], start=get_time(335340),
                                                            end=get_time(0), granularity=3600)

        #Appends the closing values for the period in an array
        for candle in values_bb:
            data_list.append(candle[4])

        #Reverses the array to present the latest values at the end
        data_list.reverse()
        #Writes the candlesticks to a numpy array
        np_array = numpy.array(data_list)

        #Applies the Bollinger Bands to the products's candlestick with a deviation of 2
        upperband, middleband, lowerband = talib.BBANDS(real=np_array, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

        #Applies the Bollinger Bands to the product's candlesticks with a deviation of 1
        oneupperband, onemiddleband, onelowerband = talib.BBANDS(real=np_array, timeperiod=20, nbdevup=1,
                                                                 nbdevdn=1, matype=0)

        #If the latest price is greater than the latest measure of the BB indicator, the
        #data for the product is written to a .tx file
        if np_array[-1] > onemiddleband[-1]:
            txt_file.write(str(value) + "bbands \n")

        #If it is not true, the MACD indicator will be used to check volativity
        else:

            #Applies the MACD indicator to the prodcut's candlestick
            macd, macdsignal, macdhist = talib.MACD(real=np_array, fastperiod=12, slowperiod=26, signalperiod=9)

            #Gets candlesticks for previous hour
            candle_list = []
            macd_values = trader_robot.get_product_historic_rates(product_id=value['id'], start=get_time(338940),
                                                                  end=get_time(3600), granularity=3600)

            for candle in macd_values:
                candle_list.append(candle[4])

            candle_list.reverse()
            num_array = numpy.array(candle_list)

            lastmacd, lastsignal, lastmacdhist = talib.MACD(real=num_array, fastperiod=12, slowperiod=26,
                                                            signalperiod=9)

            token = 0.0
            if (lastmacdhist[-1] < 0) and (macdhist[-1] > 0):
                token = 100 - (macdhist[-1] * 100 / lastmacdhist[-1])

            elif lastmacdhist[-1] and macdhist[-1] < 0:
                token = -100 - (macdhist[-1] * 100 / lastmacdhist[-1])

            elif (macdhist < 0) and (lastmacdhist[-1] > 0):
                token = -100 - (macdhist[-1] * 100 / lastmacdhist[-1])

            elif lastmacdhist and macdhist > 0:
                token = -100 + (macdhist[-1] * 100 / lastmacdhist[-1])

            if token < top_token:
                top_token = token
                macd_product = value

            print(top_token)

            if (macdhist[-1] > 0) and (macdhist[-1] > lastmacdhist[-1]):
                txt_file.write(str(value) + "macd \n")

txt_file.write(str(macd_product) + "top_token\n")








