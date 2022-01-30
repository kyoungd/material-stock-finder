from alpaca_trade_api.rest import REST
import json
import os
from util import StockAnalysis
from util import AlpacaAccess
from dbase import SecDb

class overnightGapper:
    CsvHeader = "Date, Open, High, Low, Close, Adj Close, Volume"
    conn: REST = None

    def __init__(self):
        self.sa = StockAnalysis()
        self.data = self.sa.GetJson
        self.db = SecDb()

    def getLastNightGapper(self, price1, price2):
        priceMin = float(os.environ.get('OG_MIN_PRICE', '0.30'))
        percentMin = float(os.environ.get('OG_MIN_PERCENT', '0.05'))
        priceMoveValue = abs(price2 - price1)
        priceMovePercent = priceMoveValue / price1
        return round(priceMovePercent * 100)

    def getSnapshotFromApi(self, symbols):
        data = AlpacaAccess.HistoricalSnapshots(symbols)
        if (data.status_code == 422):
            removeSymbols = json.loads(data.text)['message'].split(':')[1]
            rejectedSymbols = set()
            for symbol in removeSymbols.strip().split(','):
                rejectedSymbols.add(symbol)
            symbolList = symbols.difference(rejectedSymbols)
            data = AlpacaAccess.HistoricalSnapshots(symbolList)
        snapshots = json.loads(data.text)
        return snapshots

    def getSnapshotAtMarketClose(self, symbols):
        snapshots = self.getSnapshotFromApi(symbols)
        for symbol in snapshots.keys():
            try:
                price1 = self.db.GetLastDaily(symbol)
                price2 = float(snapshots[symbol]['minuteBar']['c'])
                isOvernightGapper = self.getLastNightGapper(
                    price1, price2)
                print('{} {} {} {}'.format(symbol, price1, price2, isOvernightGapper))
                self.sa.UpdateFilter(
                    self.data, symbol, 'lng', isOvernightGapper)
            except Exception as e:
                try:
                    print('ERROR: ' + symbol + ': ' + str(e))
                    self.sa.UpdateFilter(self.data, symbol, 'lng', 0)
                except Exception as e:
                    print(e)

    def getSnapshotAtMarketOpen(self, symbols):
        snapshots = self.getSnapshotFromApi(symbols)
        for symbol in snapshots.keys():
            try:
                price2 = float(snapshots[symbol]['minuteBar']['c'])
                self.db.SetLastDaily(symbol, price2)
                return price2
            except Exception as e:
                try:
                    print('ERROR: ' + symbol + ': ' + str(e))
                except Exception as e:
                    print(e)
                self.db.SetLastDaily(symbol, 0)

class LastNightGapper:
    def __init__(self, isMarketClose, isDebug=None):
        self.og = overnightGapper()
        self.isDebug = True if isDebug else False
        self.func = self.og.getSnapshotAtMarketClose if isMarketClose else self.og.getSnapshotAtMarketOpen

    def symbolLoop(self, func, isDebug:bool):
        lineCount = 0
        symbols = set()
        for symbol in self.og.data.keys():
            lineCount += 1
            symbols.add(symbol)
            if (lineCount % 20 == 0):
                self.func(symbols)
            if (isDebug and lineCount % 20 == 0):
                print(lineCount)
        self.func(symbols)

    def Run(self):
        self.SystemLoop(self.func, self.isDebug)

    @staticmethod
    def All(isMarketClose:bool = None):
        app = LastNightGapper(isMarketClose, isDebug=True)
        app.Run()
        app.og.sa.WriteJson(app.data)


if __name__ == "__main__":
    # timeframe = RedisTimeFrame.DAILY
    # symbol = "AAPL"
    # app = LastNightGapper()
    # data = app.HistoricalPrices(symbol, timeframe)
    # app.WriteToFile(symbol, data)
    #
    LastNightGapper.All(True)
