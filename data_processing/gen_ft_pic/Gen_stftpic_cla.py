import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft
import pandas as pd
import pickle
import os

#将经过4800个数据进行stft变换，得到4800个时频矩阵，生成对应的图片，保存至cla_list所包含文件名的文件夹下
nperseg = 32
fs = sampling_rate = 20480
datapath = '0.4A_1500n_Data_1D_R1_Train.dat'
# save_path = 'C:/Users/Q/Desktop/data/0.4A_1500n_Data_1D_R1_Train_STFT.dat'
start_idx = 0
end_idx = 4800
every_cla_length = 800
classification_num = 6 
def mkfile(file):
    if not os.path.exists(file):
        os.makedirs(file)
def Gen_Pic_stft(every_cla_length,classification_num):
    # no header,first column is index 0
    df = pd.read_csv(datapath, header = None ,sep='\s+') #(4800,2048) 
    cla_list = ['normal','eccentric','broken_tooth','half_broken_tooth','surface_wear','crack']
    mkfile('./STFT_pic')
    for j in range(0,classification_num):

        mkfile('./STFT_pic/'+cla_list[j])
        for i in range(j*every_cla_length,(j+1)*every_cla_length):
            data_ndarry = np.array(df.iloc[i])
            f, t, complex_list = stft(
                x = data_ndarry,
                fs = 20480,  # 采样频率
                nperseg = 32,     # 默认256
                noverlap = 16,    # 默认为None，即nperseg/2
                )  
            magnitude = np.abs(complex_list)                   # complex_list复数列表取正值 x轴为时间轴 y轴为频率轴

            fig = plt.figure(figsize=(11, 4))
            plt.pcolormesh(t, f, magnitude, vmin=0, vmax=np.abs(complex_list).max(), shading='gouraud') # x,y,2 dim array，，，
            plt.title('STFT Magnitude')
            plt.ylabel('Frequency [Hz]')
            plt.xlabel('Time [sec]')
            # plt.colorbar(label='Magnitude')
            # plt.show()

            save_path = './STFT_pic/'+cla_list[j]+'/'
            pic_name = cla_list[j]+str(i)
            plt.savefig(save_path+pic_name+'.png')
            plt.close()
    # return magnitude

Gen_Pic_stft(every_cla_length = 800,classification_num = 6)
