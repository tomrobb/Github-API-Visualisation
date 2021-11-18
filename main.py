# import Github from the PyGithub library
from github import Github
import json
import pymongo
import datetime
from collections import Counter


g = Github("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")
usr = g.get_user()
print("Username:    " + usr.login)


s = ""
for repo in usr.get_repos():
    s += repo.full_name + "#"
# removing the last character, so the string is easier to split in the future
s = s[:-1]


# putting our data into a dictionary for the database
dct = {'user': usr.login,
       'fullname': usr.name,
       'location': usr.location,
       'company': usr.company,
       'repos': s
       }

print("dictionary is: " + json.dumps(dct))

# now storing the dictionary in a mongodb

for k, v in dict(dct).items():
    if v is None:
        del dct[k]

print("cleaned dictionary is: " + json.dumps(dct))

# Now storing the data
# establishing a connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# create a database
db = client.classDB

db.githubuser.insert_many([dct])

for repo in usr.get_repos():
    authors = []
    c = []
    name = repo.name
    fullname = repo.full_name
    stars = repo.stargazers_count
    languages = repo.get_languages()

    commits = repo.get_commits()
    totalcommits = 0

    for i in commits:
        try:
            authors.append(i.author.login)
        except AttributeError:
            authors.append("webapp")
        totalcommits = totalcommits + 1
        commitdct = {'date': i.commit.author.date.date(),
                     'index': totalcommits,
                     }
        c.append(commitdct)

    authors = Counter(authors)

    sdct = {'name': name,
            'fullname': fullname,
            'stars': repo.stargazers_count,
            'authors': authors,
            'languages': languages,
            'totalcommits': len(c),
            'commits': c
           }

    db.githubrepos.insert_many([sdct])
