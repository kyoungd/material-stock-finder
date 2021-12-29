import pandas as pd
import os


class AllStocks:

    @staticmethod
    def Run(func, isSymbolsRewrite=False, filename=None):
        filename = './data/symbols.csv' if filename == None else filename
        with open(filename, 'r') as f:
            lines = f.readlines()
            # print(lines)
        dicts = {}
        for line in lines[1:]:
            dicts[line.split(',')[0]] = line.split(',')[1].strip('\n')
        for line in lines[1:]:
            symbol = line.split(',')[0]
            filterOk = func(symbol)
            if not filterOk:
                dicts.pop(symbol)
        if isSymbolsRewrite:
            with open(filename, "w") as fw:
                for key in dicts.keys():
                    fw.write('{},{}\n'.format(key, dicts[key]))

    @staticmethod
    def stockFile(symbol):
        datapath = os.environ.get(
            'STOCK_DATA_PATH', './data/stocks')
        return datapath + '/' + symbol + '.csv'

    @staticmethod
    def GetDailyStockData(symbol):
        try:
            filename = AllStocks.stockFile(symbol)
            df = pd.read_csv(filename)
            df.rename(columns={' Open': 'Open',
                               ' High': 'High', ' Low': 'Low', ' Close': 'Close', ' Volume': 'Volume', ' Adj Close': 'Adj Close'}, inplace=True)
            return True, df
        except Exception as e:
            print(e)
            return False, None

    @staticmethod
    def GetWeeklyStockData(symbol):
        isLoadedOk, df = AllStocks.GetDailyStockData(symbol)
        if not isLoadedOk:
            return False, None
        print(df)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)

        def take_first(array_like):
            return array_like[0]

        def take_last(array_like):
            return array_like[-1]
        how = {'Open': 'first',
               'High': 'max',
               'Low': 'min',
               'Close': 'last',
               'Adj Close': 'last',
               'Volume': 'sum'}
        output = df.resample('W').agg(how)

        # output = df.resample('W',                                 # Weekly resample
        #                      how={'Open': take_first,
        #                           'High': 'max',
        #                           'Low': 'min',
        #                           'Close': take_last,
        #                           'Adj Close': take_last,
        #                           'Volume': 'sum'},
        #                      loffset=pd.offsets.timedelta(days=-6))  # to put the labels to Monday

        output = output[['Open', 'High', 'Low',
                         'Close', 'Adj Close', 'Volume']]
        return output


if __name__ == '__main__':
    result = AllStocks.GetWeeklyStockData('AAPL')
    print(result)
