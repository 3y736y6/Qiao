from scipy.fft import fft, fftfreq
from scipy.signal import stft


class Operate_RawData:
    '''
    param: txtdata_path: the path of the txt data
    param: channel: the sample_channel of the data
    param: start_idx: the start index of the data
    param: length: the length of the data
    func: 从txt文本中,指定通道,指定数据起始位置,指定数据长度,获取一段数据
    '''
    def __init__(self,txtdata_path,channel,start_idx,length):
        self.data_path = txtdata_path
        self.data_list = []

        with open(self.data_path, 'r') as file:
            for i in range(start_idx,start_idx + length):
                line = file.readline().split() # one row has 5 number
                self.data_list.append(float(line[channel-1]))
    def get_raw_data_example(self,idx):
        return self.data_list[idx]

    def get_raw_data(self):
        return self.data_list
    

