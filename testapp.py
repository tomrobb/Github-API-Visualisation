import yfinance as yf
import streamlit as st
import pymongo
import json
import pprint

# A simple webapp used to display data, using streamlit.
# currently using data from yfinance, planning to use
# data from my database next.

# establishing a connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# create a database
db = client.classDB


def get_user():
    for user in db.githubuser.find({'user': {'$exists': True}}):
        s = user.get('user')
    return s


def get_repos():
    for user in db.githubuser.find({'repos': {'$exists': True}}):
        s = user.get('repos')
    allrepos = s.split('#')
    allrepos.sort()
    return allrepos


st.title('Data Visualisation Test')
st.write('This is an app which visualizes data from the Github API ')
st.title(get_user())

st.selectbox('Choose a repository:', get_repos())

tickerSymbol = 'GOOGL'

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')

st.line_chart(get_repos())
st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
st.write('note: these graphs currently dont display anything from the github api oops sorry')



