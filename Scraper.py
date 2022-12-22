import json

from selenium.webdriver.common.by import By

from Attributes import Attribute

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:

    # def __int__(self):
    #     print("INTIALIZED")

    def __init__(self, theStock):
        PATH = "C:\Program Files\chromedriver.exe"
        self.TICKER = theStock
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        self.service = ChromeService(executable_path=PATH)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait_Timer = 3
        print("Scraper has been initialized")
        # self.Income_Statement = self.getIncome_Statement()
        # self.BalanceSheet_Statement = self.getBalanceSheet_Statement()
        # self.CashFlow_Statement = self.getCashFlow_Statement()
        self.Analysis_Statement = self.getAnalysis_Statement()
        self.driver.close()

    # Getting the web elements from the webpage
    def getCashFlow_Statement(self):
        self.driver.get("https://finance.yahoo.com/quote/{}/cash-flow?p={}".format(self.TICKER, self.TICKER))
        myX_Path = "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[4]/div[1]/div[1]/div[2]"
        WebDriverWait(self.driver, timeout=self.wait_Timer).until(EC.presence_of_element_located((By.XPATH, myX_Path)))
        # Getting the main Class = "D(tbrg))
        webElement = self.driver.find_element(By.XPATH, myX_Path)
        return webElement.text

    def getIncome_Statement(self):
        self.driver.get("https://finance.yahoo.com/quote/{}/financials?p={}".format(self.TICKER, self.TICKER))

        myX_Path = "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[4]/div[1]/div[1]/div[2]"
        WebDriverWait(self.driver, timeout=self.wait_Timer).until(EC.presence_of_element_located((By.XPATH, myX_Path)))

        webElement = self.driver.find_element(By.XPATH, myX_Path)
        return webElement.text

    def getBalanceSheet_Statement(self):
        self.driver.get("https://finance.yahoo.com/quote/{}/balance-sheet?p={}".format(self.TICKER, self.TICKER))
        myX_Path = "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[4]/div[1]/div[1]/div[2]"
        WebDriverWait(self.driver, timeout=self.wait_Timer).until(EC.presence_of_element_located((By.XPATH, myX_Path)))

        # Working Free cash flow Address 10:56 PM 22 March "//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[4]/div[1]/div[1]/div[2]"

        # Getting the main Class = "D(tbrg))
        webElement = self.driver.find_element(By.XPATH, myX_Path)
        return webElement.text
    def getAnalysis_Statement(self):

        myX_Path = "Col1-0-AnalystLeafPage-Proxy"

        self.driver.get("https://finance.yahoo.com/quote/{}/analysis?p={}".format(self.TICKER, self.TICKER))
        # WebDriverWait(self.driver, timeout=self.wait_Timer).until(EC.presence_of_element_located((By.XPATH, myX_Path)))

        webElement = self.driver.find_element(By.ID, myX_Path)

        return webElement.text

    ## Stock Attributes
    def getFreeCashFlow(self):
        freeCashFlowList = self.stringParser(self.CashFlow_Statement, Attribute.FREE_CASH_FLOW_OFFSET)
        print("Free Cash flow of", self.TICKER, "is", freeCashFlowList)
        return freeCashFlowList

    def getTotalDebt(self):

        totalDebt = self.stringParser(self.BalanceSheet_Statement, Attribute.TOTAL_DEBT_OFFSET)
        print("Total Debt of ", self.TICKER, "is", totalDebt)
        return totalDebt

    def getRevenueEstimates(self):
        revenueEstimate = self.stringParser(self.Analysis_Statement, Attribute.TOTAL_DEBT_OFFSET)
        print("Total Revenue Estimate of ", self.TICKER, "is", revenueEstimate)
        return revenueEstimate

    def getTotalRevenue(self):

        revenueList = self.stringParser(self.Income_Statement, Attribute.REVENUE_OFFSET)
        print("Revenue of", self.TICKER, "is", revenueList)
        return revenueList

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
            stringOffSet = 15

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
            stringOffSet = 20
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
            stringOffSet = 14
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
            stringOffSet = 20
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
            stringOffSet = 11
            currentCounter = 0
            while (currentCounter < len(myStringList)):
                character = "" + myStringList[currentCounter]
                if (character.isupper()):

                    if (self.totalDebtStringChecker(myStringList[currentCounter:])):
                        # Only sending the part of the list that has the data not the word itself
                        solutionList = self.dataExtractor(myStringList[currentCounter + stringOffSet:])

                        break
                currentCounter += 1

            # Checking fot Revenue Estimates
        elif (dataType == Attribute.R_E_AVG_ESTIMATE):
            # The purpose of this offset is when we send the list to another method
            # we want to make sure that the other method doesn't receive the word inside the list
            stringOffSet = 14
            currentCounter = 0
            while (currentCounter < len(myStringList)):
                character = "" + myStringList[currentCounter]
                if (character.isupper()):

                    if (self.revenueEstimatesStringChecker(myStringList[currentCounter:])):
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
        myString = "".join(theList[:14])

        return (myString == "Free Cash Flow")

    def revenueEstimatesStringChecker(self, theList):
        """
        This method verifies that the passed in string has the correct title.
        The list passed into the method has to start at the word otherwise this method will declare it wrong.
        The revenue estimates will be grabbed from the average estimates.
        :param theList:
        :return: Boolean
        """
        if (len(theList) == 0):
            TypeError: "The passed in list is empty"

        # Assuming the list starts at the word
        myString = "".join(theList[:13])

        return (myString == "Avg. Estimate")

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
        myString = "".join(theList[:10])

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
        myString = "".join(theList[:19])

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
        myString = "".join(theList[:19])

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
        myString = "".join(theList[:13])

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
    # stock = Scraper()

    stock = Scraper("PSA")
    # print("Income Statement == " + stock.Income_Statement)
    # print("-----------------------------")
    # print("Balance Statement == " + stock.BalanceSheet_Statement)
    # print("-----------------------------")
    # print("Cash Flow Statement == " + stock.CashFlow_Statement)
    # print("-----------------------------")
    print("Analysis Statement == " + stock.Analysis_Statement)
    print("-----------------------------")

    # print(stock.getFreeCashFlow())
    # print("Getting Cash flow again")
    # print(stock.getFreeCashFlow())

    income_Statement = """Total Revenue
378,323,000 365,817,000 274,515,000 260,174,000 265,595,000
Cost of Revenue
215,572,000 212,981,000 169,559,000 161,782,000 163,756,000
Gross Profit
162,751,000 152,836,000 104,956,000 98,392,000 101,839,000
Operating Expense
45,848,000 43,887,000 38,668,000 34,462,000 30,941,000
Operating Income
116,903,000 108,949,000 66,288,000 63,930,000 70,898,000
Net Non Operating Interest Income Expense
45,000 198,000 890,000 1,385,000 2,446,000
Other Income Expense
-79,000 60,000 -87,000 422,000 -441,000
Pretax Income
116,869,000 109,207,000 67,091,000 65,737,000 72,903,000
Tax Provision
16,314,000 14,527,000 9,680,000 10,481,000 13,372,000
Net Income Common Stockholders
100,555,000 94,680,000 57,411,000 55,256,000 59,531,000
Diluted NI Available to Com Stockholders
100,555,000 94,680,000 57,411,000 55,256,000 59,531,000
Basic EPS
- 5.67 3.31 2.99 3.00
Diluted EPS
- 5.61 3.28 2.97 2.98
Basic Average Shares
- 16,701,272 17,352,119 18,471,336 19,821,508
Diluted Average Shares
- 16,864,919 17,528,214 18,595,652 20,000,436
Total Operating Income as Reported
116,903,000 108,949,000 66,288,000 63,930,000 70,898,000
Total Expenses
261,420,000 256,868,000 208,227,000 196,244,000 194,697,000
Net Income from Continuing & Discontinued Operation
100,555,000 94,680,000 57,411,000 55,256,000 59,531,000
Normalized Income
100,555,000 94,680,000 57,411,000 55,256,000 59,531,000
Interest Income
2,746,000 2,843,000 3,763,000 4,961,000 5,686,000
Interest Expense
2,701,000 2,645,000 2,873,000 3,576,000 3,240,000
Net Interest Income
45,000 198,000 890,000 1,385,000 2,446,000
EBIT
119,570,000 111,852,000 69,964,000 69,313,000 76,143,000
EBITDA
130,885,000 - - - -
Reconciled Cost of Revenue
215,572,000 212,981,000 169,559,000 161,782,000 163,756,000
Reconciled Depreciation
11,315,000 11,284,000 11,056,000 12,547,000 10,903,000
Net Income from Continuing Operation Net Minority Interest
100,555,000 94,680,000 57,411,000 55,256,000 59,531,000
Normalized EBITDA
130,885,000 123,136,000 81,020,000 81,860,000 87,046,000
Tax Rate for Calcs
0 0 0 0 0
Tax Effect of Unusual Items
0 0 0 0 0"""

    revenueEstimateString = """Revenue Estimate Current Qtr. (Mar 2022) Next Qtr. (Jun 2022) Current Year (2022) Next Year (2023)
    No. of Analysts 26 25 41 39
    Avg. Estimate 94.01B 86.57B 395.96B 418.34B
    Low Estimate 90.04B 80.6B 384.52B 396.38B
    High Estimate 100.44B 96.55B 408.3B 441.73B
    Year Ago Sales N/A N/A 365.82B 395.96B
    Sales Growth (year/est) N/A N/A 8.20% 5.70%"""
    incomeStatementString = """Total Revenue
    378,323,000 365,817,000 274,515,000 260,174,000 265,595,000
    Cost of Revenue
    215,572,000 212,981,000 169,559,000 161,782,000 163,756,000
    Gross Profit
    162,751,000 152,836,000 104,956,000 98,392,000 101,839,000
    Operating Expense
    45,848,000 43,887,000 38,668,000 34,462,000 30,941,000
    Operating Income
    116,903,000 108,949,000 66,288,000 63,930,000 70,898,000
    Net Non Operating Interest Income Expense
    45,000 198,000 890,000 1,385,000 2,446,000
    Other Income Expense
    -79,000 60,000 -87,000 422,000 -441,000
    Pretax Income
    116,869,000 109,207,000 67,091,000 65,737,000 72,903,000
    Tax Provision
    16,314,000 14,527,000 9,680,000 10,481,000 13,372,000
    Net Income Common Stockholders
    100,555,000 94,680,000 57,411,000 55,256,000 59,531,000
    Diluted NI Available to Com Stockholders
    100,555,000 94,680,000 57,411,000 55,256,000 59,531,000
    Basic EPS
    - 5.67 3.31 2.99 3.00
    Diluted EPS
    - 5.61 3.28 2.97 2.98
    Basic Average Shares
    - 16,701,272 17,352,119 18,471,336 19,821,508
    Diluted Average Shares
    - 16,864,919 17,528,214 18,595,652 20,000,436
    Total Operating Income as Reported
    116,903,000 108,949,000 66,288,000 63,930,000 70,898,000
    Total Expenses
    261,420,000 256,868,000 208,227,000 196,244,000 194,697,000
    Net Income from Continuing & Discontinued Operation
    100,555,000 94,680,000 57,411,000 55,256,000 59,531,000
    Normalized Income
    100,555,000 94,680,000 57,411,000 55,256,000 59,531,000
    Interest Income
    2,746,000 2,843,000 3,763,000 4,961,000 5,686,000
    Interest Expense
    2,701,000 2,645,000 2,873,000 3,576,000 3,240,000
    Net Interest Income
    45,000 198,000 890,000 1,385,000 2,446,000
    EBIT
    119,570,000 111,852,000 69,964,000 69,313,000 76,143,000
    EBITDA
    130,885,000 - - - -
    Reconciled Cost of Revenue
    215,572,000 212,981,000 169,559,000 161,782,000 163,756,000
    Reconciled Depreciation
    11,315,000 11,284,000 11,056,000 12,547,000 10,903,000
    Net Income from Continuing Operation Net Minority Interest
    100,555,000 94,680,000 57,411,000 55,256,000 59,531,000
    Normalized EBITDA
    130,885,000 123,136,000 81,020,000 81,860,000 87,046,000
    Tax Rate for Calcs
    0 0 0 0 0
    Tax Effect of Unusual Items
    0 0 0 0 0"""

    cashFlowString = """Operating Cash Flow
112,241,000 104,038,000 80,674,000 69,391,000 77,434,000
Investing Cash Flow
-22,067,000 -14,545,000 -4,289,000 45,896,000 16,066,000
Financing Cash Flow
-89,263,000 -93,353,000 -86,820,000 -90,976,000 -87,876,000
End Cash Position
38,630,000 35,929,000 39,789,000 50,224,000 25,913,000
Income Tax Paid Supplemental Data
28,833,000 25,385,000 9,501,000 15,263,000 10,417,000
Interest Paid Supplemental Data
2,599,000 2,687,000 3,002,000 3,423,000 3,022,000
Capital Expenditure
-10,388,000 -11,085,000 -7,309,000 -10,495,000 -13,313,000
Issuance of Capital Stock
- 1,105,000 880,000 781,000 669,000
Issuance of Debt
- 20,393,000 16,091,000 6,963,000 6,969,000
Repayment of Debt
-7,750,000 -8,750,000 -12,629,000 -8,805,000 -6,500,000
Repurchase of Capital Stock
-81,674,000 -85,971,000 -72,358,000 -66,897,000 -72,738,000
Free Cash Flow
101,853,000 92,953,000 73,365,000 58,896,000 64,121,000"""

    #print(stock.stringParser(incomeStatementString, Attribute.REVENUE_OFFSET))


main()
