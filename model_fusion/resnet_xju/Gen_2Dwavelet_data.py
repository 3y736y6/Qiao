import numpy as np
import matplotlib.pyplot as plt
import pywt
import pandas as pd
import pickle
import os

# 生成小波变换数据，压缩到128*128

datapath = '0.4A_1500n_Data_1D_R1_Train.dat'
save_path = 'Wavelet2D_data_shape2048.pkl'

start_idx = 0
end_idx = 4800 # 采样个数 4800 采样长度2048


def Gen_2D_wavelet(start_idx,end_idx):
    # .dat文件中没有首行信息，数据以 空格(\s+) 分割
    df = pd.read_csv(datapath, header = None ,sep='\s+')
    datalist = []
    fs = 20480
    # 小波尺度
    totalscal = 128

    for i in range(start_idx,end_idx):
        data_ndarray = np.array(df.iloc[i])

        wavename1 = 'morl'  # 小波名

        fc1 = pywt.central_frequency(wavename1)
        cparam1 = 2 * fc1 * totalscal  
        scales1 = cparam1 / np.arange(totalscal, 0, -1)
        

        # 进行连续小波变换
        coefficients1, frequencies1 = pywt.cwt(data_ndarray, scales1, wavename1, 1/fs) 
        # 返回 （128，2048）和 （128，）  第二个128用于对应第一个128，表示128刻度的频率
        # 小波系数矩阵绝对值
        amp1 = abs(coefficients1)

        
        #绘制
        # 根据采样频率 sampling_period 生成时间轴 t
        # t = np.arange(len(data_ndarray)) / fs

        # plt.contourf(t, frequencies1, amp1, cmap='jet')
        # plt.title('morl')
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # plt.show()
        
        # 取平均值压缩
        # split_array = amp1.reshape(128, 128, 16)  # 每行 128 个区域，每个区域 16 个元素
        # mean_array = split_array.mean(axis=2) # (128, 128)
        

        datalist.append(amp1)
    # 生成二进制文件保存二维数据列表
    with open('xju_wavelet2D_shape2048.pkl', 'wb') as f:
        pickle.dump(datalist, f)
        print("load:",len(datalist))



Gen_2D_wavelet(start_idx,end_idx)


# # 读取二进制文件保存的二维数据列表
# with open(save_path, 'rb') as f:
#     loaded_arrays_list = pickle.load(f)
#     print(len(loaded_arrays_list))
#     print(loaded_arrays_list[0])
#     print(type(loaded_arrays_list))
