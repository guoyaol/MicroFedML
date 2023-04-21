import socket
import os
import sys
import time
from client import Client
counter = 0

# SRV = os.getenv('SERVER_ADDRESS') #'0.0.0.0'#
# PORT = int(os.getenv('SERVER_PORT')) #13333#

cli_id = int(sys.argv[1])
server_address = None#(SRV, PORT)
cli = Client(cli_id, server_address, serverless = True)
while 1:
    start_time = time.perf_counter()
    print(f"Client Loop {cli_id} begins")
    # if counter != 0:
    #     cli.get_param_from_kafka()
    cli.client_update()
    # cli.client_evaluate()
    cli.send_param_to_kafka()
    cli.get_param_from_kafka()
    counter += 1
    end_time = time.perf_counter()  # record the end time
    elapsed_time = int((end_time - start_time) * 1000)  # calculate elapsed time in milliseconds
    print(f"Client Loop {cli_id} ends, took {elapsed_time} seconds to execute.")

