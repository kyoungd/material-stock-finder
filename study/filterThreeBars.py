import pandas as pd
from filterFibonachiRetracement import fibonachiRetracement, FilterFibonachiRetracement
from allstocks import AllStocks


class FilterThreeBars:
    def __init__(self):
        pass

    def isThreeBars(self, p0, p1, p2):
        if p0 > p1 and p1 < p2:
            return True
        if p0 < p1 and p1 > p2:
            return True
        return False

    def makeDataFrame(self, p0, p1, p2):
        data = {'Date':
                ['2021-01-07T00:00:00.000000000', '2021-02-01T00:00:00.000000000',
                 '2021-03-12T00:00:00.000000000'],
                'Close':
                    [p0, p1, p2]
                }
        df = pd.DataFrame(data)
        return df

    def threeBarsDf(self, dfDaily):
        p0 = dfDaily['Close'][0]  # last close price
        p1 = dfDaily['Close'][1]
        p2 = dfDaily['Close'][2]
        p3 = dfDaily['Close'][3]
        dfs = []
        if self.isThreeBars(p0, p1, p2):
            df = self.makeDataFrame(p0, p1, p2)
            dfs.append(df)
        if self.isThreeBars(p0, p2, p3):
            df = self.makeDataFrame(p0, p2, p3)
            dfs.append(df)
        if self.isThreeBars(p0, p1, p3):
            df = self.makeDataFrame(p0, p1, p3)
            dfs.append(df)
        return dfs

    def ThreeBarLogic(self, dfDaily):
        dfs = self.threeBarsDf(dfDaily)
        if len(dfs) <= 0:
            return False
        for df in dfs:
            isFirstMin = df['Close'][0] < df['Close'][1]
            price = df['Close'][0]
            fib = fibonachiRetracement(price, isFirstMin, df)
            if fib.Run():
                return True
        return False

    def Run(self, symbol):
        isLoaded, dfDaily = AllStocks.GetDailyStockData(symbol)
        result = self.ThreeBarLogic(dfDaily)
        return result
