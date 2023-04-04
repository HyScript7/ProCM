from common.configuration import (MONGO_URI, PCM_COLLECTION_POSTS,
                                  PCM_COLLECTION_PROJECTS,
                                  PCM_COLLECTION_USERS, PCM_DATABASE)
from pymongo import MongoClient, collection, database

DB_CLIENT: MongoClient = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)

DB_DATABASE: database = DB_CLIENT[PCM_DATABASE]

DB_POSTS: collection = DB_DATABASE[PCM_COLLECTION_POSTS]
DB_PROJECTS: collection = DB_DATABASE[PCM_COLLECTION_PROJECTS]
DB_USERS: collection = DB_DATABASE[PCM_COLLECTION_USERS]