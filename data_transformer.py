from kafka import KafkaConsumer, KafkaProducer
import json

# Initialize Kafka consumer and producer
consumer = KafkaConsumer(
    'player_data',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def transform_data(data):
    # Convert bounding box to x and y coordinates (center of bounding box)
    x1, y1, x2, y2 = data['boundingBox']
    x_center = x1 + (x2 - x1) / 2
    y_center = y1 + (y2 - y1) / 2
    
    # Return transformed data with timestamp and teamID
    return {
        'timestamp': data['timestamp'],
        'teamID': data['teamID'],
        'playerID': data['playerID'],
        'x': x_center,
        'y': y_center
    }

# Consume messages from 'player_data' and transform data
for message in consumer:
    transformed_data = transform_data(message.value)
    print(f"Sending transformed data: {transformed_data}")
    producer.send('player_data_transformed', value=transformed_data)
