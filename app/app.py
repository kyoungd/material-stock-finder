import sys
from alpaca import Run, AlpacaSnapshots, AlpacaHistoricalData
from util import PushToServer
from study import *

from dbase import SecDb

def isTagInOptions(tag:str, cmds:list):
    return True if tag in cmds else False

if __name__ == "__main__":
    n = len(sys.argv)
    if isTagInOptions('--daily', sys.argv):
        Run()
        AlpacaSnapshots.All()
        AlpacaHistoricalData.All()
        StockFinancial.All(True)
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
        PushToServer()

    if isTagInOptions('--fn', sys.argv):
        StockFinancial.All(True)
        PushToServer()

    if isTagInOptions('--mc', sys.argv):
        LastNightGapper.All(True)

    if isTagInOptions('--mo', sys.argv):
        LastNightGapper.All(False)
        PushToServer()

    # db = SecDb()
    # db.SetLastDaily('AAPL', 170.33, '2020-01-28')
    # data = db.GetLastDaily('AAPL') 
    # print(data)
    # LastNightGapper.All("-s")
    print('done')
