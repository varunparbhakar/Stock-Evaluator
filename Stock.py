import datetime
class Stock:
    BOND_10_Yr_Yield = 0.0232
    EXPECTED_RETURN_IN_MARKET = 0.1
    PERPETUAL_GROWTH_RATE = 0.025
    VALUE_SAFETY_MARGIN = 0.07



    def __init__(self, theName, thePrice):
        self.name = theName
        self.price = thePrice
        self.lastUpdate = datetime.date.today()

    def getName(self):
        return (self.name)
    def getPrice(self):
        return self.price

    def getLastUpdate(self):
        return self.lastUpdate


appleStock = Stock("Apple", 145)
print(appleStock.getLastUpdate())

for x in range(5):
    print(x+1)