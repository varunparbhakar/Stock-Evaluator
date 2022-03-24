import json
from Attributes import Attribute

from selenium import webdriver


class Scraper:
    def __init__(self, theStock):
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.TICKER = theStock
        self.driver = webdriver.Chrome(PATH)
        print("Scraper has been initialized")

    def initializeStock(self, theStock):
        # sds =              "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[3]/div[1]/div/div[2]/div[8]/div[1]/div[3]/span"
        #
        # cashFlow_Current = "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[3]/div[1]/div/div[2]/div[11]/div[1]/div[3]/span"
        #
        # cashFlow_LastYear = "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[3]/div[1]/div/div[2]/div[11]/div[1]/div[4]/span"
        #
        # cashFlow_2_YearsAgo = "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[3]/div[1]/div/div[2]/div[11]/div[1]/div[5]/span"
        #
        # cashFlow_3_YearsAgo = "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[3]/div[1]/div/div[2]/div[11]/div[1]/div[6]/span"

        Scraper.freeCashFlow(self.TICKER, self.driver)




        # print("Current Year",number.text)
        # number = driver.find_element_by_xpath(cashFlow_LastYear)
        # print("2020 year", number.text)
        # number = driver.find_element_by_xpath(cashFlow_2_YearsAgo)
        # print("2019", number.text)
        # number = driver.find_element_by_xpath(cashFlow_3_YearsAgo)
        # print("2018", number.text)

        self.driver.close()


    def getFreeCashFlow(self):
        self.driver.get("https://finance.yahoo.com/quote/{}/cash-flow?p={}".format(self.TICKER, self.TICKER))
        self.driver.implicitly_wait(5)

        # Working Free cash flow Address 10:56 PM 22 March "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[4]/div[1]/div[1]/div[2]"

        # Getting the main Class = "D(tbrg))
        webElement = self.driver.find_element_by_xpath("//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[4]/div[1]/div[1]/div[2]")

        freeCashFlowList = self.stringParser(webElement.text, Attribute.FREE_CASH_FLOW_OFFSET)
        print("Free Cash flow of", self.TICKER, "is", freeCashFlowList)



    def getTotalDebt(self):
        self.driver.get("https://finance.yahoo.com/quote/{}/balance-sheet?p={}".format(self.TICKER, self.TICKER))
        self.driver.implicitly_wait(5)

        # Working Free cash flow Address 10:56 PM 22 March "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[4]/div[1]/div[1]/div[2]"

        # Getting the main Class = "D(tbrg))
        webElement = self.driver.find_element_by_xpath("//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[4]/div[1]/div[1]/div[2]")

        totalDebt = self.stringParser(webElement.text, Attribute.TOTAL_DEBT_OFFSET)
        print("Free Cash flow of", self.TICKER, "is", totalDebt)

    def getTotalRevenue(self):
        self.driver.get("https://finance.yahoo.com/quote/{}/financials?p={}".format(self.TICKER, self.TICKER))
        self.driver.implicitly_wait(5)


        # Working Free cash flow Address 10:56 PM 22 March "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[4]/div[1]/div[1]/div[2]"




        # Getting the main Class = "D(tbrg))
        webElement = self.driver.find_element_by_xpath("//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[4]/div[1]/div[1]/div[2]")
        print(webElement.text)

        revenueList = self.stringParser(webElement.text, Attribute.REVENUE_OFFSET)
        print("Revenue of", self.TICKER, "is", revenueList)




    def stringParser(self, theString, dataType):
        """
        Takes the stringBlock from the webElement and the dataType that the
        user wants to extract and return a list with data from 5 periods
        such as [TTM, CURRENT YEAR, C_Y - 1, C_Y - 2, C_Y - 3]

        EX: A String like : Free Cash Flow
        101,853,000 92,953,000 -73,365,000 58,896,000 64,121,000

        will return [101853000, 92953000, -73365000, 58896000, 64121000]
        :param theString:
        :param dataType:
        :return:
        """
        myStringList = list(theString)

        solutionList = None  # Storing the solution list

        # Checking fot Free Cash Flow
        if (dataType == Attribute.FREE_CASH_FLOW_OFFSET):
            # The purpose of this offset is when we send the list to another method
            # we want to make sure that the other method doesn't receive the word inside the list
            stringOffSet = Attribute.FREE_CASH_FLOW_OFFSET.value + 1

            currentCounter = 0

            while (currentCounter < len(myStringList)):
                character = "" + myStringList[currentCounter]
                if (character.isupper()):
                    if (self.freeCashFlowStringChecker(myStringList[currentCounter:])):
                        # Only sending the part of the list that has the data not the word itself
                        solutionList = self.dataExtractor(myStringList[currentCounter + stringOffSet:])

                        break
                currentCounter += 1


        # Checking fot Operating Cash Flow
        elif (dataType == Attribute.OPERATING_CASH_FLOW_OFFSET):
            # The purpose of this offset is when we send the list to another method
            # we want to make sure that the other method doesn't receive the word inside the list
            stringOffSet = Attribute.OPERATING_CASH_FLOW_OFFSET.value + 1
            currentCounter = 0
            while (currentCounter < len(myStringList)):
                character = "" + myStringList[currentCounter]
                if (character.isupper()):

                    if (self.operatingCashFlowStringChecker(myStringList[currentCounter:])):
                        # Only sending the part of the list that has the data not the word itself
                        solutionList = self.dataExtractor(myStringList[currentCounter + stringOffSet:])

                        break
                currentCounter += 1


        # Checking fot Total Revenue
        elif (dataType == Attribute.REVENUE_OFFSET):
            # The purpose of this offset is when we send the list to another method
            # we want to make sure that the other method doesn't receive the word inside the list
            stringOffSet = Attribute.REVENUE_OFFSET.value + 1
            currentCounter = 0
            while (currentCounter < len(myStringList)):
                character = "" + myStringList[currentCounter]
                if (character.isupper()):

                    if (self.revenueStringChecker(myStringList[currentCounter:])):
                        # Only sending the part of the list that has the data not the word itself
                        solutionList = self.dataExtractor(myStringList[currentCounter + stringOffSet:])

                        break
                currentCounter += 1

        # Checking fot Capital Expenditure
        elif (dataType == Attribute.CAPITAL_EXPENDITURE_OFFSET):
            # The purpose of this offset is when we send the list to another method
            # we want to make sure that the other method doesn't receive the word inside the list
            stringOffSet = Attribute.CAPITAL_EXPENDITURE_OFFSET.value + 1
            currentCounter = 0
            while (currentCounter < len(myStringList)):
                character = "" + myStringList[currentCounter]
                if (character.isupper()):

                    if (self.capitalExpenditureStringChecker(myStringList[currentCounter:])):
                        # Only sending the part of the list that has the data not the word itself
                        solutionList = self.dataExtractor(myStringList[currentCounter + stringOffSet:])

                        break
                currentCounter += 1

            # Checking fot Total Debt
        elif (dataType == Attribute.TOTAL_DEBT_OFFSET):
            # The purpose of this offset is when we send the list to another method
            # we want to make sure that the other method doesn't receive the word inside the list
            stringOffSet = Attribute.TOTAL_DEBT_OFFSET.value + 1
            currentCounter = 0
            while (currentCounter < len(myStringList)):
                character = "" + myStringList[currentCounter]
                if (character.isupper()):

                    if (self.totalDebtStringChecker(myStringList[currentCounter:])):
                        # Only sending the part of the list that has the data not the word itself
                        solutionList = self.dataExtractor(myStringList[currentCounter + stringOffSet:])

                        break
                currentCounter += 1




        # Checking if the list is empty
        if (len(solutionList) == None):
            TypeError: "The solution list is empty or has not been filled in correctly"

        return solutionList

    def freeCashFlowStringChecker(self, theList):
        """
        This method verifies that the passed in string has the correct title.
        The list passed into the method has to start at the word otherwise this method will declare it wrong.
        :param theList:
        :return: Boolean
        """
        if (len(theList) == 0):
            TypeError: "The passed in list is empty"

        # Assuming the list starts at the word
        myString = "".join(theList[:Attribute.FREE_CASH_FLOW_OFFSET.value])

        return (myString == "Free Cash Flow")

    def totalDebtStringChecker(self, theList):
        """
        This method verifies that the passed in string has the correct title.
        The list passed into the method has to start at the word otherwise this method will declare it wrong.
        :param theList:
        :return: Boolean
        """
        if (len(theList) == 0):
            TypeError: "The passed in list is empty"

        # Assuming the list starts at the word
        myString = "".join(theList[:Attribute.TOTAL_DEBT_OFFSET.value])

        return (myString == "Total Debt")



    def operatingCashFlowStringChecker(self, theList):
        """
            This method verifies that the passed in string has the correct title.
            The list passed into the method has to start at the word otherwise this method will declare it wrong.
            :param theList:
            :return: Boolean
            """

        if (len(theList) == 0):
            TypeError: "The passed in list is empty"

        # Assuming the list starts at the word
        myString = "".join(theList[:Attribute.OPERATING_CASH_FLOW_OFFSET.value])

        return (myString == "Operating Cash Flow")


    def capitalExpenditureStringChecker(self, theList):
        """
            This method verifies that the passed in string has the correct title.
            The list passed into the method has to start at the word otherwise this method will declare it wrong.
            :param theList:
            :return: Boolean
            """

        if (len(theList) == 0):
            TypeError: "The passed in list is empty"

        # Assuming the list starts at the word
        myString = "".join(theList[:Attribute.CAPITAL_EXPENDITURE_OFFSET.value])

        return (myString == "Capital Expenditure")


    def revenueStringChecker(self, theList):
        """
        This method verifies that the passed in string has the correct title.
        The list passed into the method has to start at the word otherwise this method will declare it wrong.
        :param theList:
        :return: Boolean
        """
        if (len(theList) == 0):
            TypeError: "The passed in list is empty"

        # Assuming the list starts at the word
        myString = "".join(theList[:Attribute.REVENUE_OFFSET.value])

        return (myString == "Total Revenue")



    def dataExtractor(self, theList):
        """
        This method extracts the data from the passed in list, please make sure
        that the list that is passed does not start with any word like the header of the
        data being extracted. This method will take care of empty space between the word and the numbers.
        Only data from 1 line will be extracted.
        :param theList:
        :return:
        """
        counter = 0
        trueStartIndex = 0
        whiteSpace = True

        for element in theList:
            s = "" + element
            if (element != "\n"):
                # Checking if the numbers have white space in front of them
                # Another way of checking for just the number and the white space
                # The element can also contain a "-"
                if ((s.isdigit() or s == "-") and whiteSpace):
                    trueStartIndex = counter
                    whiteSpace = False
                counter += 1
            else:
                break

        # Converting the strings into Integers
        mylist = ""
        mylist = mylist.join((theList[trueStartIndex: counter]))
        mylist = mylist.split(" ")

        counter = 0
        while (counter < len(mylist)):
            stringNumber = mylist[counter].replace(",", "")
            mylist[counter] = int(stringNumber)
            counter += 1

        return mylist


def main():

    stock = Scraper("AAPL")
    stock.getTotalDebt()

main()