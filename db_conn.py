
import pymongo
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
mongo_pass = os.getenv("mongodb_pass")
print(mongo_pass)

uri = f"mongodb+srv://bmattblake:{mongo_pass}@passdb.qcojh7t.mongodb.net/?retryWrites=true&w=majority&appName=PassDB"


# Create a new client and connect to the server
client = pymongo.MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

pass_man_collection = client.PassMan
passdb = pass_man_collection.passdb

'''passdb.insert_one({"website": "youtube", 
                   "username": "matthew",
                   "password": "matthew's_password"})'''

objects  = []
for password in passdb.find():
    objects.append(password)

print(objects)

passdb