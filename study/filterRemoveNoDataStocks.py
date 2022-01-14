from allstocks import AllStocks

def isLoadFile(symbol):
    isLoaded, tp = AllStocks.GetDailyStockData(symbol)
    return isLoaded

if __name__ == '__main__':
    AllStocks.Run(isLoadFile, isSymbolsRewrite=True)
