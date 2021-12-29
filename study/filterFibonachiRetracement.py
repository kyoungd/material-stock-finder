import os
from allstocks import AllStocks
from localMinMax import LocalMinMax
import pandas as pd


class fibonachiRetracement:
    def __init__(self, close, isFirstMin, df):
        self.df = df
        self.close = close
        self.isFirstMin = isFirstMin
        minChange = 0.02
        self.minimumChange = self.close * minChange
        self.toleranceLow = 0.4
        self.toleranceHigh = 0.73

    def isFibonachiRetrace(self, priceFirst, priceSecond):
        priceMove = priceFirst - priceSecond
        fibPriceSecond = self.close + priceMove * self.toleranceLow
        fibPriceFirst = self.close + priceMove * self.toleranceHigh
        if (priceSecond > fibPriceSecond) and (priceFirst < fibPriceFirst):
            return True
        else:
            return False

    def isPriceCheck(self, priceFirst, priceSecond):
        if self.isFirstMin and priceFirst > priceSecond:
            return True
        elif not self.isFirstMin and priceFirst < priceSecond:
            return True
        else:
            return False

    def retracement(self):
        price0 = self.df.iloc[0].Close
        price1 = self.df.iloc[1].Close
        price2 = 0 if self.df.count() < 3 else self.df.iloc[2].Close
        price3 = 0 if self.df.count() < 4 else self.df.iloc[3].Close
        price4 = 0 if self.df.count() < 5 else self.df.iloc[4].Close
        if self.isFibonachiRetrace(price0, price1):
            return True
        elif price2 > 0 and self.isPriceCheck(price1, price2) and self.isFibonachiRetrace(price1, price2):
            return True
        elif price3 > 0 and self.isPriceCheck(price0, price3) and self.isFibonachiRetrace(price0, price3):
            return True
        elif price4 > 0 and self.isPriceCheck(price1, price4) and self.isFibonachiRetrace(price1, price4):
            return True
        else:
            return False

    def Run(self):
        return self.retracement()


class FilterFibonachiRetracement:
    def __init__(self):
        self.retracementMin = float(os.environ.get(
            'FILTER_FIBONACHI_MIN', '0.02'))
        self.retracementTolerance = float(os.environ.get(
            'FILTER_FIBONACHI_TOLERANCE', '0.02'))

    def Run(self, symbol):
        isLoaded, dfDaily = AllStocks.GetDailyStockData(symbol)
        close = dfDaily['Close'][0]  # last close price
        minMax = LocalMinMax(dfDaily)
        isFirstMinimum, df = minMax.Run()
        if (df is None) or (df.count() < 2):
            return False


if __name__ == '__main__':
    data = {'Date':
            ['2021-01-07T00:00:00.000000000', '2021-02-01T00:00:00.000000000',
             '2021-03-12T00:00:00.000000000', '2021-04-23T00:00:00.000000000',
             '2021-05-28T00:00:00.000000000', '2021-09-01T00:00:00.000000000'],
            'Close':
                [120.00, 100.01, 99.51623309,
                 93.63782723, 91.50373968, 91.8385245]
            }
    df = pd.DataFrame(data)
    price = 100.01
    isFirstMin = False
    fib = fibonachiRetracement(price, isFirstMin, df)
    result = fib.Run()
    print(result)
