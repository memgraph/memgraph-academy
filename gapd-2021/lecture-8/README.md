# Streaming support

This step demonstrates how to connect a Kafka cluster to your Memgraph instance and stream the data directly into the database.

## How to run the app

1. Build all the necessary Docker images with `docker-compose build`.
2. Start *Kafka*, *Memgraph* and the Flask server with `docker-compose up server`.
3. In a new terminal, start the transaction producer with `docker-compose up transaction-stream`.