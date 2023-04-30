FROM python:3.8-alpine
COPY requirements.txt .
RUN pip install  -r requirements.txt
RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    libressl-dev \
    musl-dev \
    linux-headers
RUN pip install  numpy
RUN pip install  torch==1.13.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
WORKDIR /app
COPY loop.py .
CMD ["/usr/local/bin/python3", "/app/loop.py"]

