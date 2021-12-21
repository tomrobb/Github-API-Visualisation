import requests
import json
import pprint

file = open("token.txt")
token = file.read()
file.close()

headers = {
    "Authorization" : "token {}".format(token)
}

user = "tomroberts201"
url = "https://api.github.com/users/{}/repos".format(user)

data = {"type" : "all", "sort" : "full_name", "direction" : "asc"}

output = requests.get(url, data=json.dumps(data))
output = json.loads(output.text)

for i in output:
    print (i["name"])






