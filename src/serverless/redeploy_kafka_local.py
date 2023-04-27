

import os

os.system("kubectl delete service/kafka-service -n kafka")
os.system("kubectl delete -n kafka service/zookeeper-service")
os.system("kubectl delete -n kafka deployment.apps/zookeeper")
os.system("kubectl delete -n kafka deployment.apps/kafka-broker")
os.system("kubectl apply -f zookeeper_deployment.yaml -n kafka")
os.system("kubectl apply -f kafka_deployment.yaml -n kafka")
os.system("kubectl get all -n kafka")
# os.system("kubectl port-forward service/kafka-service 9092 -n kafka")
