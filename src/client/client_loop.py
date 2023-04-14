import socket
import os
import sys
import time
from client import Client
counter = 0

SRV = os.getenv('SERVER_ADDRESS')
PORT = int(os.getenv('SERVER_PORT'))

cli_id = 0
server_address = (SRV, PORT)
cli = Client(cli_id, server_address)
while 1:
    counter += 1
    print(f"Client Loop {cli_id} begins")
    cli.get_param_from_server()
    cli.client_update()
    cli.client_evaluate()
    cli.send_param_to_server()
    print(f"Client Loop {cli_id} ends")

