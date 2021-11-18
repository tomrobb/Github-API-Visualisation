import yfinance as yf
import streamlit as st
from github import Github
from collections import Counter
import pymongo

# connecting to github api via access token
g = Github("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")

# establishing a connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# create a database
db = client.classDB

def get_user():
    for user in db.githubuser.find({'user': {'$exists': True}}):
        s = user.get('user')
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


def get_full_repo_name(name):
    for user in db.githubuser.find({'repos': {'$exists': True}}):
        s = user.get('repos')
    fullnames = s.split('#')
    longname = ""


usr = g.get_user()
print(usr.get_followers().totalCount)
print(usr.get_following().totalCount)
for repo in usr.get_repos():
    authors = []
    print("\n" + repo.name)
    print("   - stars: " + str(repo.stargazers_count))
    print(repo.get_languages())
    print(repo.get_commits().totalCount)


    commits = repo.get_commits()
    for i in commits:
        try:
            authors.append(i.author.login)
        except AttributeError:
            authors.append("webapp")
        #print(i.commit.author.date)

    print(str(Counter(authors)))
# Repo datastructure
# name
# languages
#


# individual commit