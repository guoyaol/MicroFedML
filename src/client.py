import gc
import pickle
import logging

import torch
import torch.nn as nn

from torch.utils.data import DataLoader
from .utils import create_datasets

logger = logging.getLogger(__name__)


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
    #create_datasets(self.data_path, self.dataset_name, self.num_clients, self.num_shards, self.iid)
    def __init__(self, client_id, local_datapath, device, dataset_name, num_clients, num_shards, iid):
        """Client object is initiated by the center server."""
        local_datasets, _, local_test_datasets = create_datasets(local_datapath, dataset_name, num_clients, num_shards, iid)

        self.id = client_id
        self.train_data = local_datasets[client_id]
        self.test_data = local_test_datasets[client_id]
        self.device = device
        self.__model = None
        self.model_tensor = None

    def read_data(id, data_path):
        """Read local data from pickle file."""
        with open(data_path, "rb") as f:
            data = pickle.load(f)
        return data[id]

    @property
    def model(self):
        """Local model getter for parameter aggregation."""
        return self.__model

    @model.setter
    def model(self, model):
        """Local model setter for passing globally aggregated model parameters."""
        self.__model = model

    def __len__(self):
        """Return a total size of the client's local data."""
        return len(self.train_data)

    def setup(self, **client_config):
        """Set up common configuration of each client; called by center server."""
        self.train_dataloader = DataLoader(self.train_data, batch_size=client_config["batch_size"], shuffle=True)
        self.test_dataloader = DataLoader(self.test_data, batch_size=client_config["batch_size"], shuffle=False)
        self.local_epoch = client_config["num_local_epochs"]
        self.criterion = client_config["criterion"]
        self.optimizer = client_config["optimizer"]
        self.optim_config = client_config["optim_config"]

    def client_update(self):
        """Update local model using local dataset."""
        self.model.train()
        self.model.to(self.device)

        optimizer = eval(self.optimizer)(self.model.parameters(), **self.optim_config)
        for e in range(self.local_epoch):
            for data, labels in self.train_dataloader:
                data, labels = data.float().to(self.device), labels.long().to(self.device)
  
                optimizer.zero_grad()
                outputs = self.model(data)
                loss = eval(self.criterion)()(outputs, labels)

                loss.backward()
                optimizer.step() 

                if self.device == "cuda": torch.cuda.empty_cache()               
        self.model.to("cpu")
        # self.grad = get_grad(xxx)
        # self.compressed_grad = self.compress(self.grad)
        # self.model_tensor =  self.compress(self.marshall(self.model))

    def marshall(self, state_dict):
        # convert the state_dict to a tensor
        tensor = torch.cat([v.flatten() for v in state_dict.values()])
        return tensor

    def client_evaluate_train(self):
        """Evaluate local model using local dataset (same as training set for convenience)."""
        self.model.eval()
        self.model.to(self.device)

        test_loss, correct = 0, 0
        with torch.no_grad():
            for data, labels in self.train_dataloader:
                data, labels = data.float().to(self.device), labels.long().to(self.device)
                outputs = self.model(data)
                test_loss += eval(self.criterion)()(outputs, labels).item()
                
                predicted = outputs.argmax(dim=1, keepdim=True)
                correct += predicted.eq(labels.view_as(predicted)).sum().item()

                if self.device == "cuda": torch.cuda.empty_cache()
        self.model.to("cpu")

        test_loss = test_loss / len(self.train_dataloader)
        test_accuracy = correct / len(self.train_data)

        message = f"\t[Client {str(self.id).zfill(4)}] ...finished evaluation!\
            \n\t=> client loss(train): {test_loss:.4f}\
            \n\t=> client accuracy(train): {100. * test_accuracy:.2f}%\n"
        print(message, flush=True); logging.info(message)
        del message; gc.collect()

        return test_loss, test_accuracy

    def client_evaluate_test(self):
        """Evaluate local model using local test dataset."""
        self.model.eval()
        self.model.to(self.device)

        test_loss, correct = 0, 0
        with torch.no_grad():
            for data, labels in self.test_dataloader:
                data, labels = data.float().to(self.device), labels.long().to(self.device)
                outputs = self.model(data)
                test_loss += eval(self.criterion)()(outputs, labels).item()
                
                predicted = outputs.argmax(dim=1, keepdim=True)
                correct += predicted.eq(labels.view_as(predicted)).sum().item()

                if self.device == "cuda": torch.cuda.empty_cache()
        self.model.to("cpu")

        test_loss = test_loss / len(self.test_dataloader)
        test_accuracy = correct / len(self.test_data)

        message = f"\t[Client {str(self.id).zfill(4)}] ...finished evaluation!\
            \n\t=> client loss(test): {test_loss:.4f}\
            \n\t=> client accuracy(test): {100. * test_accuracy:.2f}%\n"
        print(message, flush=True); logging.info(message)
        del message; gc.collect()

        return test_loss, test_accuracy
