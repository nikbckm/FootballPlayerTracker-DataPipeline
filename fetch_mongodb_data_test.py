from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['game_data']
collection = db['player_positions']

# Fetch all documents
for doc in collection.find():
    print(doc)
