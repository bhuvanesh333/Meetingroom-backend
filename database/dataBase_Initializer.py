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

Clusterroom_auth_collection = database.ClusterRoom_AUTH
Conferenceroom_auth_collection = database.ConferenceRoom_AUTH
ConferenceRoom_collection = database.ConferenceRoom

#------------------------------------------------------------------------
