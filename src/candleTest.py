from indicators import MACD
from indicators import BB
from indicators import RSI
from indicators import VolSMA
from indicators import Indicator
from threading import Thread


class CandleTest:

    def __init__(self, name, timeline):
        self.macd = MACD()
        self.rsi = RSI()
        self.bb1 = BB()
        self.bb2 = BB(ndbevup=1, nbdevdn=1)
        self.smavol = VolSMA()
        self.indicators = [self.macd, self.rsi, self.smavol, self.bb1, self.bb2]
        self.values = {
            "product": name,
            "timeline": timeline,
            "price": 0,
            "time": 0,
            "buy": False,
            "macd_macd": 0.0,
            "macd_signal": 0.0,
            "macd_hist": 0.0,
            "rsi": 0.0,
            "volume": 0.0,
            "sma(volume)": 0.0,
            "bb2_upper": 0.0,
            "bb2_middle": 0.0,
            "bb2_lower": 0.0,
            "bb2_%bb": 0.0,
            "bb2_bbw": 0.0,
            "bb2_sma(bbw)": 0.0,
            "bb1_upper": 0.0,
            "bb1_middle": 0.0,
            "bb1_lower": 0.0,
            "bb1_%bb": 0.0,
            "bb1_bbw": 0.0,
            "bb1_sma(bbw)": 0.0
        }

    def update_indicator(self, indicator: Indicator, array):
        indicator.set_indicator(array)
        values_dict = indicator.get_index(-1)
        #Adds the values of indicator to the values of the test
        for key in values_dict:
            if key in self.values:
                self.values[key] = values_dict[key]

    def update_values(self, array):
        for indicator in self.indicators:
            self.update_indicator(indicator, array)

    def update_price(self, np_array):
        self.values["price"] = np_array[-1]

    def update_time(self, timeline):
        self.values["time"] = timeline

    def longTest(self):
        if self.values["macd_hist"] >= 0:
            if self.values["macd_macd"] >= 0:
                if self.values["bb1_%bb"] >= 1.0:
                    if self.values["bb1_bbw"] >= self.values["bb1_sma(bbw)"]:
                        if self.values["rsi"] >= 70:
                            return True

    def shortTest(self):
        return not self.longTest()

    def test(self, array):
        self.update_price(array)
        self.update_values(array)
        if self.longTest():
            self.values["buy"] = True
