import sys
import logging
from datetime import datetime
from alpaca import Run, AlpacaSnapshots, AlpacaHistoricalData
from util import PushToServer, SetInterval
from study import *
from dbase import SecDb

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
    PushToServer()

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
        FilterRsiDivergence.All()
    elif isTagInOptions('--run', sys.argv):
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
