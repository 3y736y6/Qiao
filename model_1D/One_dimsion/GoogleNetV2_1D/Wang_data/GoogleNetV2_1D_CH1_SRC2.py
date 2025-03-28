'''GoogLeNet with PyTorch.'''
import torch
import torch.nn as nn #各种层 损失函数 优化器 等函数或类
import torch.nn.functional as F #激活函数 卷积操作 池化操作

# BasicConv1d（一维基础卷积模块，包含卷积、批量归一化和ReLU激活函数）
# Inception（Inception模块，它并行地使用不同大小的卷积核和池化操作来提取特征，并将这些特征拼接起来）
# GoogLeNet_1D（整个网络模型，将多个Inception模块堆叠起来）

# 编写卷积+bn+relu模块
class BasicConv1d(nn.Module): #继承基类nn.Module
    def __init__(self, in_channels, out_channals, **kwargs):
        super(BasicConv1d, self).__init__()  #调用基类构造函数
        self.conv = nn.Conv1d(in_channels, out_channals, **kwargs)
        # 创建了一个一维卷积层，输入通道数为in_channels，
        # 输出通道数为out_channals，其他参数（如kernel_size, stride, padding等）由**kwargs提供。
        # **kwargs是一个可变数量的关键字参数
        self.bn = nn.BatchNorm1d(out_channals)
        # 批量归一化BN,把每一层的输出再做一次归一化

    def forward(self, x):
        #定义了数据通过网络的方式
        x = self.conv(x)
        # 数据x先通过一维卷积层
        x = self.bn(x)
        # 接着数据通过批量归一化层
        return F.relu(x)
        # 数据通过一个ReLU激活函数

# 编写Inception模块
class Inception(nn.Module):
    def __init__(self, in_planes,
                 n1x1, n3x3red, n3x3, n5x5red, n5x5, pool_planes):
        # in_planes    输入通道数    
        # n1x1         1x1卷积层的输出通道数
        # n3x3red      在进行3x3卷积之前，用于缩减通道数的1x1卷积层的输出通道数
        # pool_planes  池化层后的输出通道数
        super(Inception, self).__init__()
        # 1x1 conv branch
        self.b1 = BasicConv1d(in_planes, n1x1, kernel_size=1)

        # 1x1 conv -> 3x3 conv branch
        self.b2_1x1_a = BasicConv1d(in_planes, n3x3red, 
                                    kernel_size=1)
        self.b2_3x3_b = BasicConv1d(n3x3red, n3x3, 
                                    kernel_size=3, padding=1)

        # 1x1 conv -> 3x3 conv -> 3x3 conv branch
        self.b3_1x1_a = BasicConv1d(in_planes, n5x5red, 
                                    kernel_size=1)
        self.b3_3x3_b = BasicConv1d(n5x5red, n5x5, 
                                    kernel_size=3, padding=1)
        self.b3_3x3_c = BasicConv1d(n5x5, n5x5, 
                                    kernel_size=3, padding=1)

        # 3x3 pool -> 1x1 conv branch
        self.b4_pool = nn.MaxPool1d(3, stride=1, padding=1) #stride步长
        self.b4_1x1 = BasicConv1d(in_planes, pool_planes, 
                                  kernel_size=1)

    def forward(self, x):
        y1 = self.b1(x)
        y2 = self.b2_3x3_b(self.b2_1x1_a(x))
        y3 = self.b3_3x3_c(self.b3_3x3_b(self.b3_1x1_a(x)))
        y4 = self.b4_1x1(self.b4_pool(x))
        # y的维度为[batch_size, out_channels, C_out,L_out]
        # 合并不同卷积下的特征图
        return torch.cat([y1, y2, y3, y4], 1)


class GoogLeNet_1D(nn.Module):
    def __init__(self):
        super(GoogLeNet_1D, self).__init__()
        self.pre_layers = BasicConv1d(1, 192, kernel_size=3, padding=1)

        self.a3 = Inception(192,  64,  96, 128, 16, 32, 32)
        self.b3 = Inception(256, 128, 128, 192, 32, 96, 64)

        self.maxpool = nn.MaxPool1d(3, stride=2, padding=1)

        self.a4 = Inception(480, 192,  96, 208, 16,  48,  64)
        self.b4 = Inception(512, 160, 112, 224, 24,  64,  64)
        self.c4 = Inception(512, 128, 128, 256, 24,  64,  64)
        self.d4 = Inception(512, 112, 144, 288, 32,  64,  64)
        self.e4 = Inception(528, 256, 160, 320, 32, 128, 128)

        self.a5 = Inception(832, 256, 160, 320, 32, 128, 128)
        self.b5 = Inception(832, 384, 192, 384, 48, 128, 128)

        self.avgpool = nn.AvgPool1d(8, stride=1)
        # #一维平均池化
        # #线性全连接层 进入414720个特征，输出7个结果
        self.linear = nn.Linear(414720, 7)

    def forward(self, x):
        out = self.pre_layers(x)
        out = self.a3(out)
        out = self.b3(out)
        out = self.maxpool(out)
        out = self.a4(out)
        out = self.b4(out)
        out = self.c4(out)
        out = self.d4(out)
        out = self.e4(out)
        out = self.maxpool(out)
        out = self.a5(out)
        out = self.b5(out)
        out = self.avgpool(out)
        out = out.view(out.size(0), -1) # 将张量重新塑造成二维[20,x,x]=[20,x*x]
        out = self.linear(out)

        return out

# def test():
#     net = GoogLeNet_1D()
#     x = torch.randn(2,1,2048)
#     y = net(x)
#     print(y.size())

# test()

# def test1():
#     net=BasicConv1d(1, 32,  kernel_size=3, padding=1)
#     x = torch.randn(2,1,2048)
#     print(x.shape)
#     y = net(x)
#     print(y.size())

# test1()