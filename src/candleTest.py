from indicators import MACD
from indicators import BB
from indicators import RSI
from indicators import VolSMA
from threading import Thread


class CandleTest:
    self.macd = MACD()
    self.rsi = RSI()
    self.bb1 = BB()
    self.bb2 = BB(ndbevup=1, nbdevdn=1)
    self.indicators = [self.macd, self.rsi, self.bb1, self.bb2]
    values = {
        "price": 0,
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

    def update_np_array(self, array):
        for indicator in self.indicators:
            indicator.np_array = array

    def update_indicator(self, indicator: Indicator):
        indicator.set_indicator()
        values_dict = indicator.get_index(-1)
        for key in values_dict:
            if key in self.values:
                self.values[key] = values_dict[key]

    def update_values(self):
        threads = []
        for indicator in self.indicators:
            threads.append(Thread(target=self.update_indicator(indicator)))

        for thread in threads:
            thread.start()

        threads[-1].join()

    def update_price(self, price):
        self.values["price"] = price

    def longTest(self):
        if self.values["macd_hist"] >= 0:
            if self.values["macd_macd"] >= 0:
                if self.values["bb1_%bb"] >= 1.0:
                    if self.values["bb1_bbw"] >= self.values["bb1_sma(bbw)"]:
                        if self.values["rsi"] >= 70:
                            return True

    def shortTest(self):
        if self.longTest():
            return False
