import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft
import pandas as pd
import pickle
import os

datapath = 'bj_30hz_2channel_1D_data.csv'
save_path = 'bj_STFT2D_2channel_data.pkl'
start_idx = 0
end_idx = 5000
# 将原始 5k s个一维振动数据进行stft变换，得到4800个时频二维数据，将其放入list中，使用二进制格式保存。(二进制中会保存数据的结构维度等信息)
def Gen_2D_stft(start_idx,end_idx):
    # no header,first column is index 0
    df = pd.read_csv(datapath, header = None ,sep=',')   # 读取csv文件 自动转换为了float64 
    datalist = []
    # print(df.head())

    for i in range(start_idx,end_idx):
        data_ndarry = np.array(df.iloc[i])
        f, t, complex_list = stft(
            x = data_ndarry,
            fs = 48000,  # 采样频率
            nperseg = 32,     # 默认256
            noverlap = 16,    # 默认为None，即nperseg/2
            )  
        magnitude = np.abs(complex_list)              # complex_list复数列表取正值丢弃重复信息
        # print(magnitude.shape)
        # print(type(magnitude))

        
        # plt.figure(figsize=(11, 4))
        # plt.pcolormesh(t, f, magnitude, vmin=0, vmax=np.abs(complex_list).max(), shading='gouraud')
        # plt.title('STFT Magnitude')
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # plt.colorbar(label='Magnitude')
        # plt.show()

        datalist.append(magnitude)
    # 生成二进制文件保存二维数据列表
    with open(save_path, 'wb') as f:
        pickle.dump(datalist, f)
        print("load:",len(datalist))

    return datalist

Gen_2D_stft(start_idx,end_idx)


# # 读取二进制文件保存的二维数据列表
# with open(save_path, 'rb') as f:
#     loaded_arrays_list = pickle.load(f)
#     print(len(loaded_arrays_list))
#     print(loaded_arrays_list[0])
#     print(type(loaded_arrays_list))

