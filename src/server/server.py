import socket
import sys
import os



class Server(object):
    """Class for implementing center server orchestrating the whole process of federated learning
    
    At first, center server distribute model skeleton to all participating clients with configurations.
    While proceeding federated learning rounds, the center server samples some fraction of clients,
    receives locally updated parameters, averages them as a global parameter (model), and apply them to global model.
    In the next round, newly selected clients will recevie the updated global model as its local model.  

    """
    def __init__(self, ):
        self.clients = []
        self.clients_values = {}
        self.model_size = 100
        
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
        
    def receiving_model_from_connection(self, conn, client_address):
        print(f'Receiving model from the client {client_address} start!')
        conn.settimeout(2)
        received = ""
        while True:
            try:
                data = conn.recv(64)
                if len(data) > 0:
                    received += self.unmarshall(data)
                    print(received)
                else:
                    break
            except Exception as e:
                break
        model = received[0]
        self.clients_values[client_address] = model
        self.clients.append((conn, client_address))
        print(f'Receiving model from the client {client_address} done!')