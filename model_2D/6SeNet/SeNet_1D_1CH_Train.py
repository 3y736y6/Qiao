import time
import numpy as np
import torch.optim as optim
import torch.nn as nn
import torch
import SeNet_1D_1CH_SRC
from torch import nn, optim
from MyDataset import MyDataset

from torch.utils.tensorboard import SummaryWriter
from datetime import datetime  


current_datetime = datetime.now()  
print("当前日期和时间:", current_datetime)
formatted_datetime = current_datetime.strftime("%Y.%m.%d_%H.%M.%S") 
summaryWriter = SummaryWriter(f"./runs/senet/{formatted_datetime}")


batch_size = 20  # 每次喂入的数据量
step_size = 5  # 每n个epoch更新一次学习率
epoch_num = 25  # 总迭代次数
num_print = 50  #每n次batch打印一次
class_num = 7
learning_rate = 0.001

train_data = MyDataset('./Data/xc_src01_train2.dat','./Data/xc_src01_trainlabel2.dat')
train_loader = torch.utils.data.DataLoader(train_data,batch_size=batch_size,shuffle=True)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = SeNet_1D_1CH_SRC.SENet1D(in_channels=1, classes=class_num).to(device=device)

criterion = nn.CrossEntropyLoss().cuda()

optimizer = optim.Adam(model.parameters(), lr=learning_rate)

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=step_size)

# 绘制
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
print("{0:-^27}".format('Train_Model'))
for epoch in range(epoch_num):
    running_loss = 0.0
    model.train()   # training mode
    
    for i, (inputs, labels) in enumerate(train_loader, 0): 
        inputs, labels = inputs.to(device), labels.to(device)
        size_tmp = inputs.shape
        inputs.resize_(size_tmp[0], 1, size_tmp[1])
        labels = labels.long()-1
        
        outputs = model(inputs)
        # accuracy
        pred = outputs.argmax(dim=1)
        total += inputs.size(0)
        correct += torch.eq(pred,labels).sum().item()  

        optimizer.zero_grad() 
        loss = criterion(outputs, labels).to(device)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        loss_list.append(loss.item())

        #总共训练epoch=25回，每回共i=350次，当49%50=49  ==  50-1时(即50的倍数次打印一次)
        if i % num_print == num_print - 1:    #共有350次，350/50一共记录7次
            print(f'[{epoch + 1} epoch, {i + 1} number] loss: {(running_loss / num_print)}' ) # 这(num_print)50次的平均损失
            print(f'[{epoch + 1} epoch, {i + 1} number] accuracy: {(correct / total)}' ) # 这(num_print)50次的平均精度

            #tag，value，x轴的值（epoch*350 + 50/100/150/200/----350）
            summaryWriter.add_scalar("training_loss",running_loss/1000,epoch*len(train_loader)+i)
            summaryWriter.add_scalar("accuracy",correct/total,epoch*len(train_loader)+i)

            running_loss = 0.0 #重新记录下次损失，精度
            correct = 0  
            total = 0
    lr_1 = optimizer.param_groups[0]['lr']
    print('learn_rate : %.15f' % lr_1)
    scheduler.step(epoch)
end = time.time()   
print('SeNet_time:{}min'.format((end-start)/60))
    
torch.save(model, '6SeNet\model\model_SeNet.pth')
