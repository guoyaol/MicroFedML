import json
import numpy as np
import os
from collections import defaultdict

import torch


def batch_data(data, batch_size, seed):
    '''
    data is a dict := {'x': [numpy array], 'y': [numpy array]} (on one client)
    returns x, y, which are both numpy array of length: batch_size
    '''
    data_x = data['x']
    data_y = data['y']

    # randomly shuffle data
    np.random.seed(seed)
    rng_state = np.random.get_state()
    np.random.shuffle(data_x)
    np.random.set_state(rng_state)
    np.random.shuffle(data_y)

    # loop through mini-batches
    for i in range(0, len(data_x), batch_size):
        batched_x = data_x[i:i+batch_size]
        batched_y = data_y[i:i+batch_size]
        yield (batched_x, batched_y)


def read_dir(data_dir):
    clients = []
    groups = []
    data = defaultdict(lambda : None)

    files = os.listdir(data_dir)
    files = [f for f in files if f.endswith('.json')]
    for f in files:
        file_path = os.path.join(data_dir,f)
        with open(file_path, 'r') as inf:
            cdata = json.load(inf)
        clients.extend(cdata['users'])
        if 'hierarchies' in cdata:
            groups.extend(cdata['hierarchies'])

        # for user, data_xy in data.items():
        #     for k in data_xy.keys():
        #         # print(user, k, type(data[user][k]), type(cdata['user_data'][user][k]))
        #         data[user][k].extend(cdata['user_data'][user][k])
        data.update(cdata['user_data'])

    clients = list(sorted(data.keys()))
    # from IPython import embed; embed()
    
    return clients, groups, data


def read_data(train_data_dir, test_data_dir, client_id):
    '''parses data in given train and test data directories

    assumes:
    - the data in the input directories are .json files with 
        keys 'users' and 'user_data'
    - the set of train set users is the same as the set of test set users
    
    Return:
        clients: list of client ids
        groups: list of group ids; empty list if none found
        train_data: dictionary of train data
        test_data: dictionary of test data
    '''
    train_clients, train_groups, train_data = read_dir(train_data_dir)
    test_clients, test_groups, test_data = read_dir(test_data_dir)
    assert train_clients == test_clients
    assert train_groups == test_groups

    # if not client_id:
    #     return train_clients, train_groups, train_data, test_data
    # else:
    return train_data[str(client_id)], test_data[str(client_id)]

class CustomDataset(torch.utils.data.Dataset):
    'Characterizes a dataset for PyTorch'
    def __init__(self, data):
            'Initialization'
            self.labels = data['y']
            self.features = data['x']

    def __len__(self):
            'Denotes the total number of samples'
            return len(self.labels)

    def __getitem__(self, index):
            'Generates one sample of data'
            # Select sample
            label = self.labels[index]
            feature = self.features[index]

            # Convert feature to tensor
            feature_tensor = torch.tensor(feature, dtype=torch.float32)

            return feature_tensor, label

def generate_dataset(local_data_path, local_id):
    train_data, test_data = read_data(local_data_path+'/train', local_data_path+'/test', client_id=local_id)
    train_dataset = CustomDataset(train_data)
    test_dataset = CustomDataset(test_data)
    return train_dataset, test_dataset

if __name__ == "__main__":
    # train_clients, train_groups, train_data, test_data = read_data('./femnist_v1/train', './femnist_v1/test', 0)
    train_data, test_data = read_data('./femnist_v1/train', './femnist_v1/test', 0)
    
