import sys
import logging
import pandas as pd
from datetime import datetime
from alpaca import *
from util import PushToServer, SetInterval
from study import *
from dbase import *
from correlate import *

def isTagInOptions(tag:str, cmds:list):
    return True if tag in cmds else False

def AppDaily():
    Run()
    AlpacaSnapshots.All()
    AlpacaHistoricalData.All()
    StockFinancial.All(isDebug=True, isForceDownloadYahoo=False)
    RemoveNoDataStocks()
    FilterAtr.All()
    FilterEma.All()
    FilterKeyLevels.All()
    FilterFibonacciRetracement.All()
    FilterThreeBars.All()
    FilterRelativeVolume.All()
    FilterVolumeProfile.All()
    FilterGapper.All()
    FilterCandlePattern.All()
    FilterDoubleTop.All()
    FilterTrends.All()
    FilterRsiDivergence.All()
    FilterCorrelate.All()
    PushToServer()

def AppCorrelation():
    Run()
    AlpacaDaily.All()
    YahooDaily.All()
    AlpacaCrypto.All()
    AtrCalculate.All()
    CorrelateAssets.All(isSendToServer=True, days=45, minAtr=5)
    CorrelateAssets.All(isSendToServer=True, days=90, minAtr=5)
    CorrelateAssets.All(isSendToServer=True, days=180, minAtr=5)

def AppMarketOpen():
    LastNightGapper.All(False)
    PushToServer()

def RunApp():
    today = datetime.now()
    print(f'{today.hour} {today.minute}')
    if today.hour == 23 and today.minute == 50:
        AppDaily()
    elif today.hour == 5 and today.minute == 0:
        AppMarketOpen()
    elif today.hour == 5 and today.minute == 30:
        AppMarketOpen()
    elif today.hour == 6 and today.minute == 0:
        AppMarketOpen()


if __name__ == "__main__":
    formatter = '%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter,
                        datefmt='%d-%b-%y %H:%M:%S', filename="analyzer.log")
    logging.info("APP.PY Started")

    if isTagInOptions('--test', sys.argv):
        # Run()
        # AlpacaDaily.All()
        # YahooDaily.All()
        # AlpacaCrypto.All()
        AtrCalculate.All()
        # CorrelateAssets.All(isSendToServer=False, days=45, minAtr=5)
        # CorrelateAssets.All(isSendToServer=False, days=90, minAtr=5)
        # CorrelateAssets.All(isSendToServer=False, days=180, minAtr=5)

        # db = MarketDataDb()
        # db.WriteMarket('AAPL', [{'close': 120, 'open': 110}, {'close': 115, 'open': 105}], name='Apple, Inc.')
        # isOk, data = db.ReadMarket('AAPL')
        # df: pd.DataFrame = db.LoadDataFrame(data)
        # print(df)
    elif isTagInOptions('--corr', sys.argv):
        AppCorrelation()
    elif isTagInOptions('--day', sys.argv):
        AppDaily()
    elif isTagInOptions('--fin', sys.argv):
        StockFinancial.All(isDebug=True, isForceDownloadYahoo=True)
    else:
        SetInterval(60, RunApp)

    # db = SecDb()
    # db.SetLastDaily('AAPL', 170.33, '2020-01-28')
    # data = db.GetLastDaily('AAPL') 
    # print(data)
    # LastNightGapper.All("-s")
    logging.info('done')
