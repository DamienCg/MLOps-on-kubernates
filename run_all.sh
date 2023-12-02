#!/bin/bash

# Start Minikube
echo "Starting Minikube..."
minikube start

# Build and Run app1 Docker Container
cd app1
docker build -t app1 .
docker run --network="host" app1

# OPEN A NEW TERMINAL

# Apply app1-service.yaml
kubectl apply -f app1-service.yaml

# Build and run app2 Docker container
cd ..
cd app2
docker build -t app2 .
docker run --network="host" app2

# Apply pod.yaml
cd ..
kubectl apply -f pod.yaml

# Apply cronjob.yaml
cd app2
kubectl apply -f cronjob.yaml
