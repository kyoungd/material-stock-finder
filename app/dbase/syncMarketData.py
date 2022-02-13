import logging
from .marketData import MarketDataDb

class SynchronizeMarketData:
    def __init__(self, data):
        self.db = MarketDataDb
        result = self.db.ReadMarket('AAPL', 'stock', '1Day')
        self.home = result[0][::-1]
        self.data = data[::-1]

    def sychronize(self, home, data):
        logging.info('SynchronizeMarketData.sychronize')
        syncValues = []
        ixHome = 0
        lastValue = None
        for ixData in range(len(data)):
            if lastValue is None:
                if data[ixData]['t'] == home[ixHome]['t']:
                    lastValue = data[ixData]['t']
            elif data[ixData]['t'] == home[ixHome]['t']:
                lastValue = data[ixData]['t']
                syncValues.append(lastValue)
            else:
                lastValue['t'] = data[ixData]['t']
                syncValues.append(lastValue)
        return syncValues

    def Run(self, data=None):
        data = self.data if data is None else data
        if len(data) == len(self.home):
            return self.data
        self.data = self.sychrnorize(self.home, data)
        return self.data[::-1]
