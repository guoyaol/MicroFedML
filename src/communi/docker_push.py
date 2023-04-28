import os

os.system("docker build -t liugztat/q-communi_serverless:latest .")

os.system("docker tag q-communi_serverless docker.io/liugztat/q-communi_serverless")

os.system("docker push docker.io/liugztat/q-communi_serverless")