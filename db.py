from flask import Flask
from flask_pymongo import pymongo
# from app import app
import urllib.parse
# URL-encode the password
username = "rohitdhiman265498"
password = urllib.parse.quote_plus("rohitdhiman@265498")  # Encodes '@' to '%40'

# Corrected connection string
# CONNECTION_STRING = f"mongodb+srv://{username}:{password}@cluster0.hy8a5.mongodb.net/"
CONNECTION_STRING =f"mongodb+srv://rohitdhiman265498:{password}@cluster0.hy8a5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(CONNECTION_STRING)
database = client.get_database('Chat-hubb')
user_collection = pymongo.collection.Collection(database, 'users')
rooms_collection = pymongo.collection.Collection(database, 'rooms')
