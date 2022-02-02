

import yfinance as yf
import time
import pandas as pd
from util import StockAnalysis, AllStocks
import dbase as db

class StockFinancial:
    def __init__(self, isDebug=None, isForceDownloadYahoo=None):
        self.sa = StockAnalysis()
        self.jsonData = self.sa.GetJson
        self.lineCount = 0
        self.isDebug = isDebug
        self.db = db.SecDb()
        self.isDownload = True if isForceDownloadYahoo else False

    # def getFinancials(self, symbol):
    #     stock = yf.Ticker(symbol)
    #     # get stock info
    #     floats = 0 if stock.info['floatShares'] is None else round(stock.info['floatShares'] / 1000000, 1)
    #     floatp = 0 if stock.info['shortPercentOfFloat'] is None else round(stock.info['shortPercentOfFloat'] * 100, 1)
    #     return floats, floatp

    def getFinancials(self, symbol):
        try:
            if self.isDebug:
                self.lineCount += 1
            stock = yf.Ticker(symbol)
            # get stock info
            floats = 0 if stock.info['floatShares'] is None else round(
                stock.info['floatShares'] / 1000000, 1)
            floatp = 0 if stock.info['shortPercentOfFloat'] is None else round(
                stock.info['shortPercentOfFloat'] * 100, 1)
            if self.isDebug:
                print('{} - {}'.format(symbol, self.lineCount))
            return floats, floatp
        except Exception as e:
            print('{} {} - {}'.format(self.lineCount, symbol, e))
            return 0, 0

    def Run(self, symbol):
        isLoaded, tp = AllStocks.GetDailyStockData(symbol)
        if isLoaded:
            try:
                if self.isDebug:
                    self.lineCount += 1
                isOk, (floatp, floatv) = self.db.GetFloats(symbol)
                if not isOk or self.isDownload:
                    floatv, floatp = self.getFinancials(symbol)
                    self.db.SetFloats(symbol, floatp, floatv)
                self.sa.UpdateFilter(self.jsonData, symbol, 'floatv', floatv)
                self.sa.UpdateFilter(self.jsonData, symbol, 'floatp', floatp)
                if self.isDebug:
                    print('{} - {}'.format(symbol, self.lineCount))
            except Exception as e:
                print('{} {} - {}'.format(self.lineCount, symbol, e))
                self.sa.UpdateFilter(
                    self.jsonData, symbol, 'floatv', 0)
                self.sa.UpdateFilter(
                    self.jsonData, symbol, 'floatp', 0)
                time.sleep(1)
        return False

    @staticmethod
    def All(isDebug=None, isForceDownloadYahoo=None):
        isDebug = True if isDebug else False
        isForceDownloadYahoo = True if isForceDownloadYahoo else False
        filter = StockFinancial(isDebug=isDebug, isForceDownloadYahoo=isForceDownloadYahoo)
        AllStocks.Run(filter.Run, False)
        filter.sa.WriteJson(filter.jsonData)


if __name__ == '__main__':
    # StockFinancial.All(True)
    # print('---------- done ----------')
    filter = StockFinancial(isDebug=True)
    filter.getFinancialData('AAPL')
