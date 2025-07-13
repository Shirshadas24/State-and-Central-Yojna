from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["chat_history"]
collection = db["conversations"]

def log_conversation(query, response, language, user_id=None, username=None):
    log = {
        "query": query,
        "response": response,
        "language": language,
        "user_id": user_id,
        "username": username,
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(log)
