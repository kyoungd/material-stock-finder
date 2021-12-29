import pandas as pd
from study.filterKeylevels import FilterKeyLevels
import os
from allstocks import AllStocks, GetDailyStockData, GetWeeklyStockData


class filterStock:
    def __init__(self, symbol=None, filter=''):
        self.symbol = symbol
        self.filter = filter

    def filterStock(self, symbol=None):
        symbol = self.symbol if symbol is None else symbol
        filter = FilterKeyLevels()
        return filter.Run(symbol)


if __name__ == '__main__':
    filter = filterStock()
    AllStocks.Run(filter.filterStock, True)
