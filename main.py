import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from math import ceil

# Setting up the Web Driver
from Scraper import Scraper
from Stock import Stock

PATH = "C:\Program Files (x86)\chromedriver.exe"
TICKER = "PSEC"
myStock = None
myScraper = Scraper()

# Check if TSLA is in the spreadsheet
myStockSpreadsheet = open("demofile.csv", "r")
csv_reader = list(csv.reader(myStockSpreadsheet))
isStockPresentInSpreadsheet = False


for line in csv_reader:
    if(line[1] == TICKER):
        print(line)
        myStock = Stock(list(line))
        isStockPresentInSpreadsheet = True

if(not isStockPresentInSpreadsheet):
    myScraper.initializeStock(TICKER)

# driver = webdriver.Chrome(PATH)
# print( "This is a stock {}, and this is the same stock{}".format(TICKER, TICKER))
# driver.get("https://finance.yahoo.com/quote/{}/financials?p={}".format(TICKER, TICKER))
# number = driver.find_element_by_xpath("//*[@id=\"Col1-1-Financials-Proxy\"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[3]/span")
# print("expecting 365,817,000")
# print(number.text)
# driver.close()