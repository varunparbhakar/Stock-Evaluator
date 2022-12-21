from datetime import datetime
class Stock:



    def __init__(self, name):
        self.Name = name
        self.lastUpdated = datetime.now()


    def getName(self):
        return self.Name
    def getLastUpdated(self):
        return self.lastUpdated
    def getTicker(self):
        return self.Ticker

