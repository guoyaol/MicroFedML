import socket
import sys
import os
from server import Serverless

# PORT = int(os.getenv('LISTEN_PORT')) #13333#

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('0.0.0.0', PORT)
# print('Starting up on {} port {}'.format(*server_address))
# sock.bind(server_address)
# sock.listen()
in_pod = True
shard_id = int(os.environ.get('HOSTNAME')[-1]) if in_pod else int(sys.argv[1])#
server = Serverless(shard_id=shard_id, in_pod=in_pod)
print(f"server {shard_id} started!")
while True:
    # print('\nWaiting for a connection')
    # connection, client_address = sock.accept()
    # try:
    #     print('Connection from ', client_address)
    #     server.receiving_model_from_connection(connection, client_address)
    # finally:
    #     if len(server.clients) >= 2:
    #         server.transmit_model()
    server.checking_model_que_from_kafka()