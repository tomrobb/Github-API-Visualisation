import yfinance as yf
import streamlit as st
import pandas as pd

# A simple webapp used to display data, using streamlit.
# currently using data from yfinance, planning to use
# data from my database next.

st.write("""
# Data Visualisation Test

This is a test app for visualising data with streamlit!
Shown are the stock closing price and volume of Google!

""")

tickerSymbol = 'GOOGL'

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
