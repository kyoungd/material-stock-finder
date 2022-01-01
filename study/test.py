import pandas as pd
import numpy as np
import talib
from talib import stream
from allstocks import AllStocks

# the Function API
isLoaded, tp = AllStocks.GetDailyStockData('AAPL')
print(tp)
print(type(tp))
# get column as array
# print(tp.High)
high = tp.High.to_numpy()
low = tp.Low.to_numpy()
close = tp.Close.to_numpy()
output = talib.ATR(high, low, close, timeperiod=14)

# the Streaming API
latest = stream.ATR(high, low, close)

print(output)
print(latest)

# # the latest value is the same as the last output value
# assert (output[-1] - latest) < 0.00001
