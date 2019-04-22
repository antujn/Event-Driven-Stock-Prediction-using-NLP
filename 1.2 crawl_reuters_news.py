# Imports

import requests
from lxml.html import fromstring
from bs4 import BeautifulSoup

from fake_useragent import UserAgent
ua = UserAgent()

import pandas as pd

import os
import time
import datetime

import threading

from tqdm import tqdm

# Get news for each ticker for past n days

### Check if the site supports Socks(Tor) proxies

from tor_request import TorRequest
with TorRequest(proxy_port=9050, ctrl_port=9051, password='password') as tr:     
    print(tr.get('http://ipecho.net/plain').text)
    print(tr.get('https://www.reuters.com/finance/stocks/company-news/AMZN.O', headers={'User-agent': ua.random}).status_code)
    
    print(requests.get('http://ipecho.net/plain').text)
    print(requests.get('https://www.reuters.com/finance/stocks/company-news/AMZN.O', headers={'User-agent': ua.random}).status_code)
    
    tr.reset_identity()

### Crawl with Proxy Rotation using free SSL proxies

def get_proxies():
    parser = fromstring(requests.get('https://www.us-proxy.org/').text)
    proxies = set()
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]') and (i.xpath('.//td[8][contains(text(),"minute ")][not(contains(text(),"hour"))]') or i.xpath('.//td[8][contains(text(),"seconds ")][not(contains(text(),"hour"))]')):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)      
    if proxies:
        return proxies
    else:
        print("Waiting for healthy proxies...")
        time.sleep(10)
        print("Retrying...")
        get_proxies()

def fetch(url, date, ticker, proxy):
    global reuters_news
    
    soup = BeautifulSoup(requests.get(url=url + "?date=" + date.strftime("%m%d%Y"), 
                                      headers={'User-agent': ua.random}, 
                                      proxies={"http": proxy, "https": proxy}).text, 'html.parser')
    if soup:
        content = soup.find_all("div", {'class': ['topStory', 'feature']})
        if content:
            for i in range(len(content)):
                head = content[i].h2.get_text().strip()
                body = content[i].p.get_text().strip()

                if i==0 and soup.find_all("div", class_="topStory"):
                    flag = True
                else:
                    flag = False

                reuters_news = reuters_news.append({'ticker':ticker, 'date':date, 
                                                            'head':head, 'body':body, 'top':flag},ignore_index=True)
        
def fetch_news(ticker, exchange):
    global datelist

    suffix = {'AMEX': '.A', 'NASDAQ': '.O', 'NYSE': '.N'}
    url = "https://www.reuters.com/finance/stocks/company-news/" + ticker + suffix[exchange]

    proxies = set()
    while 1:
        if proxies:
            proxy = proxies.pop()
            print(proxy)
        else:
            proxies = get_proxies()
            proxy = proxies.pop()
            print(proxy)
            
        try:   
            response = requests.get(url=url ,proxies={"http": proxy, "https": proxy})
        except:
            continue
            
        try:    
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                exists = len(soup.find_all("div", {'class': ['topStory', 'feature']}))
                if exists:
                    threads = [threading.Thread(target=fetch, args=(url, date, ticker, proxy)) for date in datelist]
                    for thread in tqdm(threads):
                        time.sleep(0.01)
                        thread.start()
                    for thread in tqdm(threads):
                        time.sleep(0.001)
                        thread.join()
                break
        except:
            continue


if __name__ == '__main__':
    N = 37
    top_tickers = pd.read_pickle('top_'+str(N)+'p_tickers.pkl', 'bz2')

    n=1000
    datelist = [datetime.datetime.today() - datetime.timedelta(days=x) for x in range(0, n)]

    if not os.path.exists('reuters_news'):
        os.makedirs('reuters_news')
        
    for ticker, exchange in tqdm(zip(top_tickers.index, top_tickers.Exchange)):
        if ticker in os.listdir('reuters_news'):
            continue

        reuters_news = pd.DataFrame(columns=['ticker', 'date', 'head', 'body', 'top'])
        print(chr(27) + "[2J")
        print(ticker)

        fetch_news(ticker, exchange)
        reuters_news.to_pickle('reuters_news/'+str(ticker), 'bz2') 
