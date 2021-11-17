# import Github from the PyGithub library
from github import Github
import json
import pymongo

g = Github("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")
usr = g.get_user()
print("Username:    " + usr.login)


s = ""
for repo in usr.get_repos():
    s += repo.name + "#"
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