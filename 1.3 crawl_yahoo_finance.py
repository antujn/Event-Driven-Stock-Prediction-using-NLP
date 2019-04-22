# Get historical stock prices from Yahoo Finance

import os
import time
import datetime

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from tqdm import tqdm

from multiprocessing import Process


if not os.path.exists('historical_data'):
    os.makedirs('historical_data')
    
options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": os.path.join(os.getcwd(), "historical_data"),
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

N = 37
top_tickers = pd.read_pickle('top_'+str(N)+'p_tickers.pkl', 'bz2')

n=1000


def top():
    driver = webdriver.Chrome(executable_path = 'chromedriver.exe', chrome_options=options)

    for ticker in tqdm(top_tickers.index):
        if ticker+'.csv' in os.listdir('historical_data'):
            continue

        url = "https://finance.yahoo.com/quote/"+ticker+"/history?period1="+str(int((datetime.datetime.today() - datetime.timedelta(days=n)).timestamp()))+"&period2="+str(int(datetime.datetime.today().timestamp()))+"&interval=1d&filter=history&frequency=1d"
        driver.get(url)
        try:
            csv_link = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')))
        except TimeoutException:
            continue
        csv_link.click()
    
    driver.close()

def bottom():
    driver = webdriver.Chrome(executable_path = 'chromedriver.exe', chrome_options=options)

    for ticker in tqdm(top_tickers.index[::-1]):
        if ticker+'.csv' in os.listdir('historical_data'):
            continue

        url = "https://finance.yahoo.com/quote/"+ticker+"/history?period1="+str(int((datetime.datetime.today() - datetime.timedelta(days=n)).timestamp()))+"&period2="+str(int(datetime.datetime.today().timestamp()))+"&interval=1d&filter=history&frequency=1d"
        driver.get(url)
        try:
            csv_link = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')))
        except TimeoutException:
            continue      
        csv_link.click()
    
    driver.close()   


if __name__ == '__main__':
    Process(target=top).start()
    Process(target=bottom).start()

