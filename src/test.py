from indicators import Indicator
from app_methods import get_time
import sys
import numpy

indicator = Indicator()
indicator.set_candles(product="ETH-USD", callback=get_time(27976), begin=get_time(0), granularity=300)
indicator.set_indicator()
indicator.set_dates()
print(indicator.np_array)
print(sys.getsizeof(indicator.np_array))

arr = numpy.delete(indicator.np_array, 0)

print(sys.getsizeof(arr))
