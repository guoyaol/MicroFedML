import socket
import os
import sys
import time
from client import Client
counter = 0

SRV = os.getenv('SERVER_ADDRESS') #'0.0.0.0'#
PORT = int(os.getenv('SERVER_PORT')) #13333#

cli_id = 1
server_address = (SRV, PORT)
cli = Client(cli_id, server_address)
while 1:
    start_time = time.perf_counter()
    
    print(f"Client Loop {cli_id} begins")
    if counter != 0:
        cli.get_param_from_server()
    cli.client_update()
    cli.client_evaluate()
    cli.send_param_to_server()
    counter += 1

    end_time = time.perf_counter()  # record the end time
    elapsed_time = int((end_time - start_time) * 1000)  # calculate elapsed time in milliseconds
    print(f"Client Loop {cli_id} ends, took {elapsed_time} seconds to execute.")

