import os
from util import StockAnalysis, AllStocks, LocalMinMax
import pandas as pd
import os

class trendMinMax:
    def __init__(self, minmaxs:pd.DataFrame, isFirstMin:bool, close: float):
        self.df = minmaxs
        self.isFirstMin = isFirstMin
        self.close = close
        self.minimumTrend = int(os.environ.get("FITLER_TREND_COUNT", '2'))
        self.minimumDelta = float(os.environ.get("FITLER_TREND_DELTA", '0.02'))

    def getDirections(self, df: pd.DataFrame, isFirstMin:bool, minDelta: float)->list:
        directions = []
        if len(df.index) < 3:
            return []
        for ix, row in df.iterrows():
            if ix >= 2:
                thisValue = row['Close']
                lastValue = df.iloc[ix - 2]['Close']
                delta = lastValue * minDelta
                if thisValue + delta > lastValue:
                    directions.append('up')
                elif thisValue - delta < lastValue:
                    directions.append('down')
                else:
                    directions.append('flat')
        return directions

    def trendingCount(self, directions:list, isFirstMin:bool, close:float, minDelta: float)->bool:
        dir1 = directions[0]
        count = 0
        for direction in directions:
            if direction != dir1:
                return count
            count += 0.5
        return count

    def reverseCount(self, directions:list, isFirstMin:bool, close:float, minDelta: float)->bool:
        dir2 = ''
        dir1 = directions[0]
        count = 0
        for direction in directions:
            if direction != dir1 and dir2 == '' and count <= 2.5:
                dir2 = direction
                count = 0
            elif dir2 != '' and direction != dir2 and dir2:
                return count
            count += 0.5
        return 0


    def Run(self)->set:
        directions = self.getDirections(self.df, self.isFirstMin, self.minimumDelta)
        if len(directions) <= 0:
            return 0, 0
        trendCount = self.trendingCount(directions, self.isFirstMin, self.close, self.minimumDelta)
        reverseCount = self.reverseCount(directions, self.isFirstMin, self.close, self.minimumDelta)
        return trendCount, reverseCount


class FilterTrends:
    def __init__(self):
        self.sa = StockAnalysis()
        self.jsonData = self.sa.GetJson

    def Run(self, symbol):
        isAssigned = False
        try:
            isLoaded, dfDaily = AllStocks.GetDailyStockData(symbol)
            if isLoaded:
                close = dfDaily['Close'][0]  # last close price
                minMax = LocalMinMax(dfDaily, 5)
                isFirstMinimum, df = minMax.Run()
                if df is not None and (len(df.index) > 3):
                    trend = trendMinMax(df, isFirstMinimum, close)
                    trendPeaks, reversePeaks = trend.Run()
                    self.sa.UpdateFilter(self.jsonData, symbol, 'trend', trendPeaks)
                    self.sa.UpdateFilter(self.jsonData, symbol, 'reverse', reversePeaks)
                    isAssigned = True
        except Exception as e:
            print(e)
        finally:
            if not isAssigned:
                self.sa.UpdateFilter(self.jsonData, symbol, 'trend', 0)
                self.sa.UpdateFilter(self.jsonData, symbol, 'reverse', 0)
            return False

    @staticmethod
    def All():
        filter = FilterTrends()
        AllStocks.Run(filter.Run, False)
        filter.sa.WriteJson(filter.jsonData)
