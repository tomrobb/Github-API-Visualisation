import pymongo
import pprint

print("Demonstration python based mongodb access")

# establishing a connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# create a database
db = client.classDB

for repo in db.githubrepos.find({'commits': {'$exists': True}}):
        pprint.pprint(repo)
        print()


for user in db.githubuser.find({'location': {'$exists': True}}):
    pprint.pprint(user)
    print()



