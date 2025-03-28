'''
数据载入
'''

from torch.utils.data import Dataset  
import numpy as np

class MyDataset(Dataset):

    def __init__(self, data_file, label_file):
        '''
        利用numpy读取数据
        :param data_file: 数据集文件
        :param label_file: 标签集文件
        '''
        self.data = np.loadtxt(data_file,dtype=np.float32,delimiter=',')
        self.label = np.loadtxt(label_file,dtype=np.float32)
        

    def __getitem__(self, idx):
        '''
        返回一条数据
        :param idx:
        :return:
        '''
        return self.data[idx], self.label[idx]

    def __len__(self):
        '''
        数据长度
        :return:
        '''
        return self.label.shape[0]



