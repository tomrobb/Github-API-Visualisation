import yfinance as yf
import streamlit as st
from github import Github
import pymongo
import datetime
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import bokeh
import plotly.graph_objects as go
from math import pi
import json
import pprint


# A simple webapp used to display data, using streamlit.
# currently using data from yfinance, planning to use
# data from my database next.

# connecting to github api via access token
g = Github("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")

# establishing a connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# create a database
db = client.classDB

col = db["githubrepos"]

x = col.find_one()

st.write(x)

def get_user():
    for user in db.githubuser.find({'user': {'$exists': True}}):
        s = user.get('user')
    return s

def get_fullname():
    for user in db.githubuser.find({'fullname': {'$exists': True}}):
        s = user.get('fullname')
    return s

def get_location():
    for user in db.githubuser.find({'location': {'$exists': True}}):
        s = user.get('location')
    return s

def get_repo_names():
    for user in db.githubuser.find({'repos': {'$exists': True}}):
        s = user.get('repos')
    fullnames = s.split('#')
    allrepos = []
    for i in fullnames:
        allrepos.append(g.get_repo(i).name)
    allrepos.sort()
    return allrepos


def get_full_repo_names():
    for user in db.githubuser.find({'repos': {'$exists': True}}):
        s = user.get('repos')
    fullnames = s.split('#')
    fullnames.sort()
    return fullnames


def get_longer_name(name, fullnames):
    longname= [s for s in fullnames if name in s]
    longname = str(longname)
    longname = longname[2:-2]
    return longname


def get_repo_data(name):
    for repo in db.githubrepos.find({'name': {'$exists': True}}):
        s = repo.get('name')
        if s == name:
            dct = { 'name': repo.get('name'),
                     'fullname': repo.get('fullname'),
                     'stars': repo.get('stars'),
                     'authors': repo.get('authors'),
                     'languages': repo.get('languages'),
                     'totalcommits': repo.get('totalcommits'),
                     'commits': repo.get('commits')
            }
            return dct


def get_repo_authors(name):
    for repo in db.githubrepos.find({'name': {'$exists': True}}):
        s = repo.get('name')
        if s == name:
            return repo.get('authors')


def get_repo_languages(name):
    for repo in db.githubrepos.find({'languages': {'$exists': True}}):
        s = repo.get('name')
        if s == name:
            return repo.get('languages')


def get_commits(dct):
    return dct.get('commits')


def get_totalcommits(dct):
    return dct.get('totalcommits')


def get_authors(dct):
    authors = dct.get('authors')


# data constants (declared at start so theres not a bunch of api & db calls in the program)
# get_data()
repoNames = get_repo_names()
longRepoNames = get_full_repo_names()

st.title('Data Visualisation Test')
st.subheader(get_user())
st.write(get_fullname() + " - " + get_location())


cRepo = st.selectbox('Choose a repository:', repoNames)
lRepo = str(get_longer_name(cRepo, longRepoNames))
# st.write('Full name: ' + lRepo)
authordict = get_repo_authors(cRepo)
langdict = get_repo_languages(cRepo)


# getting the usernames and values from the authors
plabels = []
pvalues = []


for key in langdict.keys():
    plabels.append(key)
for val in langdict.values():
    pvalues.append(val)
fig = go.Figure(data=[go.Pie(labels=plabels, values=pvalues)])
fig.update_layout(title='--> Languages:', autosize=False,
                  width=600, height=400)
if len(plabels) != 0:
    st.plotly_chart(fig, use_container_width=True)




st.line_chart(repoNames)

# st.line_chart(tickerDf.Close)
# st.line_chart(tickerDf.Volume)

st.write('note: these graphs currently dont display anything from the github api oops sorry')



