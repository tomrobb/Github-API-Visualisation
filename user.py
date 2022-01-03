import streamlit as st
import streamlit.components.v1 as stc
from github import Github
import plotly.graph_objects as go
from datetime import datetime
from collections import Counter

# getting the Github User Auth Token from token.txt
# no need to check if valid, since this code wont be run without a valid token
file = open("token.txt")
token = file.read()
file.close()
g = Github(token)

def run(user_in):
    # Creating the layout of the app, with two rows of columns
    # first row
    col1_1, col1_2, col1_3, col1_4, col1_5 = st.columns([0.8, 1, 0.6, 0.6, 1])
    # second row
    col2_1, col2_2, = st.columns(2)

    usr = g.get_user(user_in)

    with st.spinner('Fetching Profile Information'):
        user_info = {
            "image" : '"' + usr.avatar_url + '"',
            "name" : usr.name,
            "login" : usr.login,
            "location" : usr.location,
            "url" : usr.html_url
        }
        user_activity = []
        for i in usr.get_events():
            date = i.created_at.date()
            date = date.strftime("%Y-%m-%d")
            user_activity.append(date)
        user_activity.reverse()

    with st.spinner('Fetching Repository Information'):
        user_repos = usr.get_repos()
        repos = []
        for i in user_repos:
            dct = {
                "name": i.name,
                "stars": i.stargazers_count,
                "language": i.language,
                "size": i.size,
            }
            repos.append(dct)

    # Running functions to visualise data
    display_profile_data(user_info, col1_1, col1_2)
    display_metrics(repos, usr, col1_3, col1_4)
    display_activity(user_activity, col2_2)
    display_stars_per_repo(repos, col2_1)
    display_repo_languages(repos, col2_1)



def display_profile_data(user_info, col1, col2):
    with col1:
        # displaying the image as a html element, to be able to customise the border
        stc.html("""
            <body>
                <style>
                    img {
                        border-radius: 50%;
                    }
                </style>
                <img src= """ + user_info["image"] + """alt ="Avatar" style="width:150px">
            </body>""",
            width=158, height=158)

    col2.markdown("##### " + user_info["login"])

    if user_info["name"]:
        col2.write(" " + user_info["name"])

    if user_info["location"]:
        col2.write(user_info["location"])

    if user_info["url"]:
        col2.markdown("""[Link to Profile](""" + user_info["url"] + """)""")


def display_metrics(repos, usr, col1, col2):
    totalStars = 0
    for i in repos:
        totalStars += i.get("stars")
    #displaying first 2 metrics in the first column
    col1.metric("Followers", usr.followers)
    col1.metric("Public Repos", len(repos))
    #displaying remaining metrics in the 2nd column
    col2.metric("Following", usr.following)
    col2.metric("Stars Received", totalStars)

def display_repo_languages(repos, col):
    languages = []
    for i in repos:
        # if the language exists, add to the list
        # this is needed because some repos don't contain any code
        if i.get("language"):
            languages.append(i.get("language"))
    # dictionary of "language":count
    clanguages = dict(Counter(languages))
    sort_orders = (sorted(clanguages.items(), key=lambda x:x[1],reverse=True))

    # changed how the chart is rendered based on number of entries, only showing top 10
    # for larger sets to avoid messy and unreadable piecharts
    if len(sort_orders) > 10:
        clanguages = dict(sort_orders[:10])

        plabels = list(clanguages.keys())
        pvalues = list(clanguages.values())

        fig = go.Figure(data=[go.Pie(labels=plabels, values=pvalues)])
        fig.update_layout(title='Repository Languages (Top 10):', autosize=False,
                        width=650, height=400)
        fig.update_traces(hoverinfo='label+value', textinfo='label')
        if len(plabels) != 0:
            col.plotly_chart(fig, use_container_width=True)
    else:
        clanguages = dict(sort_orders)

        plabels = list(clanguages.keys())
        pvalues = list(clanguages.values())

        fig = go.Figure(data=[go.Pie(labels=plabels, values=pvalues)])
        fig.update_layout(title='Repository Languages:', autosize=False,
                        width=650, height=400)
        fig.update_traces(hoverinfo='label+value', textinfo='label')
        if len(plabels) != 0:
            col.plotly_chart(fig, use_container_width=True)


def display_stars_per_repo(repos, col):
    # First, getting the data we need as two lists, for plotting
    labels = []
    values = []
    stars_per_repo = {}
    for i in repos:
        if i.get("stars") != 0:
            # adding value to dictionary
            stars_per_repo[i.get("name")]= i.get("stars")

    sort_orders = (sorted(stars_per_repo.items(), key=lambda x:x[1],reverse=True))

    # changed how the chart is rendered based on number of entries, only showing top 10
    # for larger sets to avoid messy and unreadable piecharts
    if len(sort_orders) > 10:
        stars_per_repo = dict(sort_orders[:10])

        labels = list(stars_per_repo.keys())
        values = list(stars_per_repo.values())
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_layout(title='Stars per Repo (Top 10):', autosize=False,
                        width=650, height=400)
        fig.update_traces(hoverinfo='label+value', textinfo='value')
        if len(labels) != 0:
            col.plotly_chart(fig, use_container_width=True)
    else:
        stars_per_repo = dict(sort_orders)

        labels = list(stars_per_repo.keys())
        values = list(stars_per_repo.values())
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_layout(title='Stars per Repo:', autosize=False,
                        width=650, height=400)
        fig.update_traces(hoverinfo='label+value', textinfo='value')
        if len(labels) != 0:
            col.plotly_chart(fig, use_container_width=True)

def display_activity(user_activity, col):
    activity_count = dict(Counter(user_activity))
    keys = list(activity_count.keys())
    values = list(activity_count.values())

    fig = go.Figure(data=[go.Scatter(x=keys, y = values)])
    fig.update_layout(title='Recent Activity:', autosize=False,
                        width=650, height=500, plot_bgcolor='#161a24')
    fig.update_xaxes(gridcolor='#353642')
    fig.update_yaxes(gridcolor='#353642')

    col.plotly_chart(fig, use_container_width=True)    
