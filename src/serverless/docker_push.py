import os

os.system("docker build -t liugztat/guoyao-server_serverless:latest .")

os.system("docker tag guoyao-server_serverless docker.io/liugztat/guoyao-server_serverless")

os.system("docker push docker.io/liugztat/guoyao-server_serverless")