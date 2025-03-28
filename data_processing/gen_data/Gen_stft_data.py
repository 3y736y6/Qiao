import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft
import pandas as pd
import pickle
nperseg = 32
fs = sampling_rate = 20480
datapath = '0.4A_1500n_Data_1D_R1_Train.dat'
save_path = 'C:/Users/Q/Desktop/data/0.4A_1500n_Data_1D_R1_Train_STFT.dat'
start_idx = 0
end_idx = 4800
def Gen_Pic_stft(start_idx,end_idx):
    # no header,first column is index 0
    df = pd.read_csv(datapath, header = None ,sep='\s+') #(4800,2048)   sep = ',' 表示数据是以空格分隔
    # print(df.shape)
    datalist = []

    for i in range(start_idx,end_idx):
        data_ndarry = np.array(df.iloc[i])
        f, t, complex_list = stft(
            x = data_ndarry,
            fs = 20480,  # 采样频率
            nperseg = 32,     # 默认256
            noverlap = 16,    # 默认为None，即nperseg/2
            )  
        magnitude = np.abs(complex_list)                                # complex_list复数列表取正值 
        # print(magnitude.shape)
        # print(type(magnitude))

        ## 绘制图像
        # plt.figure(figsize=(11, 4))
        # plt.pcolormesh(t, f, magnitude, vmin=0, vmax=np.abs(complex_list).max(), shading='gouraud')
        # plt.title('STFT Magnitude')
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # plt.colorbar(label='Magnitude')
        # plt.show()

        datalist.append(magnitude)

    with open('vibration_list.pkl', 'wb') as f:
        pickle.dump(datalist, f)
        print("load:",len(datalist))

    return datalist

Gen_Pic_stft(start_idx,end_idx)

# with open('vibration_list.pkl', 'rb') as f:
#     loaded_arrays_list = pickle.load(f)
    # print(len(loaded_arrays_list))
    # print(loaded_arrays_list[0])

