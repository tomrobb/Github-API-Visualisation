# import Github from the PyGithub library
from github import Github

g = Github("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")

usr = g.get_user()
print("user:        " + usr.login)
print("fullname:    " + usr.name)
print("location:    " + usr.location)
print("company:     " + usr.company)