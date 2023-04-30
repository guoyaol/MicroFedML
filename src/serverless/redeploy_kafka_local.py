import time

import os

os.system("kubectl delete -n kafka statefulset.apps/server-deployment")
os.system("kubectl delete -n kafka statefulset.apps/client-deployment")



os.system("kubectl delete -n kafka service/kafka-service")
os.system("kubectl delete -n kafka service/zookeeper-service")
os.system("kubectl delete -n kafka statefulset.apps/zookeeper")
os.system("kubectl delete -n kafka statefulset.apps/kafka-broker")
os.system("kubectl apply -f zookeeper_deployment.yaml -n kafka")
time.sleep(50)
os.system("kubectl apply -f kafka_deployment.yaml -n kafka")
os.system("kubectl get all -n kafka")
time.sleep(50)
os.system("kubectl apply -n kafka -f deployment.yaml ")
os.system("kubectl apply -n kafka -f ../client_serverless/deployment.yaml ")
# os.system("kubectl port-forward service/kafka-service 9092 -n kafka")

# kubectl apply -n kafka -f deployment.yaml 

# kubectl logs -n kafka -f pod/client-deployment-0
# kubectl logs -n kafka -f pod/server-deployment-0

# kubectl delete -n kafka service/my-server-service
# kubectl delete -n kafka statefulset.apps/server-deployment
# kubectl delete -n kafka statefulset.apps/client-deployment

# kubectl logs -n kafka -f pod/kafka-broker-

# kubectl exec -it -n kafka communi-deployment-0 sh

# kubectl describe -n kafka 

# aws eks update-kubeconfig --region us-east-2 --name my-cluster