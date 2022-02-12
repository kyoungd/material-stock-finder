import yfinance as yf

class YahooFin:

    @staticmethod
    def HistoricalPrices(symbol, timeframe=None):
        timeframe = '1y' if timeframe is None else timeframe.lower()
        stock = yf.Ticker(symbol)

        hist = stock.history(period=timeframe)
        # show actions (dividends, splits)
        stock.actions

        result = []
        for _, row in hist.iterrows():
            print(str(row.name))
            result.append({'t': str(row.name), 'o': row.Open, 'h': row.High,
                           'l': row.Low, 'c': row.Close, 'v': row.Volume})
        print(result[::-1])
        return result[::-1]

    @staticmethod
    def SnapshotPrices(symbol, timeframe=None):
        timeframe = '1day' if timeframe is None else timeframe.lower()
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1day")
        for _, row in hist.iterrows():
            return {'t': str(row.name), 'o': row.Open, 'h': row.High, 'l': row.Low, 'c': row.Close, 'v': row.Volume}
