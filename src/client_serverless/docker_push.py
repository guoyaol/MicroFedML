import os

os.system("docker build -t liugztat/guoyao-client_serverless:latest .")

os.system("docker tag guoyao-client_serverless docker.io/liugztat/guoyao-client_serverless")

os.system("docker push docker.io/liugztat/guoyao-client_serverless")