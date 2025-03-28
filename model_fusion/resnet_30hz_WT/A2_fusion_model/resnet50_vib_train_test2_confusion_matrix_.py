import pickle
from torchvision import models
import os
import sys
import json
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets
from tqdm import tqdm
from resnet_src2 import resnet34,resnet50,resnet101,resnet18
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime  
from torch.utils.data import DataLoader, TensorDataset,random_split
import numpy as np
from MyDataset2 import MyDataset2
# 使用自构建的resnet模型进行训练，测试。 
# self = True 使用自构建的resnet50模型，False 使用pytorch的resnet50模型
# train = True 训练，False 不训练
# test = True 测试，False 不测试

import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

def plot_confusion_matrix(cm, classes, title='Confusion Matrix', cmap=plt.cm.Blues):
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap=cmap, xticklabels=classes, yticklabels=classes)
    plt.title(title,fontdict={'fontsize': 24,'fontname': 'Times New Roman'})
    plt.xlabel('Predicted',fontdict={'fontsize': 20,'fontname': 'Times New Roman'})
    plt.ylabel('True',fontdict={'fontsize': 20,'fontname': 'Times New Roman'})
    plt.show()

# 可以修改src中第一个输入，来拟合输入数据的 ‘颜色通道数’  彩色=(3，w,h)  参数量三倍关系 灰度=(1，w,h)  
def main(my = True,train = True,test = True,color_channel = 1):
    #########################   tensorboard --logdir=A2_fusion_model/runs/resnet   可视化查看指令
    current_datetime = datetime.now()  
    print("当前日期和时间:", current_datetime)
    formatted_datetime = current_datetime.strftime("%Y.%m.%d_%H.%M.%S") 

    # 如果有NVIDA显卡，转到GPU训练，否则用CPU
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("  1_using {} device.".format(device))

    # dataset2 = MyDataset2(data_file='bj_wavelet_reshape128x1536.pkl', label_file='lable_5.csv') # stft和小波数据集

    # # dataset = MyDataset2(data_file='bj_wavelet_reshape128x128.pkl', label_file='lable_5.csv') # stft和小波数据集
    # dataset1 = MyDataset2(data_file='bj_STFT2D_data.pkl', label_file='lable_5.csv')

    dataset2 = MyDataset2(data_file='bj_wavelet_2channel_reshape128x1536.pkl', label_file='lable_5.csv') # stft和小波数据集
    dataset1 = MyDataset2(data_file='bj_STFT2D_data.pkl', label_file='lable_5.csv')
    
    class_numbers = 5
    classes = ('normal','broken','missing_tooth','root_crack','wear')


    # 生成相同的随机索引
    def get_random_split_indices(dataset, train_test_rate=0.8):
                # 设置随机种子
        seed = 40
        torch.manual_seed(seed)
        np.random.seed(seed)

        indices = torch.randperm(len(dataset)).tolist()  # 随机排列索引
        train_size = int(train_test_rate * len(dataset))
        return indices[:train_size], indices[train_size:]

    # 划分 dataset1
    train_indices1, test_indices1 = get_random_split_indices(dataset1)
    train_dataset1 = torch.utils.data.Subset(dataset1, train_indices1)
    test_dataset1 = torch.utils.data.Subset(dataset1, test_indices1)

    # 划分 dataset2
    train_indices2, test_indices2 = get_random_split_indices(dataset2)
    train_dataset2 = torch.utils.data.Subset(dataset2, train_indices2)
    test_dataset2 = torch.utils.data.Subset(dataset2, test_indices2)

    # 创建 DataLoader
    batch_size = 32
    train_loader1 = torch.utils.data.DataLoader(train_dataset1, batch_size=batch_size, shuffle=False)
    test_loader1 = torch.utils.data.DataLoader(test_dataset1, batch_size=batch_size, shuffle=False)
    train_loader2 = torch.utils.data.DataLoader(train_dataset2, batch_size=batch_size, shuffle=False)
    test_loader2 = torch.utils.data.DataLoader(test_dataset2, batch_size=batch_size, shuffle=False)


    # params
    epochs = 4
    loss_list = []
    start = time.time()
    correct = 0  
    total = 0
    num_print = len(train_dataset1)//batch_size//3 # 每个epoch中，计算‘3’次准确率，损失率
    lr = 1e-4

    # 查看dataset1数据
    idx=1
    sample1, label1 = dataset1[idx]  
    print("查看dataset 单条数据")
    print(f"  sample1 shape:{sample1.shape,type(sample1)} , Label:{label1,type(label1)}")
    print(f"  total data:{len(dataset1)},epochs:{epochs},batch_size:{batch_size}")
    print(f"  1 epoch has {len(dataset1)//batch_size+1} steps")
    # 查看容器数据
    print("查看train_loader 容器数据")
    print("  total data", len(train_loader1)*batch_size)
    print("  batch_size:", batch_size)
    print("  Number of batches:", len(train_loader1))  
    print("  type of batches:",type(train_loader1))   
    # 获取一个批次的数据  
    for batch_idx, (inputs, labels) in enumerate(train_loader1):  
        if batch_idx == 0:  # 只查看第一个批次  
            print("input shape:", inputs.float().unsqueeze(1).repeat(1, color_channel, 1, 1).shape)
            print("input type:", inputs.float().unsqueeze(1).repeat(1, color_channel, 1, 1).type())  
            print("lable shape:", labels.long().shape)
            print("lable type:", inputs.long().type())  
            print()
            # print(labels)
            break
    # 查看dataset2数据
    idx=1
    sample2, label2 = dataset2[idx]  
    print("查看dataset 单条数据")
    print(f"  sample1 shape:{sample2.shape,type(sample2)} , Label:{label2,type(label2)}")
    print(f"  total data:{len(dataset2)},epochs:{epochs},batch_size:{batch_size}")
    print(f"  1 epoch has {len(dataset2)//batch_size+1} steps")
    # 查看容器数据
    print("查看train_loader 容器数据")
    print("  total data", len(train_loader2)*batch_size)
    print("  batch_size:", batch_size)
    print("  Number of batches:", len(train_loader2))  
    print("  type of batches:",type(train_loader2))   
    # 获取一个批次的数据  
    for batch_idx, (inputs, labels) in enumerate(train_loader2):  
        if batch_idx == 0:  # 只查看第一个批次  
            print("input shape:", inputs.float().unsqueeze(1).repeat(1, color_channel, 1, 1).shape)
            print("input type:", inputs.float().unsqueeze(1).repeat(1, color_channel, 1, 1).type())  
            print("lable shape:", labels.long().shape)
            print("lable type:", inputs.long().type())  
            # print(labels)
            break

    # 模型-----------------------------------------
    # net = models.resnet18()
    # net.fc = nn.Linear(512, 5)
 
    net = models.resnet50()
    net.fc = nn.Linear(2048, 5)

    if my == True: # 将net改为自定义模型
    # 自定义模型
        net = resnet18(num_classes = 5)
        print('自定义模型')
        color_channel = 1

    net.to(device)

    loss_function = nn.CrossEntropyLoss()
    params = [p for p in net.parameters() if p.requires_grad]
    optimizer = optim.Adam(params, lr = lr)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=10)

    if train == True:
        #实例化一个SummaryWriter对象，用于存储训练过程数据
        summaryWriter = SummaryWriter(f"A2_fusion_model/runs/resnet/{formatted_datetime}")

        #绘制网络
        for i, ((data1, target1), (data2, target2)) in enumerate(zip(test_loader1, test_loader2)):
            if i == 1:  
                break  
            inputs1, _ = data1,target1
            inputs1 = inputs1.to(device)  
            inputs1 = inputs1.float().unsqueeze(1).repeat(1, color_channel, 1, 1) # (batch_size,W,H)-->(batch_size,3,W,H)

            inputs2, _ = data2,target2
            inputs2 = inputs2.to(device)  
            inputs2 = inputs2.float().unsqueeze(1).repeat(1, color_channel, 1, 1) # (batch_size,W,H)-->(batch_size,3,W,H)

            summaryWriter.add_graph(net,(inputs1,inputs2))
            print(inputs1.shape,inputs2.shape)



        print('++++++   start train  ++++++')
        print('+++++++  ----------  +++++++')
        # 训练
        net.train()
        for epoch in range(epochs):
            running_loss = 0.0
            # 使用 zip 和 enumerate 同时遍历两个 train_loader，并获取索引
            for i, ((data1, target1), (data2, target2)) in enumerate(zip(train_loader1, train_loader2)):

                images1, labels = data1,target1
                images1 = images1.to(device)  
                images1 = images1.float().unsqueeze(1).repeat(1, color_channel, 1, 1) # (batch_size,W,H)-->(batch_size,3,W,H)
                # images = images.float().unsqueeze(1) # (batch_size,W,H)-->(batch_size,1,W,H)

                # ------------------------
                images2, labels2 = data2,target2
                images2 = images2.to(device)  
                images2 = images2.float().unsqueeze(1).repeat(1, color_channel, 1, 1) # (batch_size,W,H)-->(batch_size,3,W,H)
                # images = images.float().unsqueeze(1) # (batch_size,W,H)-->(batch_size,1,W,H)
                labels = labels.to(device)
                labels = labels.long()-1

                logits = net(images1,images2)
                # print(images.type())
                # print(logits.type())
                # print(labels.type())


                pred = logits.argmax(dim=1)  
                total += images1.size(0)  
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
                    summaryWriter.add_scalar("training_loss",running_loss/100,epoch*len(train_loader1)+i)
                    summaryWriter.add_scalar("accuracy",correct/total,epoch*len(train_loader1)+i)
                    running_loss = 0.0 
                    correct = 0  
                    total = 0

            lr_1 = optimizer.param_groups[0]['lr']
            print('---------------- current_learn_rate ----------------- : %.15f' % lr_1)
            scheduler.step(epoch)

        end = time.time()
        print('total_time:{}min'.format((end-start)/60))

        os.makedirs(os.path.dirname('A2_fusion_model\model\model_Resnet18.pth'), exist_ok=True)
        torch.save(net, 'A2_fusion_model\model\model_Resnet18.pth')
        print('Finished Training')


    # test
    if test == True:
        print('++++++++  start test  +++++++')
        print('++++++++  ----------  +++++++')


        net = torch.load('A2_fusion_model\model\model_Resnet18.pth')  
        net.eval()
        correct = 0.0
        total = 0

        all_preds = []# confusion matrix
        all_labels = []

        class_correct = list(0. for i in range(class_numbers))
        class_total = list(0. for i in range(class_numbers))

        with torch.no_grad():  # 测试集不需要反向传播
            for i, ((data1, target1), (data2, target2)) in enumerate(zip(test_loader1, test_loader2)):

                images1, labels = data1,target1
                images1 = images1.to(device)  
                images1 = images1.float().unsqueeze(1).repeat(1, color_channel, 1, 1) # (batch_size,W,H)-->(batch_size,3,W,H)
                # images = images.float().unsqueeze(1) # (batch_size,W,H)-->(batch_size,1,W,H)

                # ------------------------
                images2, labels2 = data2,target2
                images2 = images2.to(device)  
                images2 = images2.float().unsqueeze(1).repeat(1, color_channel, 1, 1) # (batch_size,W,H)-->(batch_size,3,W,H)
                # images = images.float().unsqueeze(1) # (batch_size,W,H)-->(batch_size,1,W,H)
                labels = labels.to(device)
                labels = labels.long()-1

                logits = net(images1,images2)

                pred = logits.argmax(dim=1)  # 返回每一行中最大值元素索引
                total += images1.size(0)
                correct += torch.eq(pred,labels).sum().item()
                
                all_preds.extend(pred.cpu().numpy())# confusion matrix
                all_labels.extend(labels.cpu().numpy())

                c = (pred == labels.to(device)).squeeze() # batch_size大小的tensor张量，每个元素为(True,False)
                
                for i in range(len(c)):

                    label = labels[i]
                    class_correct[label] += float(c[i])
                    class_total[label] += 1

            print('Accuracy of the network on the %d/%d tests: %.2f %%' % ( correct,total,100.0 * correct / total))
            print (class_total)
            print()

            class_X=['H' , 'G', 'W' , 'C' , 'M'] # 图片显示不下
            num_classes1 = len(class_X)
            cm = confusion_matrix(all_labels, all_preds, labels=range(num_classes1))
            plot_confusion_matrix(cm, class_X)

            for i in range(class_numbers):
                print('Accuracy of %5s : %.2f %%' % (classes[i],100 * class_correct[i] / class_total[i]))

if __name__ == '__main__':
    main(my = True,train=False,test=True)