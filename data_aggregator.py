from kafka import KafkaConsumer, KafkaProducer
import json
from collections import defaultdict
from collections import deque
import time

# Initialize Kafka consumer and producer
consumer = KafkaConsumer(
    'player_data_transformed',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Store player positions in a deque (fixed size for last 10 seconds)
player_positions = defaultdict(lambda: deque(maxlen=10))  # Store positions for each player ID
entry_count = 0  # Counter for entries processed

def aggregate_data():
    global entry_count

    while True:  # Keep processing messages
        for message in consumer:
            data = message.value
            player_id = data['playerID']
            x = data['x']
            y = data['y']

            # Only aggregate for players in team 1 (1-11)
            if 1 <= player_id <= 11:
                # Store the current position
                player_positions[player_id].append((x, y))
                entry_count += 1  # Increment entry count

            # Check if we've processed 110 entries
            if entry_count >= 110:
                # Calculate average position for each player in team 1
                avg_positions = {}
                for player_id in range(1, 12):  # For players 1 to 11
                    if player_positions[player_id]:  # Check if there are positions stored
                        avg_x = sum(pos[0] for pos in player_positions[player_id]) / len(player_positions[player_id])
                        avg_y = sum(pos[1] for pos in player_positions[player_id]) / len(player_positions[player_id])
                        avg_positions[player_id] = {'x': avg_x, 'y': avg_y}

                # Send the average positions to the new Kafka topic
                if avg_positions:
                    print(f"Average positions for team 1: {avg_positions}")
                    producer.send('player_data_aggregated_avg_position_last_10_seconds', value=avg_positions)

                # Reset the counter and positions after aggregation
                entry_count = 0
                player_positions.clear()  # Clear positions for next aggregation
        
        time.sleep(1)  # Control the frequency of message consumption

if __name__ == "__main__":
    aggregate_data()
