import socket
import sys
import os
from kafka import KafkaProducer, KafkaConsumer, TopicPartition


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
        self.model_size = 1000000
        self.shard_id = shard_id

        self.consumer_topic = f"shard_{shard_id}"
        self.topic_partition = 0  ##topic partition in kafka, not model, always 0 now
        self.threshold = 2
        # create a topic partition object
        self.consumer_tp = TopicPartition(topic=self.consumer_topic, partition=self.topic_partition)
        # self.offset = 0

        consumer_conf = {
            'bootstrap_servers': 'kafka-service.kafka:9092',
            'group_id': 'Servers',
            'auto_offset_reset': 'earliest',
            "fetch_max_bytes": 10485880,
        }

        self.consumer = KafkaConsumer(**consumer_conf)
        self.consumer.subscribe([self.consumer_topic])

        # Define the configuration for the Kafka producer
        self.producer_topic = f"shard_{shard_id}_authorative"
        producer_conf = {"bootstrap_servers": "kafka-service.kafka:9092",
                "max_request_size": 10485880,
                "value_serializer": lambda m: m,
                }
                # "buffer.memory": str(10485880 * 3),}
        self.producer = KafkaProducer(**producer_conf)
        
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

    def send_model_back2kafka(self, model):
        print(f"Server {self.shard_id} start sending to kafka!")
        msg = self.marshall(model)

        # Send the message to the Kafka topic
        self.producer.send(topic=self.producer_topic, key=f"Server {self.shard_id}".encode('utf-8'), value=msg)

        # Wait for any outstanding messages to be delivered and delivery reports received
        self.producer.flush()
        print(f"Server {self.shard_id}  done sending to kafka!")
    
    def receiving_model_from_kafka(self,):
        print(f'Receiving model from kafka start!')
        try:
            
            # Poll for new messages
            while True:
                # 
                
                msgs = self.consumer.poll(timeout_ms=1000, max_records=self.threshold, update_offsets=True)
                # from IPython import embed; embed()
                
                # 
                
                
                if not msgs:
                    continue
                # self.offset += len(msgs)
                # self.consumer.seek(self.consumer_tp, self.offset)
                msgs = msgs[self.consumer_tp]
                self.consumer.commit()
                break

            # Extract the message values
            messages = [msg.value.decode('utf-8') for msg in msgs]
            
            # Process the messages if the threshold is reached
            assert len(messages) >= self.threshold
            model = self.average_model(messages)
            print("Averaged model:", model[0], len(model))
            self.send_model_back2kafka(model[0])
            print(f'Receiving model from kafka, aggegate and produce back done!')
        except KeyboardInterrupt:
            pass
        
    def checking_model_que_from_kafka(self,):
        
        
        # Get the current high watermark and last committed offset for the partition
        high_watermark_offset = self.consumer.end_offsets([self.consumer_tp])[self.consumer_tp]
        
        last_committed_offset = self.consumer.committed(self.consumer_tp)
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