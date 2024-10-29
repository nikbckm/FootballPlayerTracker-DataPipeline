# Terraform configuration to run locally

provider "docker" {}

# Define a network for your containers
resource "docker_network" "data_eng_network" {
  name = "data_eng_network"
}

# MongoDB container
resource "docker_container" "mongo" {
  image = "mongo:latest"
  name  = "mongo"
  ports {
    internal = 27017
    external = 27017
  }
  volumes {
    host_path = "${path.module}/mongo_data"
    container_path = "/data/db"
  }
  networks_advanced {
    name = docker_network.data_eng_network.name
  }
}

# Zookeeper container
resource "docker_container" "zookeeper" {
  image = "confluentinc/cp-zookeeper:latest"
  name  = "zookeeper"
  ports {
    internal = 2181
    external = 2181
  }
  env = [
    "ZOOKEEPER_CLIENT_PORT=2181",
    "ZOOKEEPER_TICK_TIME=2000"
  ]
  networks_advanced {
    name = docker_network.data_eng_network.name
  }
}

# Kafka container
resource "docker_container" "kafka" {
  image = "confluentinc/cp-kafka:latest"
  name  = "kafka"
  ports {
    internal = 9092
    external = 9092
  }
  env = [
    "KAFKA_BROKER_ID=1",
    "KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181",
    "KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092",
    "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT",
    "KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT",
    "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1"
  ]
  networks_advanced {
    name = docker_network.data_eng_network.name
  }
}

# Data Generator container
resource "docker_container" "data_generator" {
  image = "data_generator:latest"  # Update with your actual image name
  name  = "data_generator"
  environment = [
    "KAFKA_BOOTSTRAP_SERVERS=kafka:9092"
  ]
  networks_advanced {
    name = docker_network.data_eng_network.name
  }
}

# Data Transformer container
resource "docker_container" "data_transformer" {
  image = "data_transformer:latest"  # Update with your actual image name
  name  = "data_transformer"
  environment = [
    "KAFKA_BOOTSTRAP_SERVERS=kafka:9092"
  ]
  networks_advanced {
    name = docker_network.data_eng_network.name
  }
}

# Data Aggregator container
resource "docker_container" "data_aggregator" {
  image = "data_aggregator:latest"  # Update with your actual image name
  name  = "data_aggregator"
  environment = [
    "KAFKA_BROKER=kafka:9092"
  ]
  networks_advanced {
    name = docker_network.data_eng_network.name
  }
}

# Data Ingestion MongoDB container
resource "docker_container" "data_ingestion_mongodb" {
  image = "data_ingestion_mongodb:latest"  # Update with your actual image name
  name  = "data_ingestion_mongodb"
  environment = [
    "KAFKA_BOOTSTRAP_SERVERS=kafka:9092",
    "MONGO_URI=mongodb://mongo:27017"
  ]
  networks_advanced {
    name = docker_network.data_eng_network.name
  }
}
