import pandas as pd
from util import StockAnalysis, AllStocks, JsonFavorite
import talib
import os
import json
import logging

class FilterCorrelate:
    def __init__(self):
        self.sa = StockAnalysis()
        self.jsonData = self.sa.GetJson
        corrFile = os.environ.get('CORRELATE_90_FILE', '')
        invsFile = os.environ.get('INVERSE_90_FILE', '')
        self.correlates = json.loads(JsonFavorite(filename=corrFile).GetJson)
        self.inverses = json.loads(JsonFavorite(filename=invsFile).GetJson)

    def analyzieMatix(self, symbol, row):
        symbols = []
        for key in row:
            if key != symbol:
                symbols.append(key)
        return symbols

    def corrMatch(self, symbol, corrs, colname):
        try:
            matrix1 = corrs[symbol]
            analysis1 = self.analyzieMatix(symbol, matrix1)
            self.sa.UpdateFilter(
                self.jsonData, symbol, colname, analysis1)                
        except KeyError:
            self.sa.UpdateFilter(
                self.jsonData, symbol, colname, [])
        except Exception as e:
            logging.error(
                f'FilterCorrelate.corrMatch - {symbol} {colname} {e}')
            print(f'FilterCorrelate.corrMatch - {symbol} {colname} {e}')
            self.sa.UpdateFilter(
                self.jsonData, symbol, 'corr', [])


    def Run(self, symbol):
        isLoaded, df = AllStocks.GetDailyStockData(symbol)
        if isLoaded:
            self.corrMatch(symbol, self.correlates, 'corr')
            self.corrMatch(symbol, self.inverses, 'cinv')
        return False

    def WriteFilter(self):
        self.sa.WriteJson(self.jsonData)

    @staticmethod
    def All():
        filter = FilterCorrelate()
        AllStocks.Run(filter.Run)


if __name__ == '__main__':
    FilterCorrelate.All()
    print('---------- done ----------')
    # filter = FilterEma(symbol='AAPL', barCount=20)
    # up, down = filter.Run(filter.symbol)
    # print(up, down)
