import csv
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft
import pandas as pd
import copy
# 四通道 前三通道可用
# (14450688, 4) data.shape
data_channel =1
start_idx = 0 # 从文件中的哪个点开始取数据
every_cla_length = 1000
sample_length = 1536

classification = ['normal','broken','missing_tooth','root_crack','wear']
data_path1 ={ 'normal':'./data/channel_1/N1_30.MAT',
             'broken':'./data/channel_1/B1_30.MAT',
             'missing_tooth':'./data/channel_1/M1_30.MAT',
             'root_crack':'./data/channel_1/R1_30.MAT',
             'wear':'./data/channel_1/W1_30.MAT'
            } 
data_path2 ={ 'normal':'./data/channel_2/N2_30.MAT',
             'broken':'./data/channel_2/B2_30.MAT',
             'missing_tooth':'./data/channel_2/M2_30.MAT',
             'root_crack':'./data/channel_2/R2_30.MAT',
             'wear':'./data/channel_2/W2_30.MAT'
            } 
# data_length = data['Data'].shape[0]
data_one_row = []
data_list = []


for cla in classification:
    data = loadmat(data_path2[cla])
    for i in range(start_idx,start_idx + every_cla_length):

        for j in range(i * sample_length, (i + 1) * sample_length):
            data_one_row.append(data['Data'][j][data_channel])

        data_list.append(copy.deepcopy(data_one_row))
        data_one_row.clear()
        

with open('bj_30hz_2channel_1D_data.csv','w') as file:
    for i in data_list:
        i = str(i) 
        file.writelines(i[1:-1]+'\n')   # 头尾有[] 列表符号 去掉

with open('lable_5.csv','w',newline= '\n') as file: # 创造 1-5  label
    for j in range(1,len(classification)+1):
        for i in range(every_cla_length):
            file.writelines(str(j) +'\n')

