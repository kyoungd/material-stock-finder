from unittest import mock, TestCase
from study import FilterGapper
import pandas as pd


class TestFilterGappers(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def hi(self, c, o):
        return c + 1 if c > o else o + 1

    def lo(self, c, o):
        return c - 1 if c < o else o - 1
    
    def setupDf(self, 
                    c0, c1, c2, c3, c4, c5,
                    o0, o1, o2, o3, o4, o5):
        data = {'Date':
                ['2021-01-07T00:00:00.000000000', '2021-01-06T00:00:00.000000000',
                 '2021-01-05T00:00:00.000000000', '2021-01-04T00:00:00.000000000',
                 '2021-01-03T00:00:00.000000000', '2021-01-02T00:00:00.000000000'],
                'Close': [c0, c1, c2, c3, c4, c5],
                'Open': [o0, o1, o2, o3, o4, o5]
                }
        df = pd.DataFrame(data)
        high = []
        low = []
        for idx, row in df.iterrows():
            h = row['Close']+1 if row['Close'] > row['Open'] else row['Open']+1
            l = row['Close']-1 if row['Close'] < row['Open'] else row['Open']-1
            high.append(h)
            low.append(l)
        df['High'] = high
        df['Low'] = low
        return df

    def testOvernightGapperDown(self):
        df = self.setupDf(  
            90.1, 90.2, 90.3, 90.4, 102.5, 101.6,
            89.1, 89.2, 89.3, 89.4, 99.5, 101.6)
        filter = FilterGapper()
        _, gapDown = filter.filterOn(df)
        gapDown = filter.gapDownNearClose(gapDown, 92)
        gapDown = filter.gapDownPriceMovementCheck(gapDown, df)
        self.assertEqual(len(gapDown), 1)


    def testOvernightGapperUp(self):
        df = self.setupDf(
            100.1, 101.2, 100.3, 90.4, 90.5, 91.6,
            100.1, 101.2, 100.3, 90.4, 91.5, 91.6)
        filter = FilterGapper()
        gapUp, _ = filter.filterOn(df)
        gapUp = filter.gapUpNearClose(gapUp, 101)
        gapUp = filter.gapUpPriceMovementCheck(gapUp, df)
        self.assertEqual(len(gapUp), 1)

    def testOvernightGapperDown_Fail_SwingBack(self):
        df = self.setupDf(
            100.1, 101.2, 90.3, 90.4, 102.5, 101.6,
            101.1, 100.2, 89.3, 89.4, 99.5, 101.6)
        filter = FilterGapper()
        gaps = filter.overnightGapperLogic(df)
        self.assertEqual(len(gaps), 0)
        # _, gapDown = filter.filterOn(df)
        # gapDown = filter.gapDownNearClose(gapDown, 92)
        # gapDown = filter.gapDownPriceMovementCheck(gapDown, df)
        # self.assertEqual(len(gapDown), 0)

    def testOvernightGapperUp_Fail_SwingBack(self):
        df = self.setupDf(
            90.1, 101.2, 100.3, 90.4, 90.5, 91.6,
            90.1, 101.2, 100.3, 90.4, 91.5, 91.6)
        filter = FilterGapper()
        gaps = filter.overnightGapperLogic(df)
        self.assertEqual(len(gaps), 0)
        # gapUp, _ = filter.filterOn(df)
        # gapUp = filter.gapUpNearClose(gapUp, 101)
        # gapUp = filter.gapUpPriceMovementCheck(gapUp, df)
        # self.assertEqual(len(gapUp), 0)
