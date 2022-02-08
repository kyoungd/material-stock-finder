import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from .allstocks import AllStocks
import os

class TightMinMax:
    def __init__(self, df, tightMinMaxN = None, colName = None):
        self.colName = 'Close' if colName is None else colName
        self.df = df
        self.df = self.df.reset_index()
        n = int(os.environ.get('TIGHT_MINMAX_N', '4'))
        self.minMaxN = n if tightMinMaxN is None else tightMinMaxN
    
    def getMinMax(self, df=None):
        if df is None:
            df = self.df
        n = self.minMaxN        # number of points to be checked before and after

        df['min'] = df.iloc[argrelextrema(df[self.colName].values, np.less_equal,
                            order=n)[0]][self.colName]
        df['max'] = df.iloc[argrelextrema(df[self.colName].values, np.greater_equal,
                            order=n)[0]][self.colName]
        firstMin = False
        l_minmax = None
        for ix in range(len(df.index)):
            lmin = df.iloc[ix]['min']
            lmax = df.iloc[ix]['max']
            if np.isnan(lmin):
                close = df.iloc[ix][self.colName]
                if l_minmax is None:
                    l_minmax = {f'{self.colName}': close, 'index': ix, 'type': 'min'}
                    firstMin = True
                else:
                    if l_minmax['type'] == 'max':
                        l_minmax = {f'{self.colName}': close, 'index': ix, 'type': 'min'}
                    elif (close >= l_minmax[self.colName]):
                        df['min'][ix] = np.nan
                    else:
                        lastIx = l_minmax['index']
                        df['min'][lastIx] = np.nan
                        l_minmax = {f'{self.colName}': close, 'index': ix, 'type': 'min'}
            elif np.isnan(lmax):
                close = df.iloc[ix][self.colName]
                if l_minmax is None:
                    l_minmax = {f'{self.colName}': close, 'index': ix, 'type': 'max'}
                    firstMin = False
                else:
                    if l_minmax['type'] == 'min':
                        l_minmax = {f'{self.colName}': close, 'index': ix, 'type': 'max'}
                    elif (close <= l_minmax[self.colName]):
                        df['max'][ix] = np.nan
                    else:
                        lastIx = l_minmax['index']
                        df['max'][lastIx] = np.nan
                        l_minmax = {f'{self.colName}': close, 'index': ix, 'type': 'max'}

        timeframes = []
        closes = []
        for _, row in df.iterrows():
            data = None
            if not np.isnan(row['min']) or not np.isnan(row['max']):
                closes.append(row[self.colName])
                timeframes.append(row['Date'])
        df1 = pd.DataFrame.from_dict({'Date': timeframes, f'{self.colName}': closes})
        return firstMin, df1

    def Run(self):
        isFirstMin, df1 = self.getMinMax()
        return isFirstMin, df1


if __name__ == '__main__':
    symbol = 'AAPL'
    isLoaded, df = AllStocks.GetDailyStockData(symbol)
    if isLoaded:
        app = TightMinMax(df)
        firstMin, df = app.Run()
        print(df)
        print(firstMin)
    print('done')
