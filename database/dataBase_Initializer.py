import logging
from pymongo import MongoClient
#------------------------------------------------------------------------

MONGO_USERNAME = "edveon"
MONGO_PASSWORD = "edveon123"
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "MeetingRoom"
#------------------------------------------------------------------------

MONGO_URI = "mongodb+srv://bhuvanesh:getin@meetingroom-cluster.mzsu5gs.mongodb.net/"
client = MongoClient(MONGO_URI)

database = client.MeetingRoom

Clusteradmin_auth_collection = database.ClusterAdmin_AUTH
Clusteruser_auth_collection = database.ClusterUser_AUTH
ConferenceRoom_collection = database.ConferenceRoom

user_sessions_collection = database.user_sessions

#------------------------------------------------------------------------

def get_db():
    return database

def get_all_type_users():
    return database.ClusterAdmin_AUTH, database.ClusterUser_AUTH

def get_blacklisted_tokens():
    return database.blacklisted_tokens

def get_user_sessions():
    return database.user_sessions