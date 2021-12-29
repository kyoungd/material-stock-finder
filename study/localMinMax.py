import numpy as np
import pandas as pd
from allstocks import AllStocks


class LocalMinMax:
    def __init__(self, df):
        self.df = df
        self.df = self.df.reset_index()

    def Run(self):
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


if __name__ == '__main__':
    symbol = 'AAPL'
    isLoaded, df = AllStocks.GetDailyStockData(symbol)
    if isLoaded:
        app = LocalMinMax(df)
        firstMin, df = app.Run()
        print(df)
        print(firstMin)
    print('done')
