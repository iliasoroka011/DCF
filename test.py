import yfinance as yf
from pandas_datareader import data as pdr
import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import selenium
import numpy as np
import pandas as pd
from sympy import *
from datetime import date
from datetime import timedelta
from selenium import webdriver
import pandas_datareader as dr
import matplotlib.pyplot as plt
from datetime import datetime as dt
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
pd.options.display.max_rows = None
pd.options.display.max_columns = None
driver = webdriver.Chrome(service=BraveService(ChromeDriverManager().install()))
msft = yf.Ticker("AAPL")

re = 0
equity = 0
debt = 0
beta = 0
k=0
# Required
company_ticker = 'AAPL'

# Optional
company_name = ''


# Selenium script
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

# store starting time
begin = time.time()

# FINRA's TRACE Bond Center
driver.get('http://finra-markets.morningstar.com/BondCenter/Results.jsp')

# click agree
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, ".button_blue.agree"))).click()

# click edit search
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'a.qs-ui-btn.blue'))).click()

# input Issuer Name
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'input[id=firscreener-issuer]')))
inputElement = driver.find_element_by_id("firscreener-issuer")
inputElement.send_keys(company_name)

# input Symbol
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'input[id=firscreener-cusip]')))
inputElement = driver.find_element_by_id("firscreener-cusip")
inputElement.send_keys(company_ticker)

# click advanced search
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'a.ms-display-switcher.hide'))).click()



# click show results
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'input.button_blue[type=submit]'))).click()

# wait for results
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '.rtq-grid-row.rtq-grid-rzrow .rtq-grid-cell-ctn')))

# create dataframe from scrape
frames = []
for page in range(1, 11):
    bonds = []
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, (f"a.qs-pageutil-btn[value='{str(page)}']"))))  # wait for page marker to be on expected page
    time.sleep(2)

    headers = [title.text for title in driver.find_elements_by_css_selector(
    '.rtq-grid-row.rtq-grid-rzrow .rtq-grid-cell-ctn')[1:]]

    tablerows = driver.find_elements_by_css_selector(
        'div.rtq-grid-bd > div.rtq-grid-row')
    for tablerow in tablerows:
        tablerowdata = tablerow.find_elements_by_css_selector(
            'div.rtq-grid-cell')
        bond = [item.text for item in tablerowdata[1:]]
        bonds.append(bond)

        # Convert to Dataframe
        df = pd.DataFrame(bonds, columns=headers)

    frames.append(df)

    try:
        driver.find_element_by_css_selector('a.qs-pageutil-next').click()
    except:
        break

bond_prices_df = pd.concat(frames)

print(bond_prices_df)

# store end time
end = time.time()

# total time taken
print(f"Total runtime of the program is {end - begin} seconds")



def bond_dataframe_filter(df):
# Drop bonds with missing yields and missing credit ratings
    df['Yield'].replace('', np.nan, inplace=True)

    df = df.dropna(subset=['Yield'])


# Create Maturity Years column that aligns with Semi-Annual Payments from corporate bonds
    df['Yield'] = df['Yield'].astype(float)
    df['Coupon'] = df['Coupon'].astype(float)
    df['Price'] = df['Price'].astype(float)
    now = dt.strptime(date.today().strftime('%m/%d/%Y'), '%m/%d/%Y')
    df['Maturity'] = pd.to_datetime(df['Maturity']).dt.strftime('%m/%d/%Y')
    daystillmaturity = []
    yearstillmaturity = []
    for maturity in df['Maturity']:
        daystillmaturity.append(
            (dt.strptime(maturity, '%m/%d/%Y') - now).days)
        yearstillmaturity.append(
            (dt.strptime(maturity, '%m/%d/%Y') - now).days/360)
    df = df.reset_index(drop=True)
    df['Maturity'] = pd.Series(daystillmaturity)
    df['Maturity Years1'] = pd.Series(yearstillmaturity).round() # Better for Annual Payments
    df['Maturity Years2'] = round(pd.Series(yearstillmaturity)/0.5)*0.5 # Better for Semi-Annual Payments



    return df

bond_df_result = bond_dataframe_filter(bond_prices_df)
max_row = bond_df_result.nlargest(1, 'Maturity Years1')
print(max_row)
print(bond_df_result)

D = int(msft.quarterly_balance_sheet.loc['Total Liabilities Net Minority Interest'][0])
cash = int(msft.quarterly_balance_sheet.loc['Cash And Cash Equivalents'][0])
E = int(msft.quarterly_balance_sheet.loc['Stockholders Equity'][0])
net_debt = D - cash
url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=AER&apikey=PVDNF0ZUOH9BVDV'
r = requests.get(url)
data = r.json()
income_y = pd.DataFrame(data['annualReports'])
income_q = pd.DataFrame(data['quarterlyReports'])
try:
    r_d_v = int(income_y['researchAndDevelopment'][4])/5 + int(income_y['researchAndDevelopment'][3])*2/5 + int(income_y['researchAndDevelopment'][2])*3/5 + int(income_y['researchAndDevelopment'][1])*4/5+ int(income_y['researchAndDevelopment'][0])
except:
    r_d_v = 0


Em = float(msft.fast_info['shares']) * float(msft.fast_info['last_price']) + r_d_v
V0 = E + D
V1 = E + net_debt
V3 = Em + D
print("Enterprise value: " + str(V0))
print("Enterprise value using net debt: " + str(V1))
cost_of_debt = float(max_row['Yield'])
print(cost_of_debt)




url = 'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=30year&apikey=2PVDNF0ZUOH9BVDV'
r = requests.get(url)
bond_10 = r.json()

bond_current = pd.DataFrame(bond_10)
EV = Em/V3
DV = D/V3
risk_free = float(bond_current['data'][0]['value'])
bet = float(msft.info['beta'])
risk_premium = 4.3
equired_rate_of_return_equity = risk_free + bet*risk_premium
print(equired_rate_of_return_equity)
tax_rate = float(msft.quarterly_income_stmt.loc['Tax Rate For Calcs'][0])
wacc = equired_rate_of_return_equity*EV + (1 - tax_rate)*cost_of_debt*DV
print(wacc)
# To do: probability of default


