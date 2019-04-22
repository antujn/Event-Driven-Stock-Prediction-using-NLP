# Get the top N% market-cap companies

import numpy as np
import pandas as pd

def get_tickers(N):
    topn_tickers = pd.DataFrame()
    for exchange in ["NASDAQ", "NYSE", "AMEX"]:
        url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange="
        tickers = pd.read_csv(url + exchange + '&render=download')
        tickers = tickers[["Symbol","Name","LastSale", "IPOyear","MarketCap","Sector","Industry"]]
        tickers['Exchange']=exchange
        
        topn_tickers = topn_tickers.append(tickers)
    
    topn_tickers = topn_tickers.reset_index().set_index('Symbol')
    topn_tickers = topn_tickers.drop(topn_tickers[topn_tickers.MarketCap < np.percentile(topn_tickers.MarketCap, 100 - N)].index)
    topn_tickers = topn_tickers.drop(columns=['index'])
    
    topn_tickers.to_pickle('top_'+str(N)+'p_tickers.pkl', 'bz2')
    topn_tickers.to_csv('top_'+str(N)+'p_tickers.csv')

N = 37
get_tickers(int(N))

