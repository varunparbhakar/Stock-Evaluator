import json

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


    def freeCashFlow(self):
        self.driver.get("https://finance.yahoo.com/quote/{}/cash-flow?p={}".format(self.TICKER, self.TICKER))
        self.driver.implicitly_wait(5)

        # "//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[10]/div[1]/div[3]/span"
        # "//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[12]/div[1]/div[3]/span"
        # "//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[12]/div[1]/div[4]/span"





        # Getting the main Class = "D(tbrg))
        webElement = self.driver.find_element_by_xpath("//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[3]/div[1]/div/div[2]")
        print(webElement.text)
        freeCashFlowList = self.stringParser(webElement.text)
        print(freeCashFlowList)

    def stringParser(self, theString):
        stringOffSet = 15
        myStringList = list(theString)
        currentCounter = 0
        freeAt = 0
        for el in myStringList:
            character = "" + el
            if (character.isalpha()):
                if (myStringList[currentCounter] == "F"
                        and myStringList[currentCounter + 1] == "r"
                        and myStringList[currentCounter + 2] == "e"
                        and myStringList[currentCounter + 3] == "e"):
                    print("found free")
                    freeAt = currentCounter
                    break
            currentCounter += 1

        print(myStringList[freeAt + stringOffSet:])

        mylist = ""
        mylist = mylist.join((myStringList[freeAt + stringOffSet:]))
        mylist = mylist.split(" ")
        counter = 0
        while (counter < len(mylist)):
            print(mylist[counter])
            counter += 1



def main():
    scraper = Scraper("AAPl")
    scraper.freeCashFlow()

main()