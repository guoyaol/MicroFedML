import socket
import sys
import os
from server import Server

PORT = 13333#int(os.getenv('LISTEN_PORT'))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', PORT)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen()

server = Server()
while True:
    print('\nWaiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('Connection from ', client_address)
        server.receiving_model_from_connection(connection, client_address)
    finally:
        if len(server.clients) >= 2:
            server.transmit_model()