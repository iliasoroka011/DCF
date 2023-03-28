import yfinance as yf
import requests
import pandas as pd
import numpy as np
import pandas_datareader
from pandas_datareader import famafrench
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
pd.options.display.max_rows = None
pd.options.display.max_columns = None

factor = pandas_datareader.DataReader('F-F_Research_Data_Factors', 'famafrench', '2020-03', '2023-01')[0]
data = yf.download("CMCOM.AS ^AEX", start="2020-02-01", end="2023-02-01", interval = "1mo")['Adj Close']
print(factor)

price_change = data.pct_change()
df = price_change.drop(price_change.index[0])
print(df)
df.index = factor.index
merge = pd.merge(df, factor, on = 'Date')
merge[['SMB', 'HML', 'RF']] = merge[['SMB', 'HML', 'RF']]/100
merge.rename(
    columns={"CMCOM.AS": "CM", "^AEX": "AEX"},
    inplace=True,
)
merge['CMCOM_RF'] = merge.CM - merge.RF
merge['AEX_RF'] = merge.AEX - merge.RF

print(merge)
y = merge[['CMCOM_RF']]
x = merge[['AEX_RF', 'SMB', 'HML']]
print(x)
X = sm.add_constant(x)
mod = sm.OLS(y, X).fit()
model = LinearRegression().fit(x, y)
print('Beta: ', mod.summary())

#print(pandas_datareader.famafrench.get_available_datasets())
