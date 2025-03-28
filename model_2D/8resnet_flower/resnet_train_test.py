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

def main(train = True,test = False):
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
    batch_size = 64

    train_loader = torch.utils.data.DataLoader(train_dataset,
                                                batch_size=batch_size, shuffle=True,)
    # 加载测试数据集
    test_dataset = datasets.ImageFolder(root=os.path.join(image_path, "val"),
                                            transform=data_transform["val"])
    # 测试集长度
    test_num = len(test_dataset)
    test_loader = torch.utils.data.DataLoader(test_dataset,
                                                    batch_size=batch_size, shuffle=False,)

    print("3_using {} images for training, {} images for test.".format(train_num,test_num))
    
    # train param
   
    epochs = 25
    # 用于判断最佳模型
    # best_acc = 0.0
    # 最佳模型保存地址
    # save_path = './resNet34.pth'
    # train_steps = len(train_loader)

    loss_list = []
    start = time.time()
    correct = 0  
    total = 0
    num_print = train_num//batch_size//3 # 每个epoch中，计算‘3’次准确率，损失率

    # 查看数据
    # idx=1
    # sample1, label1 = train_dataset[idx]  
    # print(f"sample1 shape:{sample1.shape,type(sample1)} , Label shape:{label1,type(label1)}")
    # print(f"total data:{len(train_dataset)},epochs:{epochs},batch_size:{batch_size}")
    # print(f"every epoch has {train_num//batch_size} steps")

    # 模型实例化
    net = resnet50(num_classes = 5)
    net.to(device)

    # 加载预训练模型权重
    # model_weight_path = "./resnet34-pre.pth"
    # exists()：判断括号里的文件是否存在，可以是文件路径
    # assert os.path.exists(model_weight_path), "file {} does not exist.".format(model_weight_path)
    # net.load_state_dict(torch.load(model_weight_path, map_location='cpu'))
    # 输入通道数
    # in_channel = net.fc.in_features
    # 全连接层
    # net.fc = nn.Linear(in_channel, 5)

    # 定义损失函数（交叉熵损失）
    loss_function = nn.CrossEntropyLoss()

    # 抽取模型参数，只抽取需要更新的参数
    params = [p for p in net.parameters() if p.requires_grad]
    # 定义adam优化器
    # params(iterable)：要训练的参数，一般传入的是model.parameters()
    # lr(float)：learning_rate学习率，也就是步长，默认：1e-3
    optimizer = optim.Adam(params, lr=0.001)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=10)

    if train == True:
        #绘制网络
        for i, (inputs, labels) in enumerate(train_loader):  
            if i == 1:  
                break  
            inputs, labels = inputs.to(device), labels.to(device)
            summaryWriter.add_graph(net,inputs)
            print('input size:',inputs.shape)

        print("start train")
        # 训练
        net.train()
        for epoch in range(epochs):
            
            running_loss = 0.0
            # tqdm：进度条显示
            # train_bar = tqdm(train_loader, file=sys.stdout)
            # train_bar: 传入数据（数据包括：训练数据和标签）
            # enumerate()：将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在for循环当中
            # enumerate返回值有两个：一个是序号，一个是数据（包含训练数据和标签）
            # x：训练数据（inputs）(tensor类型的），y：标签（labels）(tensor类型）
            for i, data in enumerate(train_loader):
                images, labels = data
                images = images.to(device)  # torch.Size([16, 3, 224, 224])
                labels = labels.to(device)  # torch.Size([16])


                # 前向传播计算预测值
                logits = net(images)    # torch.Size([16, 5]) # 批次，类别概率
                # print(images.type())# torch.cuda.FloatTensor
                # print(logits.type())# torch.cuda.FloatTensor
                # print(labels.type())# torch.cuda.LongTensor

                pred = logits.argmax(dim=1)  # 返回每一行中最大值元素索引
                # torch.Size([16])
                # tensor([2, 3, 3, 3, 2, 1, 3, 2, 2, 3, 2, 2, 3, 2, 2, 4], device='cuda:0')

                total += images.size(0)  #   批次计算总量16

                correct += torch.eq(pred,labels).sum().item() #累加正确量 (16批数据中正确的个数)

                # 计算损失
                loss = loss_function(logits, labels) #logits:预测值(16*5)，labels:真实值(16*1) 

                # 清空过往梯度
                optimizer.zero_grad()
                # 反向传播，计算当前梯度
                loss.backward()
                # 跟新参数
                optimizer.step()

                # item()：得到元素张量的数值
                running_loss += loss.item()
                loss_list.append(loss.item())

                # 进度条的前缀
                # .3f：表示浮点数的精度为3（小数位保留3位）
                # train_bar.desc = "train epoch[{}/{}] loss:{:.3f}".format(epoch + 1, epochs,loss)

                if i % num_print == num_print - 1:    # 总训练数据/batch_size = 单次迭代数 
                    print(f'[{epoch + 1} epoch, {i + 1} step] loss: {(running_loss / num_print)}   accuracy: {(correct / total)}' )

                    # tag，value，x轴的值
                    summaryWriter.add_scalar("training_loss",running_loss/100,epoch*len(train_loader)+i)
                    summaryWriter.add_scalar("accuracy",correct/total,epoch*len(train_loader)+i)

                    running_loss = 0.0 #重新记录下次损失，精度
                    correct = 0  
                    total = 0

            # print学习率
            lr_1 = optimizer.param_groups[0]['lr']
            print('current_learn_rate : %.15f' % lr_1)
            scheduler.step(epoch)

        # print总时间
        end = time.time()
        print('total_time:{}min'.format((end-start)/60))

    #     # 测试
    #     # eval()：如果模型中有Batch Normalization和Dropout，则不启用，以防改变权值
    #     # net.eval()
    #     acc = 0.0
    #     # 清空历史梯度，与训练最大的区别是测试过程中取消了反向传播
    #     with torch.no_grad():
    #         val_bar = tqdm(validate_loader, file=sys.stdout)
    #         for val_data in val_bar:
    #             val_images, val_labels = val_data
    #             outputs = net(val_images.to(device))
    #             # torch.max(input, dim)函数
    #             # input是具体的tensor，dim是max函数索引的维度，0是每列的最大值，1是每行的最大值输出
    #             # 函数会返回两个tensor，第一个tensor是每行的最大值；第二个tensor是每行最大值的索引
    #             predict_y = torch.max(outputs, dim=1)[1]
    #             # 对两个张量Tensor进行逐元素的比较，若相同位置的两个元素相同，则返回True；若不同，返回False
    #             # .sum()对输入的tensor数据的某一维度求和
    #             acc += torch.eq(predict_y, val_labels.to(device)).sum().item()

    #             val_bar.desc = "valid epoch[{}/{}]".format(epoch + 1,
    #                                                        epochs)

    #     val_accurate = acc / val_num
    #     print('[epoch %d] train_loss: %.3f  val_accuracy: %.3f' %
    #           (epoch + 1, running_loss / train_steps, val_accurate))

    #     # 保存最好的模型权重
    #     if val_accurate > best_acc:
    #         best_acc = val_accurate
    #         # torch.save(state, dir)保存模型等相关参数，dir表示保存文件的路径+保存文件名
    #         # model.state_dict()：返回的是一个OrderedDict，存储了网络结构的名字和对应的参数
    #         torch.save(net.state_dict(), save_path)

    # print('Finished Training')
    os.makedirs(os.path.dirname('model\model_flower_Resnet50.pth'), exist_ok=True)
    torch.save(net, 'model\model_flower_Resnet50.pth')

    # test
    if test == True:
        print('++++++++  start test  +++++++')
        print('++++++++  ----------  +++++++')

        class_numbers = 5
        classes = ('A','B','C','D','E')

        net = torch.load('model\model_flower_Resnet50.pth')  


        net.eval()
        correct = 0.0
        total = 0
        class_correct = list(0. for i in range(class_numbers))
        class_total = list(0. for i in range(class_numbers))

        with torch.no_grad():  # 测试集不需要反向传播
            for (images, labels) in test_loader:

                images = images.to(device)  # torch.Size([16, 3, 224, 224])
                labels = labels.to(device)  # torch.Size([16])

                outputs = net(images)
                pred = outputs.argmax(dim=1)  # 返回每一行中最大值元素索引
                total += images.size(0)
                correct += torch.eq(pred,labels).sum().item()

                c = (pred == labels.to(device)).squeeze() # batch_size大小的tensor张量，每个元素为(True,False)
                
                for i in range(len(c)):
                    label = labels[i]
                    class_correct[label] += float(c[i])
                    class_total[label] += 1
        print('Accuracy of the network on the %d/%d tests: %.2f %%' % ( correct,total,100.0 * correct / total))
        print (class_total)
        print()

        for i in range(class_numbers):
            print('Accuracy of %5s : %.2f %%' % (classes[i],100 * class_correct[i] / class_total[i]))

if __name__ == '__main__':
    main(train=True,test=True)