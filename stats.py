import numpy as np
import scipy.stats as sps
import matplotlib.pyplot as plt

mu = 25
sigma = 4

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