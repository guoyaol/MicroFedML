import socket
import os
import sys
import time
import numpy
import torch
from kafka import KafkaProducer, KafkaConsumer,TopicPartition
import logging
logging.basicConfig(level=logging.DEBUG)

counter = 0

# SRV = os.getenv('SERVER_ADDRESS') #'0.0.0.0'#
# PORT = int(os.getenv('SERVER_PORT')) #13333#

# cli_id = int(os.environ.get('HOSTNAME')[-1]) #int(sys.argv[1])
bs_name = "kafka-service:9092"
# Define the configuration for the Kafka producer
conf = {"bootstrap_servers": bs_name,
        "max_request_size": 10485880,
        "value_serializer": lambda m: m,
        }
        # "buffer.memory": str(10485880 * 3),}
producer = KafkaProducer(**conf)


topic_partition = 0  ##topic partition in kafka, not model, always 0 now

# create a topic partition object
consumer_topics = [f"LOOPTEST"]
consumer_tps = [TopicPartition(topic=topic, 
                                partition=topic_partition) for topic in consumer_topics]
# offset = 0

consumer_conf = {
    'bootstrap_servers': bs_name,
    'group_id': f'Client_',
    'auto_offset_reset': 'earliest',
    "fetch_max_bytes": 10485880,
}
consumer = KafkaConsumer(**consumer_conf)
# consumer.subscribe(consumer_topics)
consumer.assign(consumer_tps)
print("client init done!")
model_size = 100000
# while 1:
start_time = time.perf_counter()
model = torch.randn((model_size,))
print(f"Loop {counter} produce begins")
# from IPython import embed; embed()

producer.send(topic="LOOPTEST", key=f"LOOPTEST_KEY".encode('utf-8'), value=model[1:])

print(f"Loop {counter} produce ends")

print(f"Loop {counter} consume begins")

# msgs = consumer.poll(timeout_ms=1000, max_records=1, update_offsets=True)
# print(msgs)
# consumer.commit()
print(f"Loop {counter} consume ends")



counter += 1
end_time = time.perf_counter()  # record the end time
elapsed_time = int((end_time - start_time) * 1000)  # calculate elapsed time in milliseconds
print(f"Loop {counter} ends, took {elapsed_time} seconds to execute.")
print("")
time.sleep(2.0)

