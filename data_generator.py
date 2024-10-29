from kafka import KafkaProducer
from time import sleep, time
import json
import random

# Define Kafka producer
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',  # Refers to Kafka service defined in Docker Compose
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Set field limits for movement within a rectangle
FIELD_WIDTH = 100
FIELD_HEIGHT = 50

# Initialize player positions
player_positions = {
    team: {player_id: (random.randint(0, FIELD_WIDTH), random.randint(0, FIELD_HEIGHT))
           for player_id in range(1, 12)} for team in [1, 2]
}

# Function to generate bounding box coordinates
def generate_bounding_box(x, y):
    x2, y2 = x + random.randint(1, 10), y + random.randint(1, 10)
    return x, y, x2, y2

# Generate and send data to Kafka
def send_data():
    while True:
        for team_id in player_positions.keys():
            for player_id, (x, y) in player_positions[team_id].items():
                # Simulate movement within bounds
                x = (x + random.randint(-2, 2)) % FIELD_WIDTH
                y = (y + random.randint(-2, 2)) % FIELD_HEIGHT
                player_positions[team_id][player_id] = (x, y)
                
                # Create bounding box
                bounding_box = generate_bounding_box(x, y)
                
                # Define data packet
                data = {
                    "timestamp": time(),
                    "teamID": team_id,
                    "playerID": player_id,
                    "boundingBox": bounding_box
                }
                
                # Send data to Kafka
                producer.send('player_data', value=data)
                print(f"Sent data: {data}")
        
        # Send 11 players per team per second
        sleep(1)

if __name__ == "__main__":
    send_data()
