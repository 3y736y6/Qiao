import torch
import torch.nn as nn
import torch.nn.functional as F
import time
import numpy as np
import torch.optim as optim
import torch.nn as nn
import torch
import ResNet50_1D_CH1_SRC1
from torch import nn, optim
from MyDataset import MyDataset
import os
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime  

# 定义 1D 卷积块
class Conv1dBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0):
        super(Conv1dBlock, self).__init__()
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size, stride=stride, padding=padding)
        self.bn = nn.BatchNorm1d(out_channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x

# 定义残差块 (Residual Block)
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = Conv1dBlock(in_channels, out_channels, kernel_size=3, stride=stride, padding=1)
        self.conv2 = Conv1dBlock(out_channels, out_channels, kernel_size=3, stride=1, padding=1)

        # 进行维度匹配
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv1d(in_channels, out_channels, kernel_size=1, stride=stride),
                nn.BatchNorm1d(out_channels)
            )

    def forward(self, x):
        out = self.conv1(x)
        out = self.conv2(out)
          
        return out + self.shortcut(x)
    

# 定义 ResNet-18 1D 模型
class ResNet18_1D(nn.Module):
    def __init__(self, num_classes=6):
        super(ResNet18_1D, self).__init__()
        
        self.conv1 = Conv1dBlock(1, 64, kernel_size=7, stride=2, padding=3)  # 第一层卷积
        self.pool = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)  # 池化层
        
        # 第一层残差块组
        self.layer1 = self._make_layer(64, 64, 2, stride=1)
        # 第二层残差块组
        self.layer2 = self._make_layer(64, 128, 2, stride=2)
        # 第三层残差块组
        self.layer3 = self._make_layer(128, 256, 2, stride=2)
        # 第四层残差块组
        self.layer4 = self._make_layer(256, 512, 2, stride=2)

        self.fc = nn.Linear(512, num_classes)  # 全连接层

    def _make_layer(self, in_channels, out_channels, num_blocks, stride):
        layers = []
        layers.append(ResidualBlock(in_channels, out_channels, stride))
        for _ in range(1, num_blocks):
            layers.append(ResidualBlock(out_channels, out_channels, stride=1))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)  # 第一层卷积
        x = self.pool(x)  # 池化层
        x = self.layer1(x)  # 第一层残差块
        x = self.layer2(x)  # 第二层残差块
        x = self.layer3(x)  # 第三层残差块
        x = self.layer4(x)  # 第四层残差块
        x = F.adaptive_avg_pool1d(x, 1)  # 全局平均池化
        x = torch.flatten(x, 1)  # 展平
        x = self.fc(x)  # 全连接层
        return x

# 测试模型
if __name__ == "__main__":
    # 假设输入的形状为 [batch_size, 1, 1024]，代表一维信号数据


    current_datetime = datetime.now()  
    print("当前日期和时间:", current_datetime)
    formatted_datetime = current_datetime.strftime("%Y.%m.%d_%H.%M.%S") 
    summaryWriter = SummaryWriter(f"./runs/resnet/{formatted_datetime}+Resnet1D")


    batch_size = 32  # 每次喂入的数据量
    step_size = 5  # 每n个epoch更新一次学习率
    epoch_num = 20  # 总迭代次数
    num_print = 50  #每n次batch打印一次
    class_num = 5
    learning_rate = 0.001

    # dataset = MyDataset('0.4A_500n_Data_1D_R1_Train.dat','0.4A_500n_Data_1D_R1_Train_Lable.dat')
    dataset = MyDataset('bj_30hz_1channel_1D_data.csv','lable_5.csv')

    torch.manual_seed(19)
    train_test_rate = 0.7
    train_size = int(train_test_rate * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

    train_loader = torch.utils.data.DataLoader(train_dataset,batch_size=batch_size, shuffle=True,)
    test_loader = torch.utils.data.DataLoader(test_dataset,batch_size=batch_size, shuffle=False)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model = ResNet18_1D(num_classes=class_num).to(device=device)


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
    print('ResNet_time:{}min'.format((end-start)/60))
        

    torch.save(model, 'model\model_Resnet18_1D.pth')
    os.makedirs(os.path.dirname('model\model_Resnet18_1D.pth'), exist_ok=True)



    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model = torch.load('model\model_Resnet18_1D.pth')  
    model.eval()# evaluation mode

    correct = 0.0
    total = 0
    class_numbers = 5
    classes = ('normal','eccentric','broken_tooth','half_broken_tooth','surface_wearing')
    class_correct = list(0. for i in range(class_numbers))
    class_total = list(0. for i in range(class_numbers))

    with torch.no_grad():  # 测试的时候不需要对梯度进行调整，所以梯度设置不调整
        for (inputs, labels) in test_loader:        
            inputs, labels = inputs.to(device), labels.to(device) # 将输入和目标在每一步都送入GPU

            size_tmp = inputs.shape
            inputs.resize_(size_tmp[0], 1, size_tmp[1])
            labels = labels.long()-1
            
            outputs = model(inputs)
            pred = outputs.argmax(dim=1)  # 返回每一行中最大值元素索引
            total += inputs.size(0)
            correct += torch.eq(pred,labels).sum().item()
        
            c = (pred == labels.to(device)).squeeze()
            for i in range(len(c)):

                label = labels[i]
                class_correct[label] += float(c[i])
                class_total[label] += 1
    print('Accuracy of the network on the %d/%d tests: %.2f %%' % ( correct,total,100.0 * correct / total))
    print (class_total)
    print()

    for i in range(class_numbers):
        print('Accuracy of %5s : %.2f %%' % (classes[i],100 * class_correct[i] / class_total[i]))
