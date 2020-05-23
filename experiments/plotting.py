import timeit
from humanfriendly import format_timespan
import codecs
from itertools import combinations
import matplotlib.pyplot as plt
import math
import gc
import pickle
import numpy as np


x = pickle.load(open("x.p", "rb"))
product_co_reviewing_count = pickle.load(open("product_co_reviewing_count.p", "rb"))

plt.plot(x, product_co_reviewing_count, '-ok', color='black')
plt.xlabel("# co-reviewed products")
plt.ylabel("log of # pairs co-reviewed x products")
plt.xlim(0, 50)
plt.savefig('experiment.png')
plt.show()

