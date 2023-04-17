import socket
import os
import sys
import time

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
    def __init__(self, client_id, server_address):
        self.id = client_id
        self.model = client_id % 10
        self.model_size = 1000
        self.server_address = server_address
        

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
    
