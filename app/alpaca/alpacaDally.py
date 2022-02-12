import json
import threading
from threading import Thread
import time
from dbase import MarketDataDb
from util import AlpacaAccess, RedisTimeFrame
from .alpacaHistorical import AlpacaHistorical
from .alpacaSnapshot import AlpacaSnapshots
from util import RedisTimeFrame

class AlpacaDaily():

    def __init__(self, startdate=None, enddate=None, alpacaObject = None, symbolFile = None):
        self.symbolFile = './data/symbols.csv' if symbolFile is None else symbolFile
        self.alpaca = AlpacaHistorical if alpacaObject is None else alpacaObject
        self.db = MarketDataDb()
        self.startdate = startdate
        self.enddate = enddate

    def getSymbolFile(self):
        filename = self.symbolFile
        with open(filename, 'r') as f:
            lines = f.readlines()
        return lines

    def getDataLine(self, app:AlpacaHistorical, symbol, db:MarketDataDb):
        try:
            timeframe = RedisTimeFrame.DAILY
            if self.startdate is not None and self.enddate is not None:
                data = app.HistoricalPrices(
                    symbol, timeframe, starttime=self.startdate, endtime=self.enddate)
            else:
                data = app.HistoricalPrices(symbol, timeframe)
            db.WriteMarket(symbol, data, datatype='stock', timeframe=timeframe)
        except Exception as e:
            print(e)

    def getHistorical(self, symbols):
        app = AlpacaHistorical()
        lineCount = 0
        for symbol in symbols:
            lineCount += 1
            print(lineCount)
            Thread(target=self.getDataLine, args=(app, symbol, self.db)).start()
            while (threading.activeCount() > 10):
                time.sleep(2)
        if threading.activeCount() > 0:
            time.sleep(2)

    def AppendSnpashots(self, dicts):
        for key in dicts:
            self.db.AppendMarket(key, dicts[key], datatype='stock')

    def getSnapshots(self, symbols):
        app = AlpacaSnapshots()
        app.RunDaily(symbols, self.AppendSnpashots)

    def Run(self):
        symbols = self.getSymbolFile()
        symbolHistoricals, symbolSnapshots = self.db.StockSymbols(symbols, 'stock')
        if symbolHistoricals:
            self.getHistorical(symbolHistoricals)
        if symbolSnapshots:
            self.getSnapshots(symbolSnapshots)

    @staticmethod
    def All():
        app = AlpacaDaily()
        app.Run()
