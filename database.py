from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["college_db"]

users_collection = db["users"]
students_collection = db["students"]