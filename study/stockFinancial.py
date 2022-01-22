

import yfinance as yf

import pandas as pd
from allstockanalysis import StockAnalysis
from allstocks import AllStocks
import talib
import os
import time


class StockFinancial:
    def __init__(self, isDebug=False):
        self.sa = StockAnalysis()
        self.jsonData = self.sa.GetJson
        self.lineCount = 0
        self.isDebug = isDebug

    def getFinancials(self, symbol):
        stock = yf.Ticker(symbol)
        # get stock info
        floats = 0 if stock.info['floatShares'] is None else round(stock.info['floatShares'] / 1000000, 1)
        floatp = 0 if stock.info['shortPercentOfFloat'] is None else round(stock.info['shortPercentOfFloat'] * 100, 1)
        return floats, floatp

    def Run(self, symbol):
        isLoaded, tp = AllStocks.GetDailyStockData(symbol)
        if isLoaded:
            try:
                if self.isDebug:
                    self.lineCount += 1
                floats, floatp = self.getFinancials(symbol)
                self.sa.UpdateFilter(self.jsonData, symbol, 'floats', floats)
                self.sa.UpdateFilter(self.jsonData, symbol, 'floatp', floatp)
                if self.isDebug:
                    print('{} - {}'.format(symbol, self.lineCount))
            except Exception as e:
                if self.isDebug:
                    print('{} {} - {}'.format(self.lineCount, symbol, e))
                self.sa.UpdateFilter(
                    self.jsonData, symbol, 'floats', 0)
                self.sa.UpdateFilter(
                    self.jsonData, symbol, 'floatp', 0)
                time.sleep(1)
        return False

    @staticmethod
    def All(isDebug=False):
        filter = StockFinancial(isDebug=isDebug)
        AllStocks.Run(filter.Run, False)
        filter.sa.WriteJson(filter.jsonData)


if __name__ == '__main__':
    StockFinancial.All(True)
    print('---------- done ----------')
    # filter = FilterEma(symbol='AAPL', barCount=20)
    # up, down = filter.Run(filter.symbol)
    # print(up, down)
