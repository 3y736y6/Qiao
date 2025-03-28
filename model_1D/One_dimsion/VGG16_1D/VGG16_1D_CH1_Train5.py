import torch
from torch import optim
import numpy as np
import time
from MyDataset import MyDataset
import VGG16_1D_CH1_SRC2
from torch import nn
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime  
from VGG16_1D_CH1_Test5 import test
current_datetime = datetime.now()  
print("当前日期和时间:", current_datetime)
formatted_datetime = current_datetime.strftime("%Y.%m.%d_%H.%M.%S") 
summaryWriter = SummaryWriter(f"./runs/vgg/{formatted_datetime}")#根据日期实例化 数据记录文件

# 配置参数
batch_size = 32  # 每次喂入的数据量
learningrate = 0.001  # 学习率
step_size = 5  # 每n个epoch更新一次学习率
epoch_num = 25  # 总迭代次数
num_print = 50  #每n次batch打印一次


# 训练数据加载
dataset = MyDataset('0.4A_500n_Data_1D_R1_Train.dat','0.4A_500n_Data_1D_R1_Train_Lable.dat')

torch.manual_seed(19)
train_test_rate = 0.7
train_size = int(train_test_rate * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

train_loader = torch.utils.data.DataLoader(train_dataset,batch_size=batch_size, shuffle=True,)
test_loader = torch.utils.data.DataLoader(test_dataset,batch_size=batch_size, shuffle=False)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = VGG16_1D_CH1_SRC2.VGG16_1D_CH1_SRC4(nums=6).to(device=device)

criterion = nn.CrossEntropyLoss()
# adam优化器
# optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=0.001)
optimizer = optim.Adam(model.parameters(), lr=learningrate, weight_decay=1e-3)    
# 动态调整学习率
# scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=0.25)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=step_size)


##绘制网络
for i, (inputs, labels) in enumerate(train_loader):  
    if i == 1:  # i  0--249
        break  
    inputs, labels = inputs.to(device), labels.to(device)
    size_tmp = inputs.shape
    inputs.resize_(size_tmp[0], 1, size_tmp[1])
    summaryWriter.add_graph(model,inputs)
    print(inputs.shape)


# 训练
loss_list = []
start = time.time()
correct = 0  
total = 0
for epoch in range(epoch_num):
    running_loss = 0.0
    for i, (inputs, labels) in enumerate(train_loader, 0):
        inputs, labels = inputs.to(device), labels.to(device)

        size_tmp = inputs.shape
        inputs.resize_(size_tmp[0], 1, size_tmp[1])
        labels = labels.long()-1

        optimizer.zero_grad()  # 将梯度初始化为零
        outputs = model(inputs)  # 前向传播求出预测的值

        pred = outputs.argmax(dim=1)  # 返回每一行中最大值元素索引
        total += inputs.size(0) #累加350次   批次计算总量-350
        correct += torch.eq(pred,labels).sum().item() #累加正确量


        loss = criterion(outputs, labels).to(device)  # 求loss,对应loss += (label[k] - h) * (label[k] - h) / 2
        loss.backward()  # 反向传播求梯度
        optimizer.step()  # 更新所有参数

        running_loss += loss.item()
        loss_list.append(loss.item())


        if i % num_print == num_print - 1:
            #print('[%d epoch, %d] loss: %.6f' % (epoch + 1, i + 1, running_loss / num_print))
            print(f'[{epoch + 1} epoch, {i + 1} number] loss: {(running_loss / num_print)}' ) # 这(num_print)50次的平均损失
            print(f'[{epoch + 1} epoch, {i + 1} number] accuracy: {(correct / total)}' ) # 这(num_print)50次的平均精度

            summaryWriter.add_scalar("training_loss",running_loss/1000,epoch*len(train_loader)+i)
            summaryWriter.add_scalar("accuracy",correct/total,epoch*len(train_loader)+i)

            running_loss = 0.0
            correct = 0  
            total = 0

    lr_1 = optimizer.param_groups[0]['lr']
    print('learn_rate : %.15f' % lr_1)
    scheduler.step(epoch)
end = time.time()
print('VGG16_time:{}'.format(end-start))

torch.save(model, 'model/model_Vgg16_1D_.pth')   #保存模型

test(test_loader)
