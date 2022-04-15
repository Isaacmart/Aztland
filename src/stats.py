import numpy as np
import scipy.stats as sps
import matplotlib.pyplot as plt
from cbpro import PublicClient
from util import get_time

client = PublicClient()
data = client.get_product_historic_rates(product_id="ETH-USD", start=get_time(60000), end=get_time(0), granularity=300)

avr = 0
candlesticks = []

for candle in data:
    candlesticks.append(float(candle[4]))


new_sum = sum(candlesticks)

avr = new_sum/len(candlesticks)
print(len(candlesticks))
mu = avr
sigma = len(candlesticks)

# define the normal distribution and PDF
dist = sps.norm(loc=mu, scale=sigma)
x = np.linspace(dist.ppf(.001), dist.ppf(.999))
y = dist.pdf(x)

# calculate PPFs
ppfs = {}
for ppf in [.1, .5, .8, .9]:
    p = dist.ppf(ppf)
    ppfs.update({ppf*100: p})

# plot results
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y, color='k')
for i, ppf in enumerate(ppfs):
    ax.axvline(ppfs[ppf], color=f'C{i}', label=f'{ppf:.0f}th: {ppfs[ppf]:.1f}')
ax.legend()
plt.show()


