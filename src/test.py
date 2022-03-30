from indicators import Indicator
from cbpro import PublicClient
from app_methods import get_time
import numpy


#################################################
######### Tests for the Indicator class #########
#################################################

# Tests that the deques implementation has the same functionality as a list implementation
def deque_test(n, g):
    indicator = Indicator()
    indicator.set_candles(product="ETH-USD", callback=get_time(n * g), begin=get_time(0), granularity=g)

    client = PublicClient()
    data = client.get_product_historic_rates(product_id="ETH-USD", start=get_time(n * g), end=get_time(0),
                                             granularity=g)

    index = -1
    passed = True
    try:
        for line in indicator.candles:
            if line != data[index]:
                passed = False
                break
            index -= 1

    except Exception:
        passed = False

    if passed:
        print(f"Deque for granularity {g} and number of cells {n} test passed ✓")
    else:
        print(f"Deque for granularity {g} and number of cells {n} test failed ✕")


# Tests that only the latest candles are stored
def set_size_test(n, g):
    indicator = Indicator(max_length=n)
    indicator.set_candles(product="ETH-USD", callback=get_time(n * g), begin=get_time(0), granularity=g)

    client = PublicClient()
    data = client.get_product_historic_rates(product_id="ETH-USD", start=get_time(n * g), end=get_time(0),
                                             granularity=g)

    index = -1
    passed = True
    try:
        for line in indicator.candles:
            if line != data[index]:
                passed = False
                break
            index -= 1

    except Exception:
        passed = False

    if passed:
        print(f"Set size for granularity {g} and number of cells {n} test passed ✓")
    else:
        print(f"Set size for granularity {g} and number of cells {n} test failed ✕")


# Tests that prices are stored correctly
def store_prices_test(n, g):
    indicator = Indicator(max_length=n)
    indicator.set_candles(product="ETH-USD", callback=get_time(n * g), begin=get_time(0), granularity=g)

    client = PublicClient()
    data = client.get_product_historic_rates(product_id="ETH-USD", start=get_time(n * g), end=get_time(0),
                                             granularity=g)
    clarray = []
    passed = True

    try:
        for index in data:
            clarray.append(float(index[4]))
        clarray.reverse()

        indicator.set_indicator()

        index = 0
        for line in indicator.close_array:
            if line != clarray[index]:
                passed = False
                break
            index += 1
    except Exception:
        passed = False

    if passed:
        print(f"Closing price for granularity {g} and number of cells {n} test passed ✓")
    else:
        print(f"Closing price for granularity {g} and number of cells {n} test failed ✕")
        print(indicator.close_array)
        print(clarray)


grans = [60, 300, 900, 3600, 21600, 86400]
num = [1, 100, 150, 200]

for n in num:
    for g in grans:
        deque_test(n, g)
        set_size_test(n, g)
        store_prices_test(n,g)
