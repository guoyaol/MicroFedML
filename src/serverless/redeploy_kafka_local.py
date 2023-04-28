

import os

os.system("kubectl delete service/kafka-service -n kafka")
os.system("kubectl delete -n kafka service/zookeeper-service")
os.system("kubectl delete -n kafka deployment.apps/zookeeper")
os.system("kubectl delete -n kafka deployment.apps/kafka-broker")
os.system("kubectl apply -f zookeeper_deployment.yaml -n kafka")
os.system("kubectl apply -f kafka_deployment.yaml -n kafka")
os.system("kubectl get all -n kafka")
# os.system("kubectl port-forward service/kafka-service 9092 -n kafka")

# kubectl apply -n kafka -f deployment.yaml 

# kubectl logs -n kafka -f pod/client-deployment-
# kubectl logs -n kafka -f pod/server-deployment-

# kubectl delete -n kafka service/my-server-service
# kubectl delete -n kafka statefulset.apps/server-deployment
# kubectl delete -n kafka statefulset.apps/client-deployment

# kubectl logs -n kafka -f pod/kafka-broker-

# kubectl exec -it server-deployment-0 sh -n kafka