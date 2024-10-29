from kafka import KafkaConsumer, KafkaProducer
import json

# Kafka configurations
KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'  # Update if necessary
CONSUMER_TOPIC = 'player_data'
PRODUCER_TOPIC = 'player_data_transformed'

# Create a Kafka consumer
consumer = KafkaConsumer(
    CONSUMER_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='data-transformer-group'
)

# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

try:
    for message in consumer:
        data = json.loads(message.value)

        # Transform the bounding box coordinates into x and y coordinates
        player_id = data['playerID']
        x = data['boundingBox'][0] + (data['boundingBox'][2] / 2)
        y = data['boundingBox'][1] + (data['boundingBox'][3] / 2)

        # Create the new data structure
        transformed_data = {
            'playerID': player_id,
            'x': x,
            'y': y
        }

        # Produce the transformed data to the new topic
        producer.send(PRODUCER_TOPIC, transformed_data)
        print(f"Transformed and sent data: {transformed_data}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    consumer.close()
    producer.close()
