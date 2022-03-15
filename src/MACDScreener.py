from indicators import MACD
from dict import new_dict
from app_methods import get_time

""" Analyzes the daily MACD for each token """

tokens_macds =[]


for token in new_dict:

    macd = MACD()

    callback = get_time(8346240)

    macd.set_candles(product=token, callback=callback, begin=get_time(0), granularity=86400)
    try:
        macd.set_indicator()
        percent: int
        percent = (macd.hist[-1] * 100) / macd.price()
        tokens_macds.append([token, percent])

    except Exception:
        continue

    print(token)

print(tokens_macds)
tokens_macds.sort(key=lambda x: x[1], reverse=True)

writer = open("../txt_files/token_macds.txt", "w")
for line in tokens_macds:
    try:
        writer.write(str(line) + "\n")
    except Exception:
        continue
writer.close()




