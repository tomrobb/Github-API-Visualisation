import pymongo
import pprint

print("Demonstration python based mongodb access")

# establishing a connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# create a database
db = client.classDB

githubuser = db.githubuser.find()

for user in githubuser:
    pprint.pprint(user)
    print()