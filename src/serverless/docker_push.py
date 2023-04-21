import os

os.system("docker build -t liugztat/q6993607-server_serverless:latest .")

os.system("docker tag q6993607-server_serverless docker.io/liugztat/q6993607-server_serverless")

os.system("docker push docker.io/liugztat/q6993607-server_serverless")