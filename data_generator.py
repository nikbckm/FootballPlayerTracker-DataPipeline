from kafka import KafkaProducer
from time import sleep
import json
import random

# Define Kafka producer
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',  # Refers to Kafka service defined in Docker Compose
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to generate random bounding box coordinates
def generate_bounding_box():
    x1, y1 = random.randint(0, 100), random.randint(0, 100)
    x2, y2 = x1 + random.randint(1, 10), y1 + random.randint(1, 10)
    return x1, y1, x2, y2

# Generate and send data to Kafka
def send_data():
    while True:
        data = {
            "playerID": random.randint(1, 100),
            "boundingBox": generate_bounding_box()
        }
        producer.send('player_data', value=data)
        print(f"Sent data: {data}")
        sleep(1)

if __name__ == "__main__":
    send_data()
