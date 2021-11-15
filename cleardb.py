import pymongo
import pprint

print("Clearing the data in the database")

# establishing a connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# create a database
db = client.classDB

# clears all data in database
db.githubuser.delete_many({})