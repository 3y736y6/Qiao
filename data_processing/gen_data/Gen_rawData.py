import copy
import os
# 父列表随子列表内容更改而更改 用deepcopy
raw_data_path = "xxx"
gen_data_path = "0.4A_1500n_2channel_Data_1D_R1.dat"
start_idx = 0 # 数据开始索引
length = 2048 # 数据长度
group =10   # 条数
channel = 2   # 采样通道数
# file_num = 10 # 读取x个文件

NUM = 66      # 文件起始索引
dataBuff = []
data_list = []
txtdata_path6 = "C:/1/振动试验台数据/齿轮裂纹/0.4负载转速1500"# 73 - 83
txtdata_path5 = "C:/1/振动试验台数据/齿面磨损/0.5负载转速1500"# 116 - 127
txtdata_path4 = "C:/1/振动试验台数据/断半齿/0.4负载转速1500"# 144 - 154
txtdata_path3 = "C:/1/振动试验台数据/断齿/0.4负载转速1500"# 99 - 109
txtdata_path2 = "C:/1/振动试验台数据/偏心齿轮/0.4负载转速1500"# 91 - 101
txtdata_path1 = "C:/1/振动试验台数据/正常/0.4负载转速1500"# 66 - 76

txtdata_path = txtdata_path4
file_names=os.listdir(txtdata_path)

files = [file for file in file_names if os.path.isfile(os.path.join(txtdata_path, file))]

# # 打印所有文件的完整路径
# for file in files:
#     full_path = os.path.join(txtdata_path, file)
#     print(full_path)

def gen_fftdata(num):
    full_path = []
    for file in files:
        print(os.path.join(txtdata_path, file))
        full_path.append(os.path.join(txtdata_path, file))

    for i in range(0,num):
        with open(full_path[0], 'r') as file:
            for j in range(0,group):

                for i in range(start_idx,start_idx + length):
                    line = file.readline().split() # one row has 5 number
                    dataBuff.append((line[channel-1]))
                data_list.append(copy.deepcopy(dataBuff))
                dataBuff.clear()

        with open(gen_data_path,'a') as file:
            for j in range(0,group):
                line = ' '.join(data_list[j]) + '\n'
                file.write(line)


gen_fftdata(10)    



