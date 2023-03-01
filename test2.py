import yfinance as yf
from pandas_datareader import data as pdr
import streamlit as st
import pandas as pd
import numpy as np
import requests
pd.options.display.max_rows = None
pd.options.display.max_columns = None
msft = yf.Ticker("KO")
#print(msft.shares)

#print(msft.fast_info['market_cap'])
#print(float(msft.fast_info['shares']) * float(msft.fast_info['last_price']))


tax_rate = float(msft.quarterly_income_stmt.loc['Tax Rate For Calcs'][0])
#print(msft.get_income_stmt())
url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=AAPL&apikey=PVDNF0ZUOH9BVDV'
r = requests.get(url)
data = r.json()
income_y = pd.DataFrame(data['annualReports'])
income_q = pd.DataFrame(data['quarterlyReports'])
print(income_q)

def adj_income(income_q):



#r_d_v = int(income_y['researchAndDevelopment'][4])/5 + int(income_y['researchAndDevelopment'][3])*2/5 + int(income_y['researchAndDevelopment'][2])*3/5 + int(income_y['researchAndDevelopment'][1])*4/5+ int(income_y['researchAndDevelopment'][0])
#Em = float(msft.fast_info['shares']) * float(msft.fast_info['last_price']) + r_d_v
