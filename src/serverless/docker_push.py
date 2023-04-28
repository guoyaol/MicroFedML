import os

os.system("docker build -t liugztat/q699-server_serverless:latest .")

os.system("docker tag q699-server_serverless docker.io/liugztat/q699-server_serverless")

os.system("docker push docker.io/liugztat/q699-server_serverless")