import talib
from threading import Thread
from dbase import MarketDataDb
import pandas as pd
import numpy as np

class AtrCalculate():
    
    def __init__(self, startdate=None, enddate=None, alpacaObject = None, symbolFile = None):
        self.db = MarketDataDb()

    def getAtr(self, df, period):
        high = df.h.to_numpy()[0:period]
        low = df.l.to_numpy()[0:period]
        close = df.c.to_numpy()[0:period]
        price = close[0]
        atrDollar = talib.ATR(high[::-1], low[::-1], close[::-1], timeperiod=period-1)
        atr = atrDollar[-1] / price
        return 0 if pd.isna(atrDollar[-1]) else round(atr * 100, 2)

    def atrCalculation(self, data):
        df = pd.DataFrame(data)
        atr45 = self.getAtr(df, 30)
        atr90 = self.getAtr(df, 60)
        atr180 = self.getAtr(df, 120)
        return (atr45, atr90, atr180)

    def ProcessAtr(self, symbols):
        for item in symbols:
            try:
                id, data = item
                atr45, atr90, atr180 = self.atrCalculation(data)
                self.db.UpdateAtr(id, atr45, atr90, atr180)
            except Exception as e:
                print(e)

    def Run(self):
        sql = """SELECT id, data FROM public.market_data WHERE timeframe = %s AND NOT is_deleted"""
        params = (MarketDataDb.DefaultTimeframe(),)
        isOk, results = self.db.SelectQuery(sql, params)
        if isOk:
            self.ProcessAtr(results)
        return isOk

    @staticmethod
    def All():
        app = AtrCalculate()
        app.Run()
