# 读取   二进制训练数据    和   dat格式的标签数据
from torch.utils.data import Dataset  
import numpy as np
import pickle
class MyDataset2(Dataset):
    def __init__(self, data_file, label_file):
        with open(data_file, 'rb') as f:
            self.data = pickle.load(f)
        self.label = np.loadtxt(label_file,np.int64)
    def __getitem__(self, idx):
        return self.data[idx], self.label[idx]
    def __len__(self):
        return len(self.label)



