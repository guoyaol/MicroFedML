import socket
import os
import sys
import time
import json
from kafka import KafkaProducer, KafkaConsumer,TopicPartition

class Client(object):
    """Class for client object having its own (private) data and resources to train a model.
    Participating client has its own dataset which are usually non-IID compared to other clients.
    Each client only communicates with the center server with its trained parameters or globally aggregated parameters.
    Attributes:
        id: Integer indicating client's id.
        data: torch.utils.data.Dataset instance containing local data.
        device: Training machine indicator (e.g. "cpu", "cuda").
        __model: torch.nn instance as a local model.
    """
    def __init__(self, client_id, server_address, serverless = False):
        self.id = client_id
        self.model = client_id % 10
        self.model_size = 1000000
        self.server_address = server_address
        
        
        if serverless:
            # Define the topic to send messages to

            # Define the configuration for the Kafka producer
            conf = {"bootstrap_servers": "kafka-service.kafka:9092",
                    "max_request_size": 10485880,
                    "value_serializer": lambda m: m,
                    }
                    # "buffer.memory": str(10485880 * 3),}
            self.producer = KafkaProducer(**conf)
            self.shards = 1

            self.topic_partition = 0  ##topic partition in kafka, not model, always 0 now

            # create a topic partition object
            self.consumer_topics = [f"shard_{shard_id}_authorative" for shard_id in range(self.shards)]
            self.consumer_tps = [TopicPartition(topic=topic, 
                                            partition=self.topic_partition) for topic in self.consumer_topics]
            # self.offset = 0

            consumer_conf = {
                'bootstrap_servers': 'kafka-service.kafka:9092',
                'group_id': f'Client_{self.id}',
                'auto_offset_reset': 'earliest',
                "fetch_max_bytes": 10485880,
            }
            self.consumer = KafkaConsumer(**consumer_conf)
            self.consumer.subscribe(self.consumer_topics)

    def __del__(self):
        pass
        # self.sock.close()

    def setup(self, **client_config):
        pass

    def client_update(self):
        print(f"Client {self.id} start training!")
        time.sleep(2.4)
        print(f"Client {self.id} done training!")

    def client_evaluate(self):
        print(f"Client {self.id} start testing!")
        time.sleep(2.0)
        print(f"Client {self.id} done testing!")
    
    def marshall(self, model):
        return (str(model) * self.model_size).encode('utf-8')

    def unmarshall(self, blob):
        return blob.decode('utf-8')

    def get_param_from_server(self):
        print(f"Client {self.id} start receiving!")
        amount_received = 0
        amount_expected = self.model_size

        while amount_received < amount_expected:
            data = self.unmarshall(self.sock.recv(64))
            amount_received += len(data)
        self.model = int(data[0])
        self.sock.close()
        print(f"Client {self.id} done receiving!")

    def send_param_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while 1:
            try:
                self.sock.connect(self.server_address)
                break
            except Exception as e:
                print(f"Client {self.id} Cannot connect to the server,", e)
                 
        print(f"Client {self.id} start sending!")
        msg = self.marshall(self.model)
        self.sock.sendall(msg)
        
        print(f"Client {self.id} done sending!")
    
    def send_param_to_kafka(self):

        # Create a large random Torch tensor
        # large_tensor = torch.randn(1000, 1000)
        print(f"Client {self.id} start sending to kafka!")
        msg = self.marshall(self.model)
        shard_size = len(msg) // self.shards
        # Convert the tensor to a JSON string
        # tensor_str = json.dumps(large_tensor.numpy().tolist())

        # Send the message to the Kafka topic
        for i in range(self.shards):
            start = i * shard_size
            end = start + shard_size
            if i == self.shards - 1:
                end = len(msg)
            self.producer.send(topic=f"shard_{i}", key=f"Client {self.id}".encode('utf-8'), value=msg[start:end])

        # Wait for any outstanding messages to be delivered and delivery reports received
        self.producer.flush()
        print(f"Client {self.id} done sending to kafka!")

    def get_param_from_kafka(self):
        print(f'Receiving model from kafka start!')
        model_shards = {}
        while len(model_shards) < self.shards:
            msgs = self.consumer.poll(timeout_ms=10000, max_records=self.shards, update_offsets=True)
            # from IPython import embed; embed()
            model_shards.update(msgs)
        self.consumer.commit()
        # Extract the message values
        # from IPython import embed; embed()
        messages = [model_shards[shard_name][0].value.decode('utf-8') for shard_name in self.consumer_tps]
        for msg in messages:
            print(len(msg))
        self.model = messages[0][0]
        print(f'Receiving model from kafka done!')

            