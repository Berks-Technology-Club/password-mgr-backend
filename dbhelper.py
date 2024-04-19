import pymongo
import certifi

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

class dbhelper:
    def connect(self, uri):
        self.client = pymongo.MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        
        pass_man_collection = self.client.PassMan
        self.passdb = pass_man_collection.passdb
    
    def test_connection(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
    
    def get_passwords(self):
        objects = []
        for item in self.passdb.find():
            objects.append(item)
        return objects
    
    def delete_all(self):
        self.passdb.delete_many({}) 
    
    def update_passwords(self, data):
        password_str = self.get_passwords()
        '''with open("db.txt", "w") as f:
            f.write(password_str)
            f.close()'''
        try:
            self.delete_all()
            self.passdb.insert_one(data)
            return True
        except:
            print(password_str)
            self.passdb.insert_many(password_str)
            return False
            

if __name__ == "__main__":
    load_dotenv()
    mongo_user = os.getenv("mongo_user")
    mongo_pass = os.getenv("mongo_passwd")

    uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@passdb.qcojh7t.mongodb.net/?retryWrites=true&w=majority&appName=PassDB"
    helper = dbhelper()
    helper.connect(uri)
    helper.test_connection()
    
    print(helper.update_passwords({"str": "new str"}))