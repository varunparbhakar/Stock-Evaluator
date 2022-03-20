from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from math import ceil

# Setting up the Web Driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
TICKER = "AAPL"
driver = webdriver.Chrome(PATH)
print( "This is a stock {}, and this is the same stock{}".format(TICKER, TICKER))
driver.get("https://finance.yahoo.com/quote/{}/analysis?p={}".format(TICKER, TICKER))
number = driver.find_element_by_xpath("//*[@id=\"Col1-0-AnalystLeafPage-Proxy\"]/section/table[2]/tbody/tr[1]/td[5]/span")
print(number.text)
driver.close()