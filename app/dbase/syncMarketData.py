import copy
import logging
from .marketData import MarketDataDb

class SynchronizeMarketData:
    def __init__(self, data):
        try:
            self.db = MarketDataDb()
            _, result = self.db.ReadMarket(symbol='AAPL', datatype='stock', timeframe='1Day')
            self.home = result[0][::-1]
            self.data = data[::-1]
        except Exception as e:
            logging.error(f'SynchronizeMarketData.__init__: {e}')
            print(e)

    def startIndex(self, home, data):
        ixHome = 0
        ixData = 0
        while ixHome < len(home) and ixData < len(data):
            if data[ixData]['t'] < home[ixHome]['t']:
                ixData += 1
            elif data[ixData]['t'] > home[ixHome]['t']:
                ixHome += 1
            else:
                break
        return ixHome, ixData

    def synchronize(self, home, data):
        try:
            syncValues = []
            ixHome, ixData = self.startIndex(home, data)
            lastValue = data[ixData]
            ixLastData = len(data) - 1
            while ixHome < len(home):
                if ixData >= ixLastData:
                    lastValue['t'] = home[ixHome]['t']
                    syncValues.append(copy.deepcopy(lastValue))
                    ixHome += 1
                elif data[ixData]['t'] == home[ixHome]['t']:
                    lastValue = data[ixData]
                    syncValues.append(copy.deepcopy(lastValue))
                    ixData += 1
                    ixHome += 1
                elif data[ixData]['t'] < home[ixHome]['t']:
                    lastValue['t'] = home[ixHome]['t']
                    syncValues.append(copy.deepcopy(lastValue))
                    ixHome += 1
                else:
                    lastValue = data[ixData]
                    ixData += 1
            return syncValues
        except Exception as e:
            logging.error(f'SynchronizeMarketData.synchronize: {e}')
            print(e)

    def Run(self, data=None):
        data = self.data if data is None else data
        if len(data) == len(self.home):
            return self.data
        result = self.synchronize(self.home, data)
        return result[::-1]
