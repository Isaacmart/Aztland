from indicators import MACD
from indicators import Indicator
from app_methods import get_time

cb = get_time(94 * 60)
bn = get_time(0)
indicator = Indicator()
indicator.set_candles("ETH-USD", cb, bn, 60)
indicator.set_indicator()


macd = MACD()
macd.np_array = indicator.np_array
macd.set_indicator()

