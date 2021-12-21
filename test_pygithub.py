from github import Github
import time
import pprint

# Note: 
# the two programs "test_requests.py" and "test_pygithub.py"
# are only used for testing the efficiency of pygithub module, 
# vs json api requests, considering swapping to the latter, 
# since I'm not satisfied with how long gathering data for
# commits is taking me.
# (they'll both be deleted in the final program)

file = open("token.txt")
token = file.read()
file.close()

g = Github(token)
usr = g.get_user("tomroberts201")
usr.html_url
repoList = usr.get_repos()

r = g.get_repo("dabreadman/Node-Podman-OpenShift-CI-CD")

contributers = []

for i in r.get_contributors():
    print(i.login)
    contributers.append(i.login)



contrib_repo_data = {}

for c in contributers:
    contrib_repo_data[c] = []


start_time = time.time()
for i in r.get_commits():
    try:
        clist = []
        for c in contributers:
            if i.committer.login == c:
                print("match")
                dct = {
                    "date": i.stats.last_modified,
                    "additions": i.stats.additions,
                    "deletions": i.stats.deletions,
                }
                contrib_repo_data[c].append(dct)
    except Exception as e:
        print("") 


print("For each Contributor")
for c in contributers:
    addi = 0
    dele = 0
    total= 0
    for i in contrib_repo_data[c]:
        total += 1
        addi += i.get("additions")
        dele += i.get("deletions")
    print(c)
    print("Total Submissions: " + str(total))
    print("Additions: " + str(addi))
    print("Deletions: " + str(dele))
    print("")
        

      



print("--- %s seconds ---" % (time.time() - start_time))

print("Creator of Repository: " + r.owner.login)
print("Contributers: " + str(contributers))

pprint.pprint(contrib_repo_data)