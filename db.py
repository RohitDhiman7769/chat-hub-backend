from flask import Flask
from flask_pymongo import pymongo
import os

# secret_key = os.getenv("MY_SECRET")
# from app import app
import urllib.parse
# URL-encode the password
username =str(os.getenv("AUTH_USERNAME"))
passw = str(os.getenv("PASSWORD"))
password = urllib.parse.quote_plus(passw)  # Encodes '@' to '%40'

# Corrected connection string
# CONNECTION_STRING = f"mongodb+srv://{username}:{password}@cluster0.hy8a5.mongodb.net/"
CONNECTION_STRING =f"mongodb+srv://{username}:{password}@cluster0.hy8a5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',CONNECTION_STRING)
client = pymongo.MongoClient(CONNECTION_STRING)
database = client.get_database('Chat-hubb')
user_collection = pymongo.collection.Collection(database, 'users')
rooms_collection = pymongo.collection.Collection(database, 'rooms')
user_friends_collection = pymongo.collection.Collection(database, 'user_friends')
room_member_Ids_collection = pymongo.collection.Collection(database, 'room_member_id')




