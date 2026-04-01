from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://dbaayush:dbaayush25@cluster0.cbl6luh.mongodb.net/?appName=Cluster0"

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = client["dbaayush"]
reports_collection = db["reports"]