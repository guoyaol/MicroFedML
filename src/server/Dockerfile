FROM python:3-alpine
WORKDIR /app
COPY server_loop.py .
COPY server.py .
CMD ["/usr/local/bin/python3", "/app/server_loop.py"]

