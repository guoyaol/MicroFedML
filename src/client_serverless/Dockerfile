FROM python:3-alpine
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
COPY client.py .
COPY client_serverless_loop.py .
CMD ["/usr/local/bin/python3", "/app/client_serverless_loop.py"]

