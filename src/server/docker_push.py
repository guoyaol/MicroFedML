import os

os.system("docker build -t liugztat/q6993607-server:latest .")

os.system("docker tag q6993607-server docker.io/liugztat/q6993607-server")

os.system("docker push docker.io/liugztat/q6993607-server")