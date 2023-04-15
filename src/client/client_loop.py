import socket
import os
import sys
import time
from client import Client
counter = 0

SRV = "127.0.0.1"#os.getenv('SERVER_ADDRESS')
PORT = 13333#int(os.getenv('SERVER_PORT'))

cli_id = 1
server_address = (SRV, PORT)
cli = Client(cli_id, server_address)
while 1:
    
    print(f"Client Loop {cli_id} begins")
    if counter != 0:
        cli.get_param_from_server()
    cli.client_update()
    cli.client_evaluate()
    cli.send_param_to_server()
    counter += 1
    print(f"Client Loop {cli_id} ends")

