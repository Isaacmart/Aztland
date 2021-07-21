from dict import new_dict
import math


def round_down(n, decimals=0):
    if decimals >= 0:
        multiplier = 10 ** decimals
        round_n = math.floor(n * multiplier) / multiplier
    else:
        round_n = int(n)
    return round_n


def get_size(ticker, size):

    if ticker in new_dict:

        return round_down(float(size), int(new_dict[ticker]))


print(get_size("ETH-USD", 3.1234567890))





















