import yfinance as yf
import streamlit as st

#st.write()の引数はMarkDown記法で書くことができる
st.write("""
# Simple Stock Price App
Shown are the stock closing price and volume of Google!

""")

#yfinanceモジュールの関数から情報を取得

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'GOOGL'
#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# Open	High	Low	Close	Volume	Dividends	Stock Splits


#得た情報をチャートで表示(グラフ)
st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
