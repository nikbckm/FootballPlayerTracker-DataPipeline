from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'player_data_aggregated_avg_position_last_10_seconds',  # Make sure this matches your topic name
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',  # Start reading from the earliest message
    enable_auto_commit=True  # Automatically commit offsets
)

# Initialize MongoDB client
mongo_client = MongoClient('mongodb://mongo:27017')  # Ensure 'mongo' matches your MongoDB service name
db = mongo_client['game_data']  # Your database name
collection = db['player_positions']  # Your collection name

def store_aggregated_data(data):
    # Insert the aggregated data into MongoDB
    collection.insert_one(data)
    print(f"Stored aggregated data: {data}")

# Consume messages and store aggregated data
for message in consumer:
    aggregated_data = message.value  # Get the message value (the aggregated data)
    store_aggregated_data(aggregated_data)  # Store it in MongoDB
