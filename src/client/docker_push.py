import os

os.system("docker build -t liugztat/q6993607-client:latest .")

os.system("docker tag q6993607-client docker.io/liugztat/q6993607-client")

os.system("docker push docker.io/liugztat/q6993607-client")