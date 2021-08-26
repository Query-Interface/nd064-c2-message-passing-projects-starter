# Setting up Kafka on Kubernetes

We will install kafka in Kubernetes using the Strimzi operator: https://strimzi.io/quickstarts/

1. Create a namespace named kafka: kubectl create namespace kafka
2. Install the strimzi operator: kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
3. Deploy kafka cluster using the modules/kafka/deployment/kafka-crd.yaml
   kubectl apply -f modules/kafka/deployment/kafka-crd.yaml -n kafka
4. Wait for the creation using the following command: kubectl wait kafka/kafka-cluster --for=condition=Ready --timeout=300s -n kafka
5. It should display "kafka.kafka.strimzi.io/kafka-cluster condition met"
6. With the command kubectl get pods -n kafka, you should see the pods created for kafka

...