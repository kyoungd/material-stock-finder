import talib
from threading import Thread
from dbase import MarketDataDb
import pandas as pd
import numpy as np
import json

class CorrelateAssets():

    def __init__(self, days = None, minAtr = None):
        days = 90 if days is None else days
        minAtr = 7.5 if minAtr is None else minAtr
        self.db = MarketDataDb()
        if days == 45:
            self.period = 30
            self.colume = 'atr45'
        elif days == 90:
            self.period = 60
            self.colume = 'atr90'
        elif days == 180:
            self.period = 120
            self.colume = 'atr120'
        else:
            self.period = 30
            self.colume = 'atr45'
        self.minAtr = minAtr

    def buildCorrelationTable(self, results):
        df = pd.DataFrame()
        lastIx = 0
        for item in results:
            symbol, data = item
            item_df = pd.DataFrame(data)
            closes = item_df.c
            closes = closes.pct_change()
            close = closes.to_numpy()[0:self.period]
            df.insert(lastIx, symbol,close)
            lastIx += 1
        return df

    def getSymbols(self):
        sql = f'SELECT symbol, data FROM public.market_data WHERE timeframe=%s AND {self.colume}>=%s AND NOT is_deleted'
        params = (MarketDataDb.DefaultTimeframe(), self.minAtr)
        return self.db.SelectQuery(sql, params)

    def Run(self):
        isOk, symbols = self.getSymbols()
        df = self.buildCorrelationTable(symbols)
        results = df.corr(method='pearson')
        correlates = []
        inverses = []
        for _, row in results.iterrows():
            correlate = row.where(lambda x: x >= 0.75).dropna()
            inverse = row.where(lambda x: x <= -0.75).dropna()
            correlates.append(correlate)
            inverses.append(inverse)
        df_correlates = pd.DataFrame(correlates)
        df_inverses = pd.DataFrame(inverses)
        json_correlates = df_correlates.to_json()
        json_inverses = df_inverses.to_json()
        print(correlates)
        print(inverses)

            
    @staticmethod
    def All():
        app = CorrelateAssets(days=90, minAtr=5)
        app.Run()
