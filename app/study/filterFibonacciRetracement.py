import os
from util import StockAnalysis, AllStocks, LocalMinMax
import pandas as pd
import os


class fibonachiRetracement:
    def __init__(self, close, isFirstMin, df):
        self.df = df
        self.close = close
        self.isFirstMin = isFirstMin
        minChange = float(os.environ.get(
            "FITLER_FIBONACHI_MIN_CHANGE_PERCENT", '0.04'))
        self.minimumChange = self.close * minChange
        self.tolerance50 = 0.45
        self.tolerance63 = 0.68

    def isFibonachiRetrace(self, priceFirst, priceSecond):
        priceMove = priceSecond - priceFirst
        if abs(priceMove) < self.minimumChange:
            return False
        fibPrice50 = priceFirst + priceMove * self.tolerance50
        fibPrice63 = priceFirst + priceMove * self.tolerance63
        if (priceMove > 0) and (self.close > fibPrice50) and (self.close < fibPrice63):
            return True
        elif (priceMove < 0) and (self.close < fibPrice50) and (self.close > fibPrice63):
            return True
        else:
            return False

    def priceCheck5(self, p0, p1, p2, p3, p4):
        result = []
        d0 = abs(p0-p1)
        d1 = abs(p1-p2) if p2 > 0 else 0
        d2 = abs(p2-p3) if p3 > 0 else 0
        d2a = abs(p0-p3) if p3 > 0 else 0
        d3 = abs(p3-p4) if p4 > 0 else 0
        d3b = abs(p1-p4) if p4 > 0 else 0
        result.append([p0, p1])
        if d1 > d0:
            result.append([p1, p2])
        if p2 > 0 and d2 > d1 and d2 > d0:
            result.append([p2, p3])
        if p2 > 0 and d2a > d3 and d2a > d2 and d2a > d1 and d2a > d0:
            result.append([p0, p3])
        if p3 > 0 and d3 > d2 and d3 > d1 and d3 > d0:
            result.append([p3, p4])
        if p4 > 0 and d3b > d2a and d3b > d3 and d3b > d2 and d3b > d1 and d3b > d0:
            result.append([p1, p4])
        return result

    def retracement(self):
        price0 = self.df.iloc[0].Close
        price1 = self.df.iloc[1].Close
        price2 = 0 if len(self.df) < 3 else self.df.iloc[2].Close
        price3 = 0 if len(self.df) < 4 else self.df.iloc[3].Close
        price4 = 0 if len(self.df) < 5 else self.df.iloc[4].Close
        listOfPrices = self.priceCheck5(price0, price1, price2, price3, price4)
        for prices in listOfPrices:
            if self.isFibonachiRetrace(prices[0], prices[1]):
                return True
        return False

    def Run(self):
        return self.retracement()


class FilterFibonacciRetracement:
    def __init__(self):
        self.sa = StockAnalysis()
        self.jsonData = self.sa.GetJson

    def Run(self, symbol):
        try:
            isLoaded, dfDaily = AllStocks.GetDailyStockData(symbol)
            close = dfDaily['Close'][0]  # last close price
            minMax = LocalMinMax(dfDaily)
            isFirstMinimum, df = minMax.Run()
            if (df is None) or (len(df) < 2):
                return False
            fib = fibonachiRetracement(close, isFirstMinimum, df)
            result = fib.Run()
            self.sa.UpdateFilter(self.jsonData, symbol, 'fibonachi', result)
            return result
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def All():
        filter = FilterFibonacciRetracement()
        AllStocks.Run(filter.Run, False)
        filter.sa.WriteJson(filter.jsonData)


if __name__ == '__main__':
    FilterFibonacciRetracement.All()
    print('------------------------done ------------------------')

    # data = {'Date':
    #         ['2021-01-07T00:00:00.000000000', '2021-02-01T00:00:00.000000000',
    #          '2021-03-12T00:00:00.000000000', '2021-04-23T00:00:00.000000000',
    #          '2021-05-28T00:00:00.000000000', '2021-09-01T00:00:00.000000000'],
    #         'Close':
    #             [120.00, 100.01, 99.51623309,
    #              93.63782723, 91.50373968, 91.8385245]
    #         }
    # df = pd.DataFrame(data)
    # price = 110.01
    # isFirstMin = False
    # fib = fibonachiRetracement(price, isFirstMin, df)
    # result = fib.Run()
    # print(result)
