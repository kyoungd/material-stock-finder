from alpaca_trade_api.rest import REST
import json
import os
from allstockanalysis import StockAnalysis
from alpacaUtil import AlpacaAccess


class LastNightGaoper:
    CsvHeader = "Date, Open, High, Low, Close, Adj Close, Volume"
    conn: REST = None

    def __init__(self):
        self.sa = StockAnalysis()
        self.data = self.sa.GetJson

    def getLastNightGapper(self, price1, price2):
        priceMin = float(os.environ.get('OG_MIN_PERCENT', '0.30'))
        percentMin = float(os.environ.get('OG_MIN_PERCENT', '0.03'))
        priceMoveValue = abs(price2 - price1)
        priceMovePercent = priceMoveValue / price1
        if (priceMovePercent > percentMin) and (priceMoveValue > priceMin):
            return True
        else:
            return False

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

    def getSnapshot(self, symbols):
        snapshots = self.getSnapshotFromApi(symbols)
        for symbol in snapshots.keys():
            try:
                price1 = float(snapshots[symbol]['prevDailyBar']['c'])
                price2 = float(snapshots[symbol]['minuteBar']['c'])
                isOvernightGapper = self.getLastNightGapper(
                    price1, price2)
                self.sa.UpdateFilter(
                    self.data, symbol, 'lng', isOvernightGapper)
            except Exception as e:
                try:
                    print('ERROR: ' + symbol + ': ' +
                          str(e) + str(data.status_code))
                    self.sa.UpdateFilter(self.data, symbol, 'lng', False)
                except Exception as e:
                    print(e)
                    pass

    def Run(self, filename=None, isDebug=False):
        lineCount = 0
        symbols = set()
        for symbol in self.data.keys():
            lineCount += 1
            symbols.add(symbol)
            if (lineCount % 20 == 0):
                self.getSnapshot(symbols)
                symbols.clear()
            if (isDebug and lineCount % 20 == 0):
                print(lineCount)
        self.getSnapshot(symbols)
        self.sa.WriteJson(app.data)


if __name__ == "__main__":
    # timeframe = RedisTimeFrame.DAILY
    # symbol = "AAPL"
    # app = LastNightGaoper()
    # data = app.HistoricalPrices(symbol, timeframe)
    # app.WriteToFile(symbol, data)
    #
    app = LastNightGaoper()
    app.Run(isDebug=True)
    #
    print('done')
