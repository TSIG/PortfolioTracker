
class Stock:
    sharesBought = 0
    valuePerShareAtPurchase = 0
    percentageOfPortfolio = 0
    equityValue = 0
    totalSpent = 0
    ticker = ''

    def __init__(self,sharesBought, valuePerShare, ticker, Portfolio):
        self.sharesBought = sharesBought
        self.valuePerShareAtPurchase = valuePerShare
        self.ticker = ticker
        self.equityValue = (valuePerShare * sharesBought)
        self.totalSpent = (valuePerShare * sharesBought)


    def getTicker(self):
        return self.ticker

    def getValuePerShareAtPurchase(self):
        return self.valuePerShareAtPurchase

    def getPercentageOfPortfolio(self):
        return self.percentageOfPortfolio

    def calculatePercentageOfPorfolio(self, Portfolio):
        self.percentageOfPortfolio = (self.equityValue/Portfolio.getValueOfPortfolio())*100
        return self.percentageOfPortfolio

    def getTotalSpent(self):
        return self.totalSpent

    def getEquityValue(self):
        return self.equityValue

    def setEquityValue(self, stockPrice):
        self.equityValue = (float(stockPrice) * float(self.sharesBought))

    def getShares(self):
        return self.sharesBought

    def setShares(self, sharesBought):
        self.sharesBought = sharesBought

    def addToSharesBought(self, sharesBought):
        self.sharesBought += sharesBought

    def getReturns(self):
        return (1 - (self.getTotalSpent()/self.getEquityValue()))*100

