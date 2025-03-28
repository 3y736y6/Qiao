from torchvision import models
import os

import time
import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.tensorboard import SummaryWriter
from datetime import datetime  
from torch.utils.data import DataLoader, TensorDataset,random_split
import numpy as np
from MyDataset2 import MyDataset2
from VGGx_src import vgg

# SRC 中 color channel = 1 根据输出修改
def main(my = True,train = True,test = True,color_channel = 1,init_weights=True):
    #########################   tensorboard --logdir=./runs   可视化查看指令
    current_datetime = datetime.now()  
    print("当前日期和时间:", current_datetime)
    formatted_datetime = current_datetime.strftime("%Y.%m.%d_%H.%M.%S") 

    # 如果有NVIDA显卡，转到GPU训练，否则用CPU
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("  1_using {} device.".format(device))
    # dataset = MyDataset2(data_file='STFT2D_data.pkl', label_file='STFT2D_labek.dat')
    dataset = MyDataset2(data_file='Wavelet2D_data_224Reshape.pkl', label_file='Wavelet2D_label.dat')
    
    # 划分比例
    train_test_rate = 0.8
    train_size = int(train_test_rate * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

    batch_size = 32
    train_loader = torch.utils.data.DataLoader(train_dataset,batch_size=batch_size, shuffle=True,)
    test_loader = torch.utils.data.DataLoader(test_dataset,batch_size=batch_size, shuffle=False,)
    # params
    epochs = 10
    loss_list = []
    start = time.time()
    correct = 0  
    total = 0
    num_print = len(train_dataset)//batch_size//3 # 每个epoch中，计算‘3’次准确率，损失率
    lr = 1e-4
    class_numbers = 6
    # 查看dataset数据
    idx=1
    sample1, label1 = dataset[idx]  
    print("--------------------------查看dataset 单条数据---------------------------")
    print(f"  sample1 shape:{sample1.shape,type(sample1)} , Label:{label1,type(label1)}")
    print(f"  total data:{len(dataset)},epochs:{epochs},batch_size:{batch_size}")
    print(f"  1 epoch has {len(dataset)//batch_size+1} steps")

    # 查看容器数据
    print("-------------------------查看train_loader 容器数据--------------------------")
    print("  total data", len(train_loader)*batch_size)
    print("  batch_size:", batch_size)
    print("  Number of batches:", len(train_loader))  
    print("  type of batches:",type(train_loader))   
    # 获取一个批次的数据  
    for batch_idx, (inputs, labels) in enumerate(train_loader):  
        if batch_idx == 0:  # 只查看第一个批次  
            print("input shape:", inputs.float().unsqueeze(1).repeat(1, color_channel, 1, 1).shape)
            print("input type:", inputs.float().unsqueeze(1).repeat(1, color_channel, 1, 1).type())  
            print("lable shape:", labels.long().shape)
            print("lable type:", inputs.long().type())  
            print()
            break


# 自定义模型
    model_name = "vgg16"
    net = vgg(model_name=model_name, num_classes=class_numbers, init_weights = init_weights )
    net.to(device)
    print('model_name:',model_name)


    loss_function = nn.CrossEntropyLoss()
    params = [p for p in net.parameters() if p.requires_grad]
    optimizer = optim.Adam(params, lr = lr)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=10)

    if train == True:
        #实例化一个SummaryWriter对象，用于存储训练过程数据
        summaryWriter = SummaryWriter(f"./runs/resnet/{formatted_datetime}")

        #绘制网络
        for i, (inputs, labels) in enumerate(train_loader):  
            if i == 1:  
                break  
            inputs, labels = inputs.float().unsqueeze(1).repeat(1, color_channel, 1, 1).to(device), labels.long().to(device)
            summaryWriter.add_graph(net,inputs)
            print(inputs.shape)

        print('++++++   start train  ++++++')
        print('+++++++  ----------  +++++++')
        # 训练
        net.train()
        for epoch in range(epochs):
            running_loss = 0.0
            for i, data in enumerate(train_loader):
                images, labels = data

                images = images.to(device)  
                images = images.float().unsqueeze(1).repeat(1, color_channel, 1, 1) # (batch_size,W,H)-->(batch_size,3,W,H)
                # images = images.float().unsqueeze(1) # (batch_size,W,H)-->(batch_size,1,W,H)
                labels = labels.to(device)
                labels = labels.long()-1

                logits = net(images)
                # print(images.type())
                # print(logits.type())
                # print(labels.type())


                pred = logits.argmax(dim=1)  
                total += images.size(0)  
                correct += torch.eq(pred,labels).sum().item() 
                loss = loss_function(logits, labels)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
                loss_list.append(loss.item())
                if i % num_print == num_print - 1:
                    print(f'[{epoch + 1} epoch, {i + 1} step]:')
                    print(f'accuracy: {(correct / total)} , loss: {(running_loss / num_print)} ' ) 
                    summaryWriter.add_scalar("training_loss",running_loss/100,epoch*len(train_loader)+i)
                    summaryWriter.add_scalar("accuracy",correct/total,epoch*len(train_loader)+i)
                    running_loss = 0.0 
                    correct = 0  
                    total = 0

            lr_1 = optimizer.param_groups[0]['lr']
            print('---------------- current_learn_rate ----------------- : %.15f' % lr_1)
            scheduler.step(epoch)

        end = time.time()
        print('total_time:{}min'.format((end-start)/60))

        os.makedirs(os.path.dirname('model\model_Resnet50.pth'), exist_ok=True)
        torch.save(net, 'model\model_Resnet50.pth')
        print('Finished Training')


    # test
    if test == True:
        print('++++++++  start test  +++++++')
        print('++++++++  ----------  +++++++')

        class_numbers = 6
        classes = ('normal','eccentric','broken_tooth','half_broken_tooth','surface_wearing','crack')

        net = torch.load('model\model_Resnet50.pth')  


        net.eval()
        correct = 0.0
        total = 0
        class_correct = list(0. for i in range(class_numbers))
        class_total = list(0. for i in range(class_numbers))

        with torch.no_grad():  # 测试集不需要反向传播
            for (images, labels) in test_loader:

                images = images.to(device)  
                images = images.float().unsqueeze(1).repeat(1, color_channel, 1, 1) # (batch_size,W,H)-->(batch_size,3,W,H)
                labels = labels.to(device)
                labels = labels.long()-1

                outputs = net(images)
                pred = outputs.argmax(dim=1)  # 返回每一行中最大值元素索引
                total += images.size(0)
                correct += torch.eq(pred,labels).sum().item()

                c = (pred == labels.to(device)).squeeze() # batch_size大小的tensor张量，每个元素为(True,False)
                
                for i in range(len(c)):

                    label = labels[i]
                    label = labels[i]
                    class_correct[label] += float(c[i])
                    class_total[label] += 1
        print('Accuracy of the network on the %d/%d tests: %.2f %%' % ( correct,total,100.0 * correct / total))
        print (class_total)
        print()

        for i in range(class_numbers):
            print('Accuracy of %5s : %.2f %%' % (classes[i],100 * class_correct[i] / class_total[i]))

if __name__ == '__main__':
    main(my = True,train=True,test=True,color_channel = 1,init_weights=True)