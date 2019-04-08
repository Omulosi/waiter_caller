
import pymongo

def init():
    client = pymongo.MongoClient()
    c = client['waitercaller']
    c.users.create_index("email", unique=True)
    c.requests.create_index("table_id", unique=True)