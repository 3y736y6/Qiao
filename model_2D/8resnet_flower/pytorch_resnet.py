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
from resnet_src import resnet34,resnet50,resnet101
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime  

def main():
    #tensorboard --logdir=./runs可视化查看指令
    #根据日期实例化 数据记录文件
    current_datetime = datetime.now()  
    print("当前日期和时间:", current_datetime)
    formatted_datetime = current_datetime.strftime("%Y.%m.%d_%H.%M.%S") 
    summaryWriter = SummaryWriter(f"./runs/resnet/{formatted_datetime}")

    # 如果有NVIDA显卡，转到GPU训练，否则用CPU
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("1_using {} device.".format(device))

    data_transform = {
        # 训练
        # Compose()：将多个transforms的操作整合在一起
        "train": transforms.Compose([
            # RandomResizedCrop(224)：将给定图像随机裁剪为不同的大小和宽高比，然后缩放所裁剪得到的图像为给定大小
            transforms.RandomResizedCrop((224,224)),
            # RandomVerticalFlip()：以0.5的概率竖直翻转给定的PIL图像
            transforms.RandomHorizontalFlip(),
            # ToTensor()：数据转化为Tensor格式
            transforms.ToTensor(),
            # Normalize()：将图像的像素值归一化到[-1,1]之间，使模型更容易收敛
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]),
        # 验证
        "val": transforms.Compose([transforms.Resize(256),
                                    transforms.CenterCrop(224),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])}
    # abspath()：获取文件当前目录的绝对路径
    # join()：用于拼接文件路径，可以传入多个路径
    # getcwd()：该函数不需要传递参数，获得当前所运行脚本的路径
    data_root = os.path.abspath(os.getcwd())
    # 得到数据集的路径
    image_path = os.path.join(data_root, "flower_data")
    # exists()：判断括号里的文件是否存在，可以是文件路径,如果image_path不存在，序会抛出AssertionError错误，报错为参数内容“ ”
    assert os.path.exists(image_path), "{} path does not exist.".format(image_path)

    train_dataset = datasets.ImageFolder(root=os.path.join(image_path, "train"),
                                            transform=data_transform["train"])

    # print('------------')
    # print(train_dataset[0][0][0][0]) #(总数, (颜色通道，每个颜色通道有一个二维矩阵),标签)
    # 训练集长度
    train_num = len(train_dataset)

    # {'daisy':0, 'dandelion':1, 'roses':2, 'sunflower':3, 'tulips':4}
    # class_to_idx：获取分类名称对应索引
    flower_list = train_dataset.class_to_idx
    # dict()：创建一个新的字典
    # 循环遍历数组索引并交换val和key的值重新赋值给数组，这样模型预测的直接就是value类别值
    cla_dict = dict((val, key) for key, val in flower_list.items())
    # 把字典编码成json格式
    json_str = json.dumps(cla_dict, indent=4)
    # 把字典类别索引写入json文件
    with open('class_indices.json', 'w') as json_file:
        json_file.write(json_str)

    # 一次训练载入16张图像
    batch_size = 128
    train_loader = torch.utils.data.DataLoader(train_dataset,batch_size=batch_size, shuffle=True,)
    # 加载测试数据集
    validate_dataset = datasets.ImageFolder(root=os.path.join(image_path, "val"),transform=data_transform["val"])
    # 测试集长度
    val_num = len(validate_dataset)
    validate_loader = torch.utils.data.DataLoader(validate_dataset,batch_size=batch_size, shuffle=False,)

    print("3_using {} images for training, {} images for validation.".format(train_num,val_num))
    
    # params
    epochs = 150
    loss_list = []
    start = time.time()
    correct = 0  
    total = 0
    num_print = train_num//batch_size//3 # 每个epoch中，计算‘3’次准确率，损失率

    # 查看数据
    idx=1
    sample1, label1 = train_dataset[idx]  
    print(f"sample1 shape:{sample1.shape,type(sample1)} , Label shape:{label1,type(label1)}")
    print(f"total data:{len(train_dataset)},epochs:{epochs},batch_size:{batch_size}")
    print(f"every epoch has {train_num//batch_size} steps")

    # 模型实例化
    

    net = models.resnet50()
    net.fc = nn.Linear(2048, 5)

    # net = resnet50(num_classes = 5)
    net.to(device = device)

    loss_function = nn.CrossEntropyLoss()
    params = [p for p in net.parameters() if p.requires_grad]
    optimizer = optim.Adam(params, lr=0.001)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=10)


    #绘制网络
    for i, (inputs, labels) in enumerate(train_loader):  
        if i == 1:  
            break  
        inputs, labels = inputs.to(device), labels.to(device)
        summaryWriter.add_graph(net,inputs)
        print(inputs.shape) # 批次，通道，二维，矩阵



    print("start train")
    # 训练
    net.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(train_loader, 0):       #i 0--349
            images, labels = inputs.to(device), labels.to(device)
            logits = net(images)

            pred = logits.argmax(dim=1)  
            total += images.size(0)  
            correct += torch.eq(pred,labels).sum().item() 
            loss = loss_function(logits, labels).to(device)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            loss_list.append(loss.item())
            if i % num_print == num_print - 1:
                print(f'[{epoch + 1} epoch, {i + 1} step] loss: {(running_loss / num_print)}' )
                print(f'[{epoch + 1} epoch, {i + 1} strp] accuracy: {(correct / total)}' ) 
                summaryWriter.add_scalar("training_loss",running_loss/100,epoch*len(train_loader)+i)
                summaryWriter.add_scalar("accuracy",correct/total,epoch*len(train_loader)+i)
                running_loss = 0.0 
                correct = 0  
                total = 0

        lr_1 = optimizer.param_groups[0]['lr']
        print('current_learn_rate : %.15f' % lr_1)
        scheduler.step(epoch)

    end = time.time()
    print('total_time:{}min'.format((end-start)/60))

    os.makedirs(os.path.dirname('model\model_Resnet50.pth'), exist_ok=True)
    torch.save(net, 'model\model_Resnet50.pth')




if __name__ == '__main__':
    main()