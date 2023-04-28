FROM python:3-alpine
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
COPY loop.py .
CMD ["/usr/local/bin/python3", "/app/loop.py"]

