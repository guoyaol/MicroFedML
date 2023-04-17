# DistributedML

## Easy cmds:
kubectl delete deployment.apps/server-deployment
kubectl delete deployment.apps/client-deployment

kubectl logs -f deployment.apps/server-deployment
kubectl logs -f deployment.apps/client-deployment

cd src/client; kubectl apply -f deployment.yaml
cd src/server; kubectl apply -f deployment.yaml

python docker_push.py

kubectl get services
kubectl get all
kubectl describe <pod>