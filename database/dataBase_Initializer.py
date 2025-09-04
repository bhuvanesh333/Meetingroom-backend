import logging
from pymongo import MongoClient
#------------------------------------------------------------------------

MONGO_USERNAME = "edveon"
MONGO_PASSWORD = "edveon123"
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "MeetingRoom"
#------------------------------------------------------------------------

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)

database = client.MeetingRoom
Meetingroom_auth_collection = database.MeetingRoom_AUTH
Meetingroom_collection = database.MeetingRoom

#------------------------------------------------------------------------
