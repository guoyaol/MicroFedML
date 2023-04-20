import os

os.system("docker build -t liugztat/q6993607-client_serverless:latest .")

os.system("docker tag q6993607-client_serverless docker.io/liugztat/q6993607-client_serverless")

os.system("docker push docker.io/liugztat/q6993607-client_serverless")