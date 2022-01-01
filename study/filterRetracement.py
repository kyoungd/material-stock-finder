from allstocks import AllStocks
from filterFibonachiRetracement import fibonachiRetracement, FilterFibonachiRetracement
from filterThreeBars import FilterThreeBars


class FilterRetracement:

    @staticmethod
    def Run(symbol):
        resultFibonachi = FilterFibonachiRetracement().Run(symbol)
        resultThreeBars = FilterThreeBars().Run(symbol)
        return resultFibonachi or resultThreeBars

    @staticmethod
    def All():
        AllStocks.Run(FilterRetracement.Run, True)


if __name__ == '__main__':
    FilterRetracement.All()
