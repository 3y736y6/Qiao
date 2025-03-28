import torch  
import numpy as np  
from MyDataset import MyDataset
import time

start = time.time()

# 确保你在预测时使用了与训练时相同的设备（CPU或GPU）  
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")  

# 数据  抽取第 idx 个值
# inputs=train_data[0]     --train_data[idx]  return(x,x)  --则type(inputs) = tuple

train_data = MyDataset('./Data/xc_src01_test2.dat','./Data/xc_src01_testlabel2.dat')
idx = 100
input,lable=train_data[idx] # 数组对象
input = torch.from_numpy(input)  # 转化为张量
input = input.unsqueeze(0)  # 增加维度将(feature)转换为(1,feature)---训练时数据为2维 (batch,feature) 
input= input.to(device)
size_tmp = input.shape
input.resize_(size_tmp[0], 1, size_tmp[1])



# 加载模型  
model = torch.load('1Googlenet\model\model_googlenetv2_xc_src_01_1.pkl',map_location=device)  
model = model.to(device)  
model.eval()  # 将模型设置为评估模式

# 进行预测  
with torch.no_grad():  # 不需要计算梯度，也不会进行反向传播，这可以减少内存消耗并加速预测过程  
    predictions = model(input)  # 得到模型的输出  
print(predictions)
# 根据模型的输出处理预测结果  
classes = ('Z','W1','W2','N1','N2','G1','G2')
predicted_class = predictions.argmax(dim=1).item()  # 概率最高的类别   
print(f"Predicted class: {classes[predicted_class]}")

end = time.time()
print('GoogleNet_time:{}'.format(end-start))