import torch.nn as nn
import torch
 

color_channels = 1 
#进行分类的代码
class VGG(nn.Module):
    def __init__(self, features, num_classes, init_weights=False):
        super(VGG, self).__init__()
        # 定义 提取特征的网络结构
        self.features = features
        # 定义 最后 全连接的分类网络结构
        self.classifier = nn.Sequential(

            nn.Linear(7*7*512,1*1*4096),    #  经过特征提取后，进行展平后的输入为 7*7*512 -> 1*1*4096
            nn.ReLU(True),
            nn.Dropout(p=0.5),

            nn.Linear(1*1*4096,1*1*4096),
            nn.ReLU(True),
            nn.Dropout(p=0.5),

            nn.Linear(1*1*4096, num_classes)
        )
        # init_weights = True 则初始化网络
        if init_weights:
            self._initialize_weights()
 
    # 定义初始化 
    def _initialize_weights(self):
        # 初始化需要对每一个网络层的参数进行操作，所以利用继承nn.Module类中的一个方法:self.modules()遍历返回所有module
        for m in self.modules():
            # 如果是卷积层
            if isinstance(m, nn.Conv2d):
                # 按照 Xavier 均匀分布初始化参数。这种初始化方法试图根据层的输入和输出维度自动调整权重的尺度，使得每一层的激活值和梯度的方差在传播过程中保持一致，有助于缓解梯度消失或爆炸的问题。
                nn.init.xavier_uniform_(m.weight)
                # 如果有bias，则初始化为0
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            # 如果是全连接层
            elif isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0)
    # 定义传播-- 提取特征，展平，全连接
    def forward(self, x):
        # N x 3 x 224 x 224 将数据输入特征提取的网络
        x = self.features(x)
        # N x 512 x 7 x 7 
        x = torch.flatten(x, start_dim=1) # 0 为为batch_size，所以从第二位开始展平
        # N x 512*7*7 将数据输入分类层
        x = self.classifier(x)
        return x
  
#进行特征提取部分的代码
def make_features(cfg: list):
    layers = []
    in_channels = color_channels # color_channels
    for v in cfg:   # 遍历配置表
        if v == "M":    # 如果是M，则添加一个最大池化层
                        # 创建一个最大池化层，在VGG中所有的最大池化层的kernel_size=2，stride=2
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:       # 否则是卷积层
                    # 在Vgg中，所有的卷积层的kernel_size=3,padding=1，stride=1
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
                        # 将卷积层和ReLU放入列表
            layers += [conv2d, nn.ReLU(True)]
                        #网络列表每加一层，本层输入通道数都要改成上层的输出通道数
            in_channels = v
                    # 将列表通过非关键字参数的形式返回，*layers可以接收任意数量的参数
    return nn.Sequential(*layers)
 
#init函数里直接利用传入的参数定义了特提取网络，这里要定义如何创建,
# 之所以单独用一个函数定义，是因为vgg有多种配置，需要根据配置创建不同的网络结构，而配置则是用列表逐一描述了网络层的类型和通道数
# 定义cfgs字典文件，每一个key-value对代表一个模型的配置文件，在模型实例化时，我们根据选用的模型名称key，将对应的值-配置列表作为参数传到函数里
# 如：VGG11代表A配置，也就是一个11层的网络， 数字代表卷积层中卷积核的个数，'M'代表池化层
# 通过函数make_features(cfg: list)生成提取特征网络结构
cfgs = {
    'vgg11': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'vgg13': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'vgg16': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'vgg19': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
}
 
#vgg实例化和LeNet,AlexNet有点不同，因为要先手动选择网络名称，以VGG16为例，定义如下
# **kwargs表示可变长度的字典变量，在调用VGG函数时传入的字典变量
def vgg(model_name="vgg16", **kwargs):
        # 如果model_name不在cfgs，序会抛出AssertionError错误，报错为参数内容“ ”
    assert model_name in cfgs, "Warning: model number {} not in cfgs dict!".format(model_name)
    cfg = cfgs[model_name]

    # 这个字典变量包含了分类的个数以及是否初始化权重的布尔变量
    model = VGG(make_features(cfg), **kwargs)
    return model