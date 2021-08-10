from indicators import Indicator
from indicators import MACD
from indicators import BB
from indicators import VolSMA
from indicators import RSI
from indicators import EMA


class Strategy(MACD, BB, VolSMA, RSI, EMA, Indicator):

    def __init__(self):
        self.indicator = Indicator
        self.macd = MACD
        self.bands_1dev = BB
        self.bands_2dev = BB
        self.volume = VolSMA
        self.rsi = RSI
        self.ema = EMA

    def start_bb(self):
        self.bands_1dev.__init__(ndbevup=1, nbdevdn=1)


new_strategy = Strategy()
new_strategy.start_bb()
data = new_strategy.bands_1dev.get_BB()
print(data)





