# Real-time data backend for tracking football player locations using Docker, Kafka & MongoDB

Using Docker for containerization, Kafka for data-streaming and MongoDB for storage.

This project aims to simulate a simplified real-time data backend for tracking football player locations, enabling analyses such as formation changes over time. 
Using the SoccerTrack dataset from Kaggle (https://www.kaggle.com/datasets/atomscott/soccertrack), which annotates football game footage with player coordinates, the data will first be streamed into Kafka as raw four-column bounding boxes. 
Then the data will be transformed to two-column x-y coordinates in a seperate microservice. 
Another containerized microservice aggregates the data, additionally the data is send to MongoDB.
Based on MongoDB, the position of players can be visualized.

##Simplified high-level data flow:
![Data Flow simplified](/data_flow.jpg)

##Example visualisation of player positioning data:
![Player Positioning Visual](/player_positions_viz.png)
