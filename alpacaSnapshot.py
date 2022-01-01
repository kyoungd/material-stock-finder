
from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime, timedelta
from enum import Enum
import alpaca_trade_api as tradeapi
import requests
from alpacaUtil import AlpacaAccess, RedisTimeFrame
import json
import os
import threading
from threading import Thread
import time

custom_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
response = requests.get('https://www.dev2qa.com', headers=custom_header)


class TimePeriod(Enum):
    REALTIME = "0"
    Min1 = "1Min"
    Min5 = "5Min"
    Min10 = "10Min"
    Min15 = "15Min"
    Min30 = "30Min"
    Hour = "Hour"
    Hour4 = "4Hour"
    Day = "Day"
    Week = "Week"


class AlpacaSnapshots:
    ALPACA_URL = 'https://data.alpaca.markets/v2/stocks/snapshots?symbols=%s'
    CsvHeader = "Date, Open, High, Low, Close, Adj Close, Volume"
    conn: REST = None

    def __init__(self, minPrice=None, maxPrice=None, minVolume=None, maxVolume=None):
        self.custom_header = AlpacaAccess.CustomHeader()
        self.MinPrice = minPrice if minPrice is not None else int(os.environ.get(
            'MIN_PRICE', '20'))
        self.MaxPrice = maxPrice if maxPrice is not None else int(os.environ.get(
            'MAX_PRICE', '1000'))
        self.MinVolume = minVolume if minVolume is not None else int(os.environ.get(
            'MIN_VOLUME', '1000000'))
        self.MaxVolume = maxVolume if maxVolume is not None else int(os.environ.get(
            'MAX_VOLUME', '2000000000'))

    def HistoricalSnapshots(self, symbols):
        # split set into a string of symbols separated by commas
        symbolsString = ','.join(s for s in symbols)
        url = AlpacaSnapshots.ALPACA_URL % (
            symbolsString)
        snapshots = requests.get(url, headers=self.custom_header)
        return snapshots

    def withinPriceVolumeRange(self, price, volume, minPrice, maxPrice, minVolume, maxVolume):
        if (price < minPrice):
            return False
        elif (price > maxPrice):
            return False
        elif (volume < minVolume):
            return False
        elif (volume > maxVolume):
            return False
        else:
            return True

    def getSnapshot(self, symbols, dicts):
        app = AlpacaSnapshots()
        data = app.HistoricalSnapshots(symbols)
        if (data.status_code == 422):
            removeSymbols = json.loads(data.text)['message'].split(':')[1]
            rejectedSymbols = set()
            for symbol in removeSymbols.strip().split(','):
                rejectedSymbols.add(symbol)
                dicts.pop(symbol)
            symbolList = symbols.difference(rejectedSymbols)
            data = app.HistoricalSnapshots(symbolList)
        snapshots = json.loads(data.text)
        symbols = ''
        for symbol in snapshots.keys():
            try:
                price = snapshots[symbol]['dailyBar']['c']
                volume = snapshots[symbol]['dailyBar']['v']
                if not self.withinPriceVolumeRange(price, volume, self.MinPrice, self.MaxPrice, self.MinVolume, self.MaxVolume):
                    dicts.pop(symbol)
            except Exception as e:
                print('ERROR: ' + symbol + ': ' +
                      str(e) + str(data.status_code))
                try:
                    dicts.pop(symbol)
                except Exception as e:
                    pass

    def Run(self, filename=None, isDebug=False):
        filename = './data/symbols.csv' if filename == None else filename
        with open(filename, 'r') as f:
            lines = f.readlines()
            # print(lines)
        dicts = {}
        for line in lines[1:]:
            dicts[line.split(',')[0]] = line.split(',')[1].strip('\n')
        lineCount = 0
        symbols = set()
        for line in lines[1:]:
            lineCount += 1
            symbol = line.split(',')[0]
            symbols.add(symbol)
            if (lineCount % 20 == 0):
                self.getSnapshot(symbols, dicts)
                symbols.clear()
                if (isDebug):
                    print(lineCount)
        self.getSnapshot(symbols, dicts)
        with open(filename, "w") as fw:
            for key in dicts.keys():
                content = dicts[key].strip('\n')
                fw.write('{},{}\n'.format(key, content))


if __name__ == "__main__":
    # timeframe = RedisTimeFrame.DAILY
    # symbol = "AAPL"
    # app = AlpacaSnapshots()
    # data = app.HistoricalPrices(symbol, timeframe)
    # app.WriteToFile(symbol, data)
    #
    app = AlpacaSnapshots()
    app.Run(isDebug=True)
    #
    print('done')
