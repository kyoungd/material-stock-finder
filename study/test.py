# from cmath import nan
# import yfinance as yf
from scipy.signal import argrelextrema
import numpy as np
import pandas as pd
from localMinMax import LocalMinMax
from allstocks import AllStocks

# hist = yf.Ticker("VZ")

# # get stock info
# hist.info

# # get historical market data
# df = hist.history(period="1y")


# app = LocalMinMax(df)
# firstMin, df = app.Run()
# print(df)
# print(firstMin)

def TightMinMiax(df):
    n = 4  # number of points to be checked before and after

    df['min'] = df.iloc[argrelextrema(df.Close.values, np.less_equal,
                        order=n)[0]]['Close']
    df['max'] = df.iloc[argrelextrema(df.Close.values, np.greater_equal,
                        order=n)[0]]['Close']
    firstMin = False
    l_minmax = None
    for ix in range(len(df.index)):
        lmin = df.iloc[ix]['min']
        lmax = df.iloc[ix]['max']
        if l_minmax is None and not np.isnan(lmin):
            l_minmax = {'Close': lmin, 'index': ix, 'type': 'min'}
            firstMin = True
        elif l_minmax is None and not np.isnan(lmax):
            l_minmax = {'Close': lmax, 'index': ix, 'type': 'max'}
            firstMin = False
        elif not np.isnan(lmin):
            thisPt = df.iloc[ix]
            if l_minmax['type'] == 'max':
                l_minmax = {'Close': thisPt['Close'], 'index': ix, 'type': 'min'}
            elif (thisPt['Close'] >= l_minmax['Close']):
                df['min'][ix] = np.nan
            else:
                lastIx = l_minmax['index']
                df['min'][lastIx] = np.nan
                l_minmax = {'Close': thisPt['Close'], 'index': ix, 'type': 'min'}
        elif not np.isnan(lmax):
            thisPt = df.iloc[ix]
            if l_minmax['type'] == 'min':
                l_minmax = {'Close': thisPt['Close'], 'index': ix, 'type': 'max'}
            elif (thisPt['Close'] <= l_minmax['Close']):
                df['max'][ix] = np.nan
            else:
                lastIx = l_minmax['index']
                df['max'][lastIx] = np.nan
                l_minmax = {'Close': thisPt['Close'], 'index': ix, 'type': 'max'}
    
    timeframes = []
    closes = []
    for _, row in df.iterrows():
        data = None
        if not np.isnan(row['min']):
            data = row['min']
        elif not(row['max']):
            data = row['max']
        if data is not None:
            closes.append(data)
            timeframes.append(row['Date'])
    df1 = pd.DataFrame.from_dict({'Date': timeframes, 'Close': closes})
    return firstMin, df1

symbol = 'AAPL'
isLoaded, df = AllStocks.GetDailyStockData(symbol)
if isLoaded:
    app = LocalMinMax(df)
    firstMin, df = app.Run()
    # firstMin, df = TightMinMiax(df)
    print(df)
    print(firstMin)
