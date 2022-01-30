import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from .allstocks import AllStocks


class LocalMinMax:
    def __init__(self, df):
        self.df = df
        self.df = self.df.reset_index()

    def Polyfit(self):
        # discrete dataset
        x_data = self.df.index.tolist()      # the index will be our x axis, not date
        y_data = self.df['Close']
        t_data = self.df['Date']

        # x values for the polynomial fit, 200 points
        x = np.linspace(0, max(self.df.index.tolist()),
                        max(self.df.index.tolist()) + 1)

        # polynomial fit of degree xx
        pol = np.polyfit(x_data, y_data, 30)
        y_pol = np.polyval(pol, x)

        data = y_pol

        # ___ detection of local minimums and maximums ___

        min_max = np.diff(np.sign(np.diff(data))).nonzero()[
            0] + 1          # local min & max
        l_min = (np.diff(np.sign(np.diff(data))) >
                 0).nonzero()[0] + 1      # local min
        l_max = (np.diff(np.sign(np.diff(data))) <
                 0).nonzero()[0] + 1      # local max

        # ___ package local minimums and maximums for return  ___

        # dfMin = None if len(l_min) < 0 else pd.DataFrame.from_dict(
        #     {'Date': t_data[l_min].values, 'Close': data[l_min]})
        # dfMax = pd.DataFrame.from_dict(
        #     {'Date': t_data[l_max].values, 'Close': data[l_max]})
        # return dfMin, dfMax

        l_minmax = np.sort(np.append(l_min, l_max))
        isFirstMinimum = True if l_min[len(
            l_min)-1] < l_max[len(l_max)-1] else False
        timeframes = t_data[l_minmax].values
        closes = data[l_minmax]
        df = pd.DataFrame.from_dict({'Date': timeframes, 'Close': closes})
        return isFirstMinimum, df


    def TightMinMiax(self, df=None):
        if df is None:
            df = self.df
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
                    l_minmax = {'Close': thisPt['Close'],
                                'index': ix, 'type': 'min'}
                elif (thisPt['Close'] >= l_minmax['Close']):
                    df['min'][ix] = np.nan
                else:
                    lastIx = l_minmax['index']
                    df['min'][lastIx] = np.nan
                    l_minmax = {'Close': thisPt['Close'],
                                'index': ix, 'type': 'min'}
            elif not np.isnan(lmax):
                thisPt = df.iloc[ix]
                if l_minmax['type'] == 'min':
                    l_minmax = {'Close': thisPt['Close'],
                                'index': ix, 'type': 'max'}
                elif (thisPt['Close'] <= l_minmax['Close']):
                    df['max'][ix] = np.nan
                else:
                    lastIx = l_minmax['index']
                    df['max'][lastIx] = np.nan
                    l_minmax = {'Close': thisPt['Close'],
                                'index': ix, 'type': 'max'}

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

    def Run(self):
        isFirstMin, df1 = self.TightMinMiax()
        return isFirstMin, df1


if __name__ == '__main__':
    symbol = 'AAPL'
    isLoaded, df = AllStocks.GetDailyStockData(symbol)
    if isLoaded:
        app = LocalMinMax(df)
        firstMin, df = app.Run()
        print(df)
        print(firstMin)
    print('done')
