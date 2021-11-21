import yfinance as yf
import streamlit as st
from github import Github
import datetime
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from math import pi
from collections import Counter


# A simple webapp used to display data, using streamlit.
# currently using data from yfinance, planning to use
# data from my database next.


# connecting to github api via access token
g = Github("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")

st.set_page_config(layout="wide")


def display_user_info(usr):
    userImage = usr.avatar_url
    userName = usr.name
    userLogin = usr.login
    userLocation = usr.location

    col1_1.markdown("![User's Avatar ><]("+ userImage + "&s=150)")
    col1_2.markdown("##### " + userLogin)
    if userName is not None:
        col1_2.write(" " + userName)
    if userLocation is not None:
        col1_2.write(userLocation)


def get_repo_names(userRepos):
    nameList = []
    for i in userRepos:
        nameList.append(i.name)
    return nameList


def get_total_stars(userRepos):
    total = 0
    for i in userRepos:
        total = total + i.stargazers_count
    return total

def get_repo_sizes(userRepos):
    dct = {}
    for i in userRepos:
        dct[i.name] = i.size
    return dct



###### SIDEBAR CODE #######
input_type = "null"
valid_input = True

st.sidebar.image('./images/logo.png')

user_in = st.sidebar.text_input("Enter github username or repo link:")
# for when the user inputs a username
if "/" not in user_in and len(user_in) > 3:
    input_type = "user"
    try:
        usr  = g.get_user(user_in)
    except:
        st.sidebar.write("User not found")
        valid_input = False


# for when the user inputs a repo link
if "/" in user_in and len(user_in) > 5:
    input_type = "repo"
    if user_in.startswith("https"):
        user_in = user_in[19:]
    if user_in.startswith("github"):
        user_in = user_in[11:]
    try:
        rpo  = g.get_repo(user_in)
    except:
        st.sidebar.write("Repository not found")
        valid_input = False



if valid_input and input_type == "user":
    rNames = []

    for i in usr.get_repos():
        rNames.append(i.name)

    rSelection = st.sidebar.selectbox('Choose a Repository:', rNames)

    if st.sidebar.button('View Repository Data'):
        longName = usr.login + "/" + rSelection
        input_type = "repo"
        rpo  = g.get_repo(longName)


################## TOP BAR ################


if input_type == "user":
    st.title('👥 User Data Visualisation')
    st.write("")
if input_type == "repo":
    st.title('👥 Repository Data Visualisation')
if input_type == "null":
    st.title('👥 GitHub API Data Visualisation')
    st.write("Enter a username, or link a repository to begin! :)")

col1_1, col1_2, col1_3, col1_4, col1_5 = st.columns([1.0,1.5,1,1,2])
# st.write("Current Repository: " + cRepo)
# st.caption("Link to the repository [here](https://github.com/" + lRepo +")")




# Column 1_1 & 1_2:
#   -   Display User Avatar + info
#   -   Also initialises variables used by other columns
if valid_input and input_type == "user":
    display_user_info(usr)
    userRepos = usr.get_repos()
    userStars = get_total_stars(userRepos)
    repoNames = get_repo_names(userRepos)
    repoSizes = get_repo_sizes(userRepos)
    userE = usr.get_events

if valid_input and input_type == "repo":
    st.write(rpo.name)




# currentRepo = g.get_repo(lRepo)
# ownerImage = currentRepo.owner.avatar_url
# ownerName = currentRepo.owner.name
# ownerUser = currentRepo.owner.login


# col1_1.markdown("![Avatar of Repo Owner ><]("+ ownerImage + "&s=150)")
# col1_1.caption("###### Owner of Repository: ")
# if ownerName is not None:
#     col1_1.markdown("""##### **""" + ownerName + """**""" + """ ("""+ ownerUser + """)""")
# else:
#     col1_1.markdown("""##### **""" + ownerUser + """**""")



# Column 1_3:
#   -   Display Followers & Total Repos
if valid_input and input_type == "user":



    col1_3.metric("Followers", usr.followers)
    col1_3.metric("Total Repos", userRepos.totalCount)

# rnlabels = []
# rnvalues = []
# # getting the usernames and values from the languages

# for key in numRepoCommits.keys():
#     rnlabels.append(key)
# for val in numRepoCommits.values():
#     rnvalues.append(val)

# fig2 = go.Figure(data=[go.Table(header=dict(values=['Repository Name','Number of Commits'],
#                                             line_color='#11151c',
#                                             fill_color='#262730',
#                                             align=['center', 'center'],
#                                             height=30,
#                                             font=dict(color='white', size=16)),
#                                cells=dict(values=[rnlabels, rnvalues],
#                                           line_color='#11151c',
#                                           fill_color='#0e1117',
#                                           align=['center', 'center'],
#                                           height=23,
#                                           font=dict(color='white', size=[12, 14])),
#                                 columnwidth = [150,80])
#                       ])

# fig2.update_layout(title='Number of commits for each repository', autosize=False,
#                    height=350)

# col1_2.plotly_chart(fig2, use_container_width=True)


# Column 1_4:
#   -   Display Following & Stars Received
if valid_input and input_type == "user":



    col1_4.metric("Following", usr.following)
    col1_4.metric("Stars Received", userStars)




# langdict = get_repo_languages(cRepo)

# # getting the usernames and values from the languages
# plabels = []
# pvalues = []

# for key in langdict.keys():
#     plabels.append(key)
# for val in langdict.values():
#     pvalues.append(val)
# fig = go.Figure(data=[go.Pie(labels=plabels, values=pvalues)])
# fig.update_layout(title='Repository Languages:', autosize=False,
#                     width=600, height=400)
# if len(plabels) != 0:
#     col1_3.plotly_chart(fig, use_container_width=True)



####### COLUMN 2-1 #########

col2_1, col2_2 =  st.columns([1,2])

if valid_input and input_type == "user":
    languages = []

    for i in userRepos:
        languages.append(i.language)


    clanguages = dict(Counter(languages))
    plabels = list(clanguages.keys())
    pvalues = list(clanguages.values())

    fig = go.Figure(data=[go.Pie(labels=plabels, values=pvalues)])
    fig.update_layout(title='Repository Languages:', autosize=False,
                        width=650, height=500)
    if len(plabels) != 0:
        col2_1.plotly_chart(fig, use_container_width=True)


####### COLUMN 2-2 #########
if valid_input and input_type == "user":
    names = list(repoSizes.keys())
    sizes = list(repoSizes.values())

    fig = go.Figure([go.Bar(x=names, y=sizes)])

    col2_2.plotly_chart(fig, use_container_width=True)

if input_type == "repo":
    st.write("repo")
