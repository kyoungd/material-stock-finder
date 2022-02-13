import logging
from util import RedisTimeFrame
from .alpacaDally import AlpacaDaily
from .alpacaHistorical import AlpacaHistorical
from util import AlpacaAccess, RedisTimeFrame
from dbase import MarketDataDb, SynchronizeMarketData
from threading import Thread


class YahooDaily(AlpacaDaily):

    def __init__(self, startdate=None, enddate=None, alpacaObject=None, symbolFile=None):
        symbolFile = './data/commodity.csv' if symbolFile is None else symbolFile
        super().__init__(startdate=None, enddate=None, alpacaObject=None, symbolFile=symbolFile)
        self.datatype = 'commod'
    #
    # override getDataLine to use CryptoPrices instead of HistroicalPrices
    #

    def getDataLine(self, app: AlpacaHistorical, symbol: str, db: MarketDataDb):
        try:
            logging.info(f'YahooDaily.getDataLine: {symbol}')
            timeframe = RedisTimeFrame.DAILY
            if self.startdate is not None and self.enddate is not None:
                data = app.CommodityPrices(
                    symbol, timeframe, starttime=self.startdate, endtime=self.enddate)
            else:
                data = app.CommodityPrices(symbol, timeframe)
            sync = SynchronizeMarketData(data)
            mdata = sync.Run()
            db.WriteMarket(symbol, mdata, datatype=self.datatype,
                           timeframe=timeframe)
        except Exception as e:
            logging.error(f'YahooDaily.getDataLine: {symbol} - {e}')
            print(e)

    def Run(self):
        logging.info('YahooDaily.Run')
        symbols = self.getSymbolFile()
        symbolHistoricals, symbolSnapshots = self.db.StockSymbols(
            symbols, self.datatype)

        if symbolHistoricals:
            self.getHistorical(symbolHistoricals)
        # there is no snapshot for crypto.  just write historical data
        if symbolSnapshots:
            self.getHistorical(symbolSnapshots)

    @staticmethod
    def All():
        logging.info('Running YahooDaily.All')
        app = YahooDaily()
        app.Run()
