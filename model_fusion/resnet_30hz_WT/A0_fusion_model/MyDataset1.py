'''
数据载入
'''

from torch.utils.data import Dataset  
import numpy as np

class MyDataset(Dataset):

    def __init__(self, data_file, label_file):
        self.data = np.loadtxt(data_file,dtype=np.float32,delimiter=',')
        self.label = np.loadtxt(label_file,dtype=np.int64)
        
    def __getitem__(self, idx):
        return self.data[idx], self.label[idx]

    def __len__(self):
        return self.label.shape[0]



