import socket
import sys
import os
from kafka import KafkaConsumer, TopicPartition


class Serverless(object):
    """Class for implementing center server orchestrating the whole process of federated learning
    
    At first, center server distribute model skeleton to all participating clients with configurations.
    While proceeding federated learning rounds, the center server samples some fraction of clients,
    receives locally updated parameters, averages them as a global parameter (model), and apply them to global model.
    In the next round, newly selected clients will recevie the updated global model as its local model.  

    """
    def __init__(self, shard_id):
        self.clients = []
        self.clients_values = {}
        self.model_size = 10000000
        self.shard_id = shard_id

        self.topic = f"shard_{shard_id}"
        self.topic_partition = 0  ##topic partition in kafka, not model, always 0 now
        self.threshold = 1
        # create a topic partition object
        self.tp = TopicPartition(topic=self.topic, partition=self.topic_partition)
        # self.offset = 0

        consumer_conf = {
            'bootstrap_servers': 'kafka-service.kafka:9092',
            'group_id': 'my_group',
            'auto_offset_reset': 'earliest',
            "fetch_max_bytes": 10485880,
        }

        self.consumer = KafkaConsumer(**consumer_conf)
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
        return clients_values[0]

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
    
    def receiving_model_from_kafka(self,):
        print(f'Receiving model from kafka start!')
        try:
            
            # Poll for new messages
            while True:
                # 
                
                msgs = self.consumer.poll(timeout_ms=1000, max_records=self.threshold, update_offsets=True)[self.tp]
                from IPython import embed; embed()
                
                
                if not msgs:
                    continue
                # self.offset += len(msgs)
                # self.consumer.seek(self.tp, self.offset)
                self.consumer.commit()
                break

            # Extract the message values
            messages = [msg.value.decode('utf-8') for msg in msgs]
            
            # Process the messages if the threshold is reached
            assert len(messages) >= self.threshold
            model = self.average_model(messages)
            print("Averaged model:", model)
            # self.transmit_model()
            print(f'Receiving model from kafka, aggegate and produce back done!')
        except KeyboardInterrupt:
            pass
        
    def checking_model_que_from_kafka(self,):
        
        
        # Get the current high watermark and last committed offset for the partition
        high_watermark_offset = self.consumer.end_offsets([self.tp])[self.tp]
        
        last_committed_offset = self.consumer.committed(self.tp)
       # Calculate the number of unprocessed messages
        unprocessed_messages = high_watermark_offset - last_committed_offset if last_committed_offset is not None else high_watermark_offset
        # unprocessed_messages = high_watermark_offset - self.offset 
        # print(unprocessed_messages)
        if unprocessed_messages >= self.threshold:
            # Trigger the function to consume messages
            self.receiving_model_from_kafka()
            
        else:
            # Wait for more messages to be produced
            # print(f'current unprocessed_messages num: {unprocessed_messages}')
            pass