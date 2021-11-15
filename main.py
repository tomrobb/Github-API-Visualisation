# import Github from the PyGithub library
from github import Github
import json

g = Github("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")

usr = g.get_user()
print("Username:    " + usr.login)

dct = {'user': usr.login,
       'fullname': usr.name,
       'location': usr.location,
       'company': usr.company
       }

print ("dictionary is: " + json.dumps(dct))