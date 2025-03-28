import time
import numpy as np
import torch
from torch import nn, optim
from MyDataset import MyDataset
import GoogleNetV2_1D_CH1_SRC2 as GoogleNetV2_1D_CH1_SRC2
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime  
import  os
from GoogleNetV2_1D_CH1_Test2 import test

#tensorboard --logdir=./runs可视化查看指令
#根据日期实例化 数据记录文件
current_datetime = datetime.now()  
print("当前日期和时间:", current_datetime)
formatted_datetime = current_datetime.strftime("%Y.%m.%d_%H.%M.%S") 
summaryWriter = SummaryWriter(f"Wang_data/runs/{formatted_datetime}+Wang")

# 配置参数
batch_size = 32  # 每次喂入的数据量
learningrate = 0.001  # 学习率
step_size = 5  # 每n个epoch更新一次学习率
epoch_num = 25 # 总迭代次数
num_print = 50  #每n次batch打印一次

### 训练数据加载 生成一个实例
dataset = MyDataset('Wang_data/xc_src01_train2.dat','Wang_data/xc_src01_trainlabel2.dat')


# # 查看数据集的大小  
# print(len(train_data))   #7000
# print(type(train_data))   #<class 'MyDataset.MyDataset'>

# # 查看(第idx条)数据
# idx=1888
# print(train_data[idx])
# #(array([0.18702322, 0.17607737, 0.40415427, ..., 0.67580384, 0.7445435 ,0.6485875 ], dtype=float32), 2.0)
# #这是一个元组，第一个是一维向量(1645*1)，第二个是标签

# 将train_data[idx]第一个元素与第二个元素分别提取      
# sample, label = train_data[idx]  
# print(f"Sample shape:{sample.shape,type(sample)} , Label shape:{label.shape,type(label)}")
# Sample shape:(1645,)  每个(第idx)个Sample是一维的向量    sample为一个ndarray数组对象
# Label shape:()        Lable是标量,0维                   label 为一个浮点对象

### 加载数据 一个容器中包含7000/20=350个数据   shuffle洗牌
# train_loader = torch.utils.data.DataLoader(train_data,batch_size=batch_size,shuffle=True)

torch.manual_seed(19)
train_test_rate = 0.7
train_size = int(train_test_rate * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

train_loader = torch.utils.data.DataLoader(train_dataset,batch_size=batch_size, shuffle=True,)
test_loader = torch.utils.data.DataLoader(test_dataset,batch_size=batch_size, shuffle=False,)


# # 显示完整的批次数量
# print("Number of batches:", len(train_loader))  # Number of batches: 350 --- (总数)7000/(batch_size)20=350
# print("type of batches:",type(train_loader))    # <class 'torch.utils.data.dataloader.DataLoader'>


# # 获取一个批次的数据  enumerate函数--参数(数据，起始索引),返回值(索引值,数据值)
# for batch_idx, (inputs, labels) in enumerate(train_loader):  
#     if batch_idx == 0:  # 只查看第一个批次  
#         print("input shape:", inputs.shape,inputs.type())  # 显示数据的形状  # input shape: torch.Size([20, 1645])
#         print("lable shape:", labels.shape,inputs.type())  # 显示标签的形状  # lable shape: torch.Size([20])
#         break

# 是否使用GPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# 实例化定义的模型
model = GoogleNetV2_1D_CH1_SRC2.GoogLeNet_1D().to(device=device)
# 损失函数
criterion = nn.CrossEntropyLoss()
# adam优化器 
optimizer = optim.Adam(model.parameters(), lr=learningrate, weight_decay=0.001)
# 动态调整学习率
# scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=0.25)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=step_size)

# ### 喂一次预估整体时间
# total_samples = len(train_data)  
# total_iterations = (total_samples // batch_size) * epoch_num  
# start_time = time.time()  
# for i, (inputs, labels) in enumerate(train_loader):  
#     if i == 10:  # 01234 56789 十次迭代
#         break  
#     inputs, labels = inputs.to(device), labels.to(device)
#     size_tmp = inputs.shape
#     inputs.resize_(size_tmp[0], 1, size_tmp[1])
#     labels = labels.long()-1
#     optimizer.zero_grad()
#     outputs = model(inputs) 
#     loss = criterion(outputs, labels).to(device)
#     loss.backward()
#     optimizer.step()
# end_time = time.time()  
# single_iteration_time = (end_time - start_time)/10
# estimated_total_time = single_iteration_time * total_iterations  

# print(f"单次迭代时间: {single_iteration_time:.4f} 秒")  
# print(f"预估总训练时间: {estimated_total_time:.2f} 秒")  

##绘制网络
for i, (inputs, labels) in enumerate(train_loader):  
    if i == 1:  # i  0--249
        break  
    inputs, labels = inputs.to(device), labels.to(device)
    size_tmp = inputs.shape
    inputs.resize_(size_tmp[0], 1, size_tmp[1])
    summaryWriter.add_graph(model,inputs)
    print(inputs.shape) # torch.Size([20,1,1645])
# 结束后，inputs仍然为tensor([20,1645])
## print(inputs.shape) # torch.Size([20,1645])//试图在外部访问(inputs定义在内部)内部已经释放的变量，理论会报错无法访问


# 训练
loss_list = []
start = time.time()
correct = 0  
total = 0
for epoch in range(epoch_num):    #总次数 len(train_loader)=350  *  epoch=25
    running_loss = 0.0
    model.train()
    for i, (inputs, labels) in enumerate(train_loader, 0):       #i 0--349
        inputs, labels = inputs.to(device), labels.to(device)

        size_tmp = inputs.shape        # size_tmp ---torch.Size([20, 1645])
        inputs.resize_(size_tmp[0], 1, size_tmp[1])        # resize_(batch_size=20, 1, feature_length=1650)  [20*1*1650]
        labels = labels.long()-1            # 标签为1,2,3…… --> 0,1,2……

        outputs = model(inputs)  # 前向传播求出预测的值
        
        pred = outputs.argmax(dim=1)  # 返回每一行中最大值元素索引
        total += inputs.size(0) #累加350次   批次计算总量-350
        correct += torch.eq(pred,labels).sum().item() #累加正确量

        optimizer.zero_grad()  # 将梯度初始化为零  损失函数相对于模型参数的梯度
        loss = criterion(outputs, labels).to(device)  # 求loss,对应loss += (label[k] - h) * (label[k] - h) / 2
        loss.backward()  # 反向传播求梯度
        optimizer.step()  # 更新所有参数

        running_loss += loss.item()  #累计损失值  loss.item()会返回这个标量(形状为0的张量)的Python数值表示
        loss_list.append(loss.item())

        #总共训练epoch=25回，每回共i=350次，当49%50=49  ==  50-1时(即50的倍数次打印一次)
        if i % num_print == num_print - 1:    #共有350次，350/50一共记录7次
            print(f'[{epoch + 1} epoch, {i + 1} number] loss: {(running_loss / num_print)}' ) # 这(num_print)50次的平均损失
            print(f'[{epoch + 1} epoch, {i + 1} number] accuracy: {(correct / total)}' ) # 这(num_print)50次的平均精度
            #tag，value，x轴的值（epoch*350 + 50/100/150/200/----350）
            summaryWriter.add_scalar("training_loss",running_loss/100,epoch*len(train_loader)+i)
            summaryWriter.add_scalar("accuracy",correct/total,epoch*len(train_loader)+i)

            running_loss = 0.0 #重新记录下次损失，精度
            correct = 0  
            total = 0

    lr_1 = optimizer.param_groups[0]['lr']
    print('learn_rate : %.15f' % lr_1)
    scheduler.step(epoch)
end = time.time()
print('GoogleNet_time:{}min'.format((end-start)/60))

os.makedirs(os.path.dirname('Wang_data\model\model_Googlenet1D.pth'), exist_ok=True)
torch.save(model, 'Wang_data\model\model_Googlenet1D.pth')

test(test_loader)