from util import RedisTimeFrame
from .alpacaDally import AlpacaDaily
from .alpacaHistorical import AlpacaHistorical
from util import AlpacaAccess, RedisTimeFrame
from dbase import MarketDataDb
from threading import Thread


class YahooDaily(AlpacaDaily):

    def __init__(self, startdate=None, enddate=None, alpacaObject=None, symbolFile=None):
        symbolFile = './data/commodities.csv' if symbolFile is None else symbolFile
        super().__init__()
        self.datatype = 'commodity'
    #
    # override getDataLine to use CryptoPrices instead of HistroicalPrices
    #

    def getDataLine(self, app: AlpacaHistorical, symbol: str, db: MarketDataDb):
        try:
            timeframe = RedisTimeFrame.DAILY
            if self.startdate is not None and self.enddate is not None:
                data = app.CommodityPrices(
                    symbol, timeframe, starttime=self.startdate, endtime=self.enddate)
            else:
                data = app.CommodityPrices(symbol, timeframe)
            db.WriteMarket(symbol, data, datatype=self.datatype,
                           timeframe=timeframe)
        except Exception as e:
            print(e)

    def Run(self):
        symbols = self.getSymbolFile()
        symbolHistoricals, symbolSnapshots = self.db.StockSymbols(
            symbols, self.datatype)

        if symbolHistoricals:
            self.getHistorical(symbolHistoricals)
        # there is no snapshot for crypto.  just write historical data
        if symbolSnapshots:
            self.getHistorical(symbolHistoricals)

    @staticmethod
    def All():
        app = YahooDaily()
        app.Run()
