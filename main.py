import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
st.title('Stonk screener')
stonk = st.text_input("Stonk ticker")
msft = yf.Ticker(stonk)
st.header("Info")

st.header("Chart")
hist = msft.history(period="max")
st.line_chart(hist['Close'])
st.header("Income statement")
st.subheader("Yearly")
print(msft.income_stmt)
st.subheader("Quarterly")
st.dataframe(msft.quarterly_income_stmt)
st.header("Balance sheet")
st.subheader("Yearly")
st.dataframe(msft.balance_sheet)
st.subheader("Quarterly")
st.dataframe(msft.quarterly_balance_sheet)
st.header("Cash Flows")
st.subheader("Yearly")
st.dataframe(msft.cashflow)
st.subheader("Quarterly")
st.dataframe(msft.quarterly_cashflow)
st.header("Analysts")
st.dataframe(msft.recommendations.tail(4))
st.header("Valuation")
st.subheader("WACC")
D = int(msft.quarterly_balance_sheet.loc['Total Liabilities Net Minority Interest'][0])
cash = int(msft.quarterly_balance_sheet.loc['Cash And Cash Equivalents'][0])
E = int(msft.quarterly_balance_sheet.loc['Stockholders Equity'][0])
net_debt = D - cash
V0 = E + D
V1 = E + net_debt
st.markdown("Enterprise value: " + str(V0))
st.markdown("Enterprise value using net debt: " + str(V1))




