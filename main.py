# import Github from the PyGithub library
from github import Github

g = Github("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")

usr = g.get_user()
print("Username:    " + usr.login)

if usr.name is not None:
    print("Full name:   " + usr.name)

if usr.location is not None:
    print("Location:    " + usr.location)

if usr.company is not None:
    print("Company:     " + usr.company)