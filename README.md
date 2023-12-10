# Start Minikube

```bash
minikube start
docker login


## Build apply service and Run app1 Docker Container
cd EXTERNAL_SOURCE_DATA_STORE
docker build -t external_source_ds .
#docker tag app1 damiencg/externaldata:v1.0
#docker push damiencg/externaldata:v1.0
kubectl apply -f external_source_ds_service.yaml
docker run --network="host" external_source_ds



## Build apply service and Run app3 Docker Container
cd FEATURES_STORE
docker build -t features_store .
#docker tag app1 damiencg/featuresstore:v1.0
#docker push damiencg/featuresstore:v1.0
kubectl apply -f features_store_service.yaml
docker run --network="host" features_store



# Build and run app2 Docker container:
cd DATA_MANAGEMENT_PIPELINE
docker build -t data_management .
#docker tag app2 damiencg/ingpipeline:v1.0
#docker push damiencg/ingpipeline:v1.0
docker run --network="host" data_management



cd ..
cd MODEL_STORE
docker build -t model_store .
kubectl apply -f model_store_service.yaml
docker run --network="host" model_store


cd MODEL_MANAGEMENT_PIPELINE
docker build -t model_management .
docker run --network="host" model_management

cd ..
cd WEB_APP
docker build -t webapp .
docker run --network="host" webapp


# Apply pod.yaml
cd ..
kubectl apply -f mlops_workflow_pod.yaml

# Applica crone
cd app2
kubectl apply -f cronjob.yaml



kubectl get cronjobs
kubectl describe cronjob data_management-cronjob
kubectl logs --selector=job-name=data_management-cronjob-28367542
kubectl get pods --watch
