import numpy as np
import pandas as pd

import os
from tqdm import tqdm

if not os.path.exists('return_labels'):
    os.makedirs('return_labels')

sp500 = pd.read_csv('historical_data/^GSPC.csv')

sp500['short'] = np.log(sp500['Adj Close'])-np.log(sp500['Open'])
sp500['mid'] = np.log(sp500['Adj Close']).diff(periods=7)
sp500['long'] = np.log(sp500['Adj Close']).diff(periods=28)

sp500.to_csv('return_labels/^GSPC.csv', index=False)

for ticker in tqdm(os.listdir('historical_data')):
    if ticker in os.listdir('return_labels'):
        continue
    hist_prices = pd.read_csv('historical_data/'+ticker)
    return_sp500 = sp500.loc[(sp500.Date>=hist_prices.Date.iloc[0]) & (sp500.Date<=hist_prices.Date.iloc[-1])].reset_index()

    hist_prices['rel_short'] = (np.log(hist_prices['Adj Close'])-np.log(hist_prices['Open']))-return_sp500['short']
    hist_prices['rel_mid'] = np.log(hist_prices['Adj Close']).diff(periods=7)-return_sp500['mid']
    hist_prices['rel_long'] = np.log(hist_prices['Adj Close']).diff(periods=28)-return_sp500['long']
    
    hist_prices.to_csv('return_labels/'+ticker, index=False)