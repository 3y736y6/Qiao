import torch  
import numpy as np  
from MyDataset2 import MyDataset2
import time

# 输入一个数据进行预测 并 计算预测速度
start = time.time()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")  

# 数据  抽取第 idx 个值
# inputs=train_data[0]     --train_data[idx]  return(x,x)  --则type(inputs) = tuple

train_data = MyDataset2('STFT2D_data.pkl','STFT2D_labek.dat')
idx = 1700
input,lable=train_data[idx] # 数组对象
input = torch.from_numpy(input)  # 转化为张量
input = input.unsqueeze(0)  # 增加维度将(feature)转换为(1,feature)---训练时数据为 (batch,feature) 
input = input.float().unsqueeze(1).repeat(1, 3, 1, 1) # (batch_size,W,H)-->(batch_size,3,W,H)
input = input.to(device)  



# 加载模型  
model = torch.load('model\model_Resnet50.pth',map_location=device)  
model = model.to(device)  
model.eval()  # 将模型设置为评估模式

# 进行预测  
with torch.no_grad():  # 不需要计算梯度，也不会进行反向传播，这可以减少内存消耗并加速预测过程  
    predictions = model(input)  # 得到模型的输出  
print(predictions)
# 根据模型的输出处理预测结果  
classes = ('A','B','C','D','E','F')

predicted_class = predictions.argmax(dim=1).item()  # 概率最高的类别   
print(f"Predicted class: {classes[predicted_class]}")

end = time.time()
print('GoogleNet_time:{}'.format(end-start))