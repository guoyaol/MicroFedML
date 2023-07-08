# DistributedML

## Easy cmds:

### Deploy client and server pods on k8s

cd src/client; kubectl apply -f deployment.yaml

cd src/server; kubectl apply -f deployment.yaml


### Delete client and server pods on k8s

kubectl delete deployment.apps/server-deployment

kubectl delete deployment.apps/client-deployment

### Logs of client and server pods on k8s
kubectl logs -f deployment.apps/server-deployment

kubectl logs -f deployment.apps/client-deployment


### When client/ or server/ dir changed, need to push updates to docker
python docker_push.py

### Common cmds:
kubectl get services

kubectl get all

kubectl describe <pod>