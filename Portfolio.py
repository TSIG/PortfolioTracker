import time

class Portfolio:
    totalAmountInvested = 0
    portfolioValue = 0
    sharesOutstanding = 0
    portfolioPerformance = 0
    listOfStocks = {}
    historicalList = {}

    def __init__(self):
        print ("Created Portfolio")

    def getTotalAmountInvested(self):
        return self.totalAmountInvested;

    def addToTotalAmountInvested(self, amount):
        self.totalAmountInvested += amount

    def addStockToPortfolio(self, Stock):
        self.addToTotalAmountInvested(Stock.getTotalSpent())
        self.addToPortfolioValue(Stock.getEquityValue())
        self.listOfStocks.update({Stock.ticker : Stock})

    def getValueOfPortfolio(self):
        return self.portfolioValue

    def addToPortfolioValue(self, value):
        self.portfolioValue += value

    def getListOfStocks(self):
        return self.listOfStocks

    def refreshWeights(self):
        for stock in self.listOfStocks:
            self.listOfStocks[stock].calculatePercentageOfPorfolio(self)


    def getCurrentData(self):
        self.portfolioValue = 0
        for stock in self.listOfStocks:
            time.sleep(.5)
            self.listOfStocks[stock].setEquityValue(gf.getQuotes(stock)[0]['LastTradePrice'])
        self.refreshWeights()
        self.portfolioPerformance = (1 - (self.totalAmountInvested / self.portfolioValue)) * 100

    def showReturns(self):
        self.getCurrentData()






