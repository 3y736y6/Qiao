group = 800  # 每一类长度
classificaion = 6   # 类别数
save_path = "0.4A_1500n_Data_1D_R1_Train_Lable.dat"

def gen_fftdata():
    with open(save_path,'a') as file:
        for i in range(1,classificaion + 1):
            for _ in range(0,group):
                line =f'{i}\n' 
                file.write(line)

gen_fftdata()    



