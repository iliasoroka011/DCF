import yfinance as yf
from pandas_datareader import data as pdr
import streamlit as st
import pandas as pd
import numpy as np
import requests
pd.options.display.max_rows = None
pd.options.display.max_columns = None
msft = yf.Ticker("KO")
import statsmodels.formula.api as smf
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1.5
from statsmodels.tsa.ar_model import AutoReg

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

#print(msft.shares)

#print(msft.fast_info['market_cap'])
#print(float(msft.fast_info['shares']) * float(msft.fast_info['last_price']))

#print(msft.get_income_stmt())
url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=AAPL&apikey=PVDNF0ZUOH9BVDV'
r = requests.get(url)
data = r.json()
income_y = pd.DataFrame(data['annualReports'])
income_q = pd.DataFrame(data['quarterlyReports'])
income_r = income_q['grossProfit'].astype(float).iloc[::-1].reset_index(drop=True)
print(income_r)
print(income_y)
plt.plot(income_r, color='red')
plt.show()
#model1 = smf.ols(formula='grossProfit ~ totalRevenue', data=income_q).fit()
#print(model1.summary())





#r_d_v = int(income_y['researchAndDevelopment'][4])/5 + int(income_y['researchAndDevelopment'][3])*2/5 + int(income_y['researchAndDevelopment'][2])*3/5 + int(income_y['researchAndDevelopment'][1])*4/5+ int(income_y['researchAndDevelopment'][0])
#Em = float(msft.fast_info['shares']) * float(msft.fast_info['last_price']) + r_d_v
