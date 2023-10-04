#!/bin/bash

echo "Installing python packages"
python3 -m pip install -r requirements.txt

echo "Starting API Server"
uvicorn api_server:app --reload
echo "API Server started at http://127.0.0.1:8000/photos"

echo "Starting Change Stream Listener"
python3 change_stream_listener.py
echo "Change Stream Listener started..."

echo "Starting Kafka Consumer"
python3 kafka_consumer.py
echo "Kafka Consumer listening for new messages..."