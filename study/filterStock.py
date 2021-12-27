import pandas as pd
from keylevels import KeyLevels
import os


class filterStock:
    def __init__(self, symbol=None, filter=''):
        self.symbol = symbol
        self.filter = filter
        self.datapath = os.environ.get(
            'STOCK_DATA_PATH', './data/stocks')

    def stockFile(self, symbol):
        return self.datapath + '/' + symbol + '.csv'

    def Run(self, symbol=None, filter=None):
        symbol = self.symbol if symbol is None else symbol
        filter = self.filter if filter is None else filter
        filename = self.stockFile(symbol)
        df = pd.read_csv(filename)
        print(df)


if __name__ == '__main__':
    filter = filterStock().Run('AAPL')
    filter.Run()
