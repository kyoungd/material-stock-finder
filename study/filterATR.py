import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import talib
import os
from datetime import date
from allstocks import AllStocks


class FilterATR:
    def __init__(self, isFilter):
        self.atrTimeperiod = int(os.environ.get('ATR_TIME_PERIOD', '14'))
        self.atrMovementBars = int(os.environ.get('ATR_MOVEMENT_BARS', '30'))
        self.atrMovementPercent = int(
            os.environ.get('ATR_MOVEMENT_PERCENT', '5'))
        self.isFilter = isFilter

    def filterOn(self, tp):
        high = tp.High.to_numpy()
        low = tp.Low.to_numpy()
        close = tp.Close.to_numpy()
        output = talib.ATR(high[::-1], low[::-1], close[::-1], timeperiod=14)
        end = len(output)
        start = end - self.atrTimeperiod
        avgValue = np.mean(output[start:end])
        lastValue = output[-1]

    def Run(self, symbol):
        isLoaded, tp = AllStocks.GetDailyStockData(symbol)
        if isLoaded:
            self.filterOn(tp)
        return isLoaded

    @staticmethod
    def All():
        filter = FilterATR()
        AllStocks.Run(filter.Run, False)


if __name__ == '__main__':
    FilterATR.All()
    # filter = FilterKeyLevels()
    # result = filter.Run('AAPL')
    # print(result)
