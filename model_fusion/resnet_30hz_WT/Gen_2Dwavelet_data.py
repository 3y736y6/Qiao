import numpy as np
import matplotlib.pyplot as plt
import pywt
import pandas as pd
import pickle
import os

# 生成小波变换数据，压缩到128*128

datapath = 'bj_30hz_2channel_1D_data.csv'
save_path = 'bj_wavelet_2channel_reshape128x128.pkl'
start_idx = 0
end_idx = 5000

def Gen_2D_wavelet(start_idx,end_idx):

    df = pd.read_csv(datapath, header = None ,sep=',') 
    datalist = []
    fs = 48000
    T = 1/fs
    # 小波尺度
    totalscal = 128
    # 采样时长
    sampling_period = 1536
    
    for i in range(start_idx,end_idx):
        data_ndarray = np.array(df.iloc[i])


        wavename1 = 'morl' #
        fc1 = pywt.central_frequency(wavename1)
        cparam1 = 2 * fc1 * totalscal  
        scales1 = cparam1 / np.arange(totalscal, 0, -1)
        

        # 进行连续小波变换
        coefficients1, frequencies1 = pywt.cwt(data_ndarray, scales1, wavename1, 1/fs) 
        # print(coefficients1.shape,frequencies1.shape)
        # 返回 （128，1536）和 （128，）  第一个128用于对应第一个128，表示128刻度的频率
        # 小波系数矩阵绝对值
        amp1 = abs(coefficients1)
        # print(amp1.shape)

    # 生成二进制文件保存二维数据列表128*128
        # # 取平均值压缩
        # split_array = amp1.reshape(128, 128, 12)  # 每行 128 个区域，每个区域 12 个元素
        # mean_array = split_array.mean(axis=2) # (128, 128)
        

        # datalist.append(mean_array)
    # with open(save_path, 'wb') as f:
    #     pickle.dump(datalist, f)
    #     print("load:",len(datalist))


    # 生成二进制文件保存二维数据列表128*1536
        datalist.append(amp1)
    with open('bj_wavelet_2channel_reshape128x1536.pkl', 'wb') as f:
        pickle.dump(datalist, f)
        print("load:",len(datalist))

        # # 根据采样频率 sampling_period 生成时间轴 t
        # t = np.arange(len(data_ndarray)) / fs

        # plt.contourf(t, frequencies1, amp1, cmap='jet')
        # plt.title('morl')
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # plt.show()

Gen_2D_wavelet(start_idx=0,end_idx=5000)


# 读取二进制文件保存的二维数据列表
with open('bj_wavelet_2channel_reshape128x1536.pkl', 'rb') as f:
    loaded_arrays_list = pickle.load(f)
