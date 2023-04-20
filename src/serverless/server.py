import socket
import sys
import os
from confluent_kafka import Consumer, KafkaError


class Server(object):
    """Class for implementing center server orchestrating the whole process of federated learning
    
    At first, center server distribute model skeleton to all participating clients with configurations.
    While proceeding federated learning rounds, the center server samples some fraction of clients,
    receives locally updated parameters, averages them as a global parameter (model), and apply them to global model.
    In the next round, newly selected clients will recevie the updated global model as its local model.  

    """
    def __init__(self, partition_id):
        self.clients = []
        self.clients_values = {}
        self.model_size = 10000000
        self.partition_id = partition_id

        self.topic = f"partition_{partition_id}"
        self.partition = 0  ##topic partition, not model
        self.threshold = 3

        self.consumer_conf = {
            'bootstrap.servers': 'kafka-service.kafka:9092',
            'group.id': 'my_group',
            'auto.offset.reset': 'earliest'
        }

        self.consumer = Consumer(self.consumer_conf)
        self.consumer.subscribe([self.topic])
        
    def __del__(self):
        # for connection, client_address in self.clients:
        #     connection.close()
        pass
        
    def setup(self, **init_kwargs):
        pass

    def marshall(self, model):
        return (str(model) * self.model_size).encode('utf-8')

    def unmarshall(self, blob):
        return blob.decode('utf-8')

    def average_model(self, clients_values):
        return clients_values

    def transmit_model(self,):
        self.clients_values = self.average_model(self.clients_values)
        for connection, client_address in self.clients:
            print(f'Sending model back to the client {client_address} start!')
            client_model = self.marshall(self.clients_values[client_address])
            connection.sendall(client_model)
            print(f'Sending model back to the client {client_address} done!')
            # connection.close()
        self.clients = []
        self.clients_values = {}
        
    def checking_model_que_from_kafka(self, conn, client_address):
        print(f'Receiving model from the client {client_address} start!')
        # conn.settimeout(2)
        # received = ""
        # # while True:
        # #     try:
        # #         data = conn.recv(64)
        # #         if len(data) > 0:
        # #             received += self.unmarshall(data)
                    
        # #         else:
        # #             break
        # #     except Exception as e:
        # #         break
        # amount_received = 0
        # amount_expected = self.model_size

        # while amount_received < amount_expected:
        #     data = self.unmarshall(conn.recv(64))
        #     if len(data) > 0:
        #         received += data
        #     amount_received += len(data)
        # model = received[0]
        # print(received[0])
        # self.clients_values[client_address] = model
        # self.clients.append((conn, client_address))
        # print(f'Receiving model from the client {client_address} done!')

        # Get the current high watermark and last committed offset for the partition
        watermark_offsets = self.consumer.get_watermark_offsets(topic, partition)
        high_watermark_offset = watermark_offsets.high
        last_committed_offset = watermark_offsets.offsets[0]

        # Calculate the number of unprocessed messages
        unprocessed_messages = high_watermark_offset - last_committed_offset

        if unprocessed_messages >= self.threshold:
            # Trigger the function to consume messages
            # ...
        else:
            # Wait for more messages to be produced
            # ...