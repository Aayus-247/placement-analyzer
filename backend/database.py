from pymongo import MongoClient
import certifi

client = MongoClient(
    "mongodb+srv://dbaayush:dbaayush25@cluster0.cbl6luh.mongodb.net/dbaayush?retryWrites=true&w=majority",
    tlsCAFile=certifi.where()
)

# 🔥 ADD HERE
print("Connecting to MongoDB...")
print(client.list_database_names())

db = client["dbaayush"]
reports_collection = db["reports"]