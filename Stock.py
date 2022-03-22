import datetime
class Stock:
    BOND_10_Yr_Yield = 0.0232
    EXPECTED_RETURN_IN_MARKET = 0.1
    PERPETUAL_GROWTH_RATE = 0.025
    VALUE_SAFETY_MARGIN = 0.07


    def __init__(self, theStockArray):
        self.list = theStockArray

    def getName(self):
        return self.list[0]

    def getTicker(self):
        return self.list[1]

    def getPrice(self):
        return self.list[2]

    def getLastUpdated(self):
        return self.list[3]

    def getFreeCashFlowToEquity_CURRENT_YEAR(self):
        return self.list[4]

