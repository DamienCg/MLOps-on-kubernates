```bash

# Start Minikube

```bash
minikube start

## Build and Run app1 Docker Container
cd app1
docker build -t app1 .
docker run --network="host" app1

# Apply app1-service.yaml:

kubectl apply -f app1-service.yaml

## Build and Run app3 Docker Container
cd app3DataStore
docker build -t app3 .
docker run --network="host" app3

# Apply app3-service.yaml:

kubectl apply -f app3-service.yaml

# Build and run app2 Docker container:
cd ..
cd app2
docker build -t app2 .
docker run --network="host" app2

# Apply pod.yaml
cd ..
kubectl apply -f pod.yaml

# Applica crone
cd app2
kubectl apply -f cronjob.yaml