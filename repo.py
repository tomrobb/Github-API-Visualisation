import streamlit as st
import streamlit.components.v1 as stc
from github import Github
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
from collections import OrderedDict
from collections import Counter

# getting the Github User Auth Token from token.txt
# no need to check if valid, since this code wont be run without a valid token
file = open("token.txt")
token = file.read()
file.close()
g = Github(token)

def run(user_in):

    r = g.get_repo(user_in)


    with st.spinner('Fetching Repository Stats'):
        repo_stats = {
            "name" : r.name,
            "url" : r.html_url,
            "stars" : r.stargazers_count,
            "forks" : r.forks_count,
            "created_at" : r.created_at,
            "owner" : r.owner.login,
            "owner_avatar" : r.owner.avatar_url
        }

    with st.spinner('Fetching Repository Commits'):
        all_commits = []
        authors = []
        for i in r.get_commits():
            try:
                if i.author.login:
                    dct = {
                        "date" : datetime.strptime(i.stats.last_modified, "%a, %d %b %Y %H:%M:%S %Z"),
                        "author" : i.author.login,
                        "additions": i.stats.additions,
                        "deletions" : i.stats.deletions
                    }
                    all_commits.append(dct)
                    authors.append(dct["author"])
            except Exception as e:
                print("No Login")
        authors = list(dict.fromkeys(authors)) # removes duplicate entries in authors
        repo_stats["authors"] = authors
        repo_stats["commits"] = len(all_commits)


    col1_1, col1_2, col1_3 = st.columns([5, 1, 1])

    display_repo_stats(repo_stats, col1_1, col1_2, col1_3)
    graph_additions_deletions(all_commits,st)




def display_repo_stats(repo_stats, col1, col2, col3):
    col1.title('📁 ' + repo_stats["name"])
    col1.write("Created by user:  " + repo_stats["owner"] + " on " + repo_stats["created_at"].strftime("%d/%m/%Y"))
    col1.markdown("Link to Repository [here](" + repo_stats["url"] +")")
    col2.metric("Commits", repo_stats["commits"])
    col2.metric("Stars", repo_stats["stars"])
    col3.metric("Contributors", len(repo_stats["authors"]))
    col3.metric("Forks", repo_stats["forks"])

def graph_additions_deletions(commit_stats, col1):

    additions= {}
    deletions = {}

    for i in commit_stats:
        date = i["date"].strftime("%Y-%m-%d")
        if date in additions:
            additions[date] += i["additions"]
        else:
            additions[date] = i["additions"]
        if date in deletions:
            deletions[date] += i["deletions"]
        else:
            deletions[date] = i["deletions"]


    fig = go.Figure()

    fig.add_trace(go.Scatter(x= list(additions.keys()), y=list(additions.values()),
                    mode='lines',
                    name='additions'))
    fig.add_trace(go.Scatter(x=list(deletions.keys()), y=list(deletions.values()),
                    mode='lines',
                    name='deletions'))
    fig.update_layout(title='Additions and Deletions', autosize=False,
                        width=650, height=500, plot_bgcolor='#161a24')
    fig.update_xaxes(gridcolor='#353642')
    fig.update_yaxes(gridcolor='#353642')
    col1.plotly_chart(fig, use_container_width=True)
