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

st.set_page_config(layout="wide")

cRepo = ""
database_repo = True
external_repo = False

@st.cache
def get_user():
    for user in db.githubuser.find({'user': {'$exists': True}}):
        s = user.get('user')
    return s


@st.cache
def get_fullname():
    for user in db.githubuser.find({'fullname': {'$exists': True}}):
        s = user.get('fullname')
    return s


@st.cache
def get_location():
    for user in db.githubuser.find({'location': {'$exists': True}}):
        s = user.get('location')
    return s


@st.cache
def get_repo_names():
    for user in db.githubuser.find({'repos': {'$exists': True}}):
        s = user.get('repos')
    fullnames = s.split('#')
    allrepos = []
    for i in fullnames:
        allrepos.append(g.get_repo(i).name)
    allrepos.sort()
    return allrepos


@st.cache
def get_full_repo_names():
    for user in db.githubuser.find({'repos': {'$exists': True}}):
        s = user.get('repos')
    fullnames = s.split('#')
    fullnames.sort()
    return fullnames


@st.cache
def get_longer_name(name, fullnames):
    longname= [s for s in fullnames if name in s]
    longname = str(longname)
    longname = longname[2:-2]
    return longname

@st.cache
def get_num_repo_commits():
    rn = {}
    for repo in db.githubrepos.find({'name': {'$exists': True}}):
        name = repo.get('name')
        num = len(repo.get('commits'))
        rn[name] = num
    return rn

@st.cache
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

@st.cache
def get_repo_authors(name):
    for repo in db.githubrepos.find({'name': {'$exists': True}}):
        s = repo.get('name')
        if s == name:
            return repo.get('authors')

@st.cache
def get_repo_languages(name):
    for repo in db.githubrepos.find({'languages': {'$exists': True}}):
        s = repo.get('name')
        if s == name:
            return repo.get('languages')


# data constants (declared at start so theres not a bunch of api & db calls in the program)
repoNames = get_repo_names()
longRepoNames = get_full_repo_names()
numRepoCommits = get_num_repo_commits()




###### SIDEBAR CODE #######

st.sidebar.title("Control Panel")

input_type = st.sidebar.radio(
    "Data Type: ", ("From local database", "From Repo Link")
)
if input_type == "From local database":
    database_repo = True
    external_repo = False
if input_type == "From Repo Link":
    database_repo = False
    external_repo = True

if database_repo == True:
    st.sidebar.subheader(get_user())
    st.sidebar.write(get_fullname() + " - " + get_location())

    cRepo = st.sidebar.selectbox('Choose a repository:', repoNames)
    lRepo = str(get_longer_name(cRepo, longRepoNames))


if external_repo == True:
    st.sidebar.write("or")
    ext_repo = st.sidebar.text_input("Paste a link to an external repository: ")
    if len(ext_repo) > 22:
        lRepo = ext_repo[19:]
        split_repo = lRepo.split('/')
        cRepo = split_repo[1]


if database_repo == True:
    ################## TOP BAR ################

    st.title('🌐 Github API Data Visualisation')


    st.write("Current Repository: " + cRepo)
    st.caption("Link to the repository [here](https://github.com/" + lRepo +")")



    col1_1, col1_2, col1_3 = st.columns(3)
    ############# LEFT COLUMN ################


    currentRepo = g.get_repo(lRepo)
    ownerImage = currentRepo.owner.avatar_url
    ownerName = currentRepo.owner.name
    ownerUser = currentRepo.owner.login


    col1_1.markdown("![Avatar of Repo Owner ><]("+ ownerImage + "&s=150)")
    col1_1.caption("###### Owner of Repository: ")
    if ownerName is not None:
        col1_1.markdown("""##### **""" + ownerName + """**""" + """ ("""+ ownerUser + """)""")
    else:
        col1_1.markdown("""##### **""" + ownerUser + """**""")




    ######### MIDDLE COLUMN ###########


    rnlabels = []
    rnvalues = []
    # getting the usernames and values from the languages

    for key in numRepoCommits.keys():
        rnlabels.append(key)
    for val in numRepoCommits.values():
        rnvalues.append(val)

    fig2 = go.Figure(data=[go.Table(header=dict(values=['Repository Name','Number of Commits'],
                                                line_color='#11151c',
                                                fill_color='#262730',
                                                align=['center', 'center'],
                                                height=30,
                                                font=dict(color='white', size=16)),
                                   cells=dict(values=[rnlabels, rnvalues],
                                              line_color='#11151c',
                                              fill_color='#0e1117',
                                              align=['center', 'center'],
                                              height=23,
                                              font=dict(color='white', size=[12, 14])),
                                    columnwidth = [150,80])
                          ])

    fig2.update_layout(title='Number of commits for each repository', autosize=False,
                       height=350)

    col1_2.plotly_chart(fig2, use_container_width=True)


    ##########################


    ####### RIGHT COLUMN #########


    langdict = get_repo_languages(cRepo)

    # getting the usernames and values from the languages
    plabels = []
    pvalues = []

    for key in langdict.keys():
        plabels.append(key)
    for val in langdict.values():
        pvalues.append(val)
    fig = go.Figure(data=[go.Pie(labels=plabels, values=pvalues)])
    fig.update_layout(title='Repository Languages:', autosize=False,
                      width=600, height=400)
    if len(plabels) != 0:
        col1_3.plotly_chart(fig, use_container_width=True)



#################



animals=['giraffes', 'orangutans', 'monkeys']

fig = go.Figure([go.Bar(x=animals, y=[20, 14, 23])])

st.plotly_chart(fig, use_container_width=True)


authordict = get_repo_authors(cRepo)


st.write('note: these graphs currently dont display anything from the github api oops sorry')



