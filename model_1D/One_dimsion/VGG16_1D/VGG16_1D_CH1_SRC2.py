import torch
import torch.nn as nn

class VGG16_1D_CH1_SRC1(nn.Module):
    def __init__(self, nums):
        super(VGG16_1D_CH1_SRC1, self).__init__()
        self.nums = nums
        vgg = []

        # 第一个卷积部分
        # 112, 112, 64
        vgg.append(nn.Conv1d(in_channels=1, out_channels=64, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(64))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(64))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=2, stride=2))

        # 第二个卷积部分
        # 56, 56, 128
        vgg.append(nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(128))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(128))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 第三个卷积部分
        # 28, 28, 256
        vgg.append(nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(256))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(256))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(256))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 第四个卷积部分
        # 14, 14, 512
        vgg.append(nn.Conv1d(in_channels=256, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 第五个卷积部分
        # 7, 7, 512
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 将每一个模块按照他们的顺序送入到nn.Sequential中,输入要么事orderdict,要么事一系列的模型，遇到上述的list，必须用*号进行转化
        self.main = nn.Sequential(*vgg)

        # 全连接层
        classfication = []
        # in_features四维张量变成二维[batch_size,channels,width,height]变成[batch_size,channels*width*height]
        classfication.append(nn.Linear(in_features=512 * 3 , out_features=512))  # 输出4096个神经元，参数变成512*7*7*4096+bias(4096)个
        classfication.append(nn.ReLU())
        classfication.append(nn.Dropout(p=0.5))
        classfication.append(nn.Linear(in_features=512, out_features=512))
        classfication.append(nn.ReLU())
        classfication.append(nn.Dropout(p=0.5))
        classfication.append(nn.Linear(in_features=512, out_features=self.nums))

        self.classfication = nn.Sequential(*classfication)

    def forward(self, x):
        feature = self.main(x)  # 输入张量x
        feature = feature.view(x.size(0), -1)  # reshape x变成[batch_size,channels*width*height]
        result = self.classfication(feature)
        return result

class VGG16_1D_CH1_SRC2(nn.Module):
    def __init__(self, nums):
        super(VGG16_1D_CH1_SRC2, self).__init__()
        self.nums = nums
        self.model_name = 'CWRUcnn'

        self.conv = nn.Sequential(
            nn.Conv1d(1, 32, 16, padding=0),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(4),
            nn.Conv1d(32, 32, 16, padding=0),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(),
            nn.Conv1d(32, 32, 16, padding=0),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(4),
            nn.Conv1d(32, 64, 16, padding=0),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(),
            nn.Conv1d(64, 64, 16, padding=0),
            nn.BatchNorm1d(64),
            nn.ReLU()
        )

        self.fc = nn.Sequential(
            nn.Linear(4096, 64),
            nn.ReLU(),
            nn.Linear(64, self.nums),
        )

        

    def forward(self, x):
        feature = self.conv(x)  # 输入张量x
        feature = feature.view(x.size(0), -1)  # reshape x变成[batch_size,channels*width*height]
        result = self.fc(feature)
        return result



class VGG16_1D_CH1_SRC3(nn.Module):
    def __init__(self, nums):
        super(VGG16_1D_CH1_SRC3, self).__init__()
        self.nums = nums
        vgg = []

        # 第一个卷积部分
        # 112, 112, 64
        vgg.append(nn.Conv1d(in_channels=1, out_channels=64, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(64))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(64))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=2, stride=2))

        # 第二个卷积部分
        # 56, 56, 128
        vgg.append(nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(128))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(128))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 第三个卷积部分
        # 28, 28, 256
        vgg.append(nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(256))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(256))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(256))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 第四个卷积部分
        # 14, 14, 512
        vgg.append(nn.Conv1d(in_channels=256, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 第五个卷积部分
        # 7, 7, 512
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 将每一个模块按照他们的顺序送入到nn.Sequential中,输入要么事orderdict,要么事一系列的模型，遇到上述的list，必须用*号进行转化
        self.main = nn.Sequential(*vgg)

        # 全连接层
        classfication = []
        # in_features四维张量变成二维[batch_size,channels,width,height]变成[batch_size,channels*width*height]
        classfication.append(nn.Linear(in_features=512 * 4 , out_features=512))  # 输出4096个神经元，参数变成512*7*7*4096+bias(4096)个
        classfication.append(nn.ReLU())
        classfication.append(nn.Dropout(p=0.5))
        classfication.append(nn.Linear(in_features=512, out_features=512))
        classfication.append(nn.ReLU())
        classfication.append(nn.Dropout(p=0.5))
        classfication.append(nn.Linear(in_features=512, out_features=self.nums))

        self.classfication = nn.Sequential(*classfication)

    def forward(self, x):
        feature = self.main(x)  # 输入张量x
        feature = feature.view(x.size(0), -1)  # reshape x变成[batch_size,channels*width*height]
        result = self.classfication(feature)
        return result

class VGG16_1D_CH1_SRC4(nn.Module):
    def __init__(self, nums):
        super(VGG16_1D_CH1_SRC4, self).__init__()
        self.nums = nums
        vgg = []

        # 第一个卷积部分
        # 112, 112, 64
        vgg.append(nn.Conv1d(in_channels=1, out_channels=64, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(64))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(64))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=2, stride=2))

        # 第二个卷积部分
        # 56, 56, 128
        vgg.append(nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(128))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(128))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 第三个卷积部分
        # 28, 28, 256
        vgg.append(nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(256))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(256))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(256))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 第四个卷积部分
        # 14, 14, 512
        vgg.append(nn.Conv1d(in_channels=256, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 第五个卷积部分
        # 7, 7, 512
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.Conv1d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        vgg.append(nn.BatchNorm1d(512))
        vgg.append(nn.ReLU())
        vgg.append(nn.MaxPool1d(kernel_size=4, stride=4))

        # 将每一个模块按照他们的顺序送入到nn.Sequential中,输入要么事orderdict,要么事一系列的模型，遇到上述的list，必须用*号进行转化
        self.main = nn.Sequential(*vgg)

        # 全连接层
        classfication = []
        # in_features四维张量变成二维[batch_size,channels,width,height]变成[batch_size,channels*width*height]
        classfication.append(nn.Linear(in_features=512 * 3 , out_features=512))  # 输出4096个神经元，参数变成512*7*7*4096+bias(4096)个
        classfication.append(nn.ReLU())
        classfication.append(nn.Dropout(p=0.5))
        classfication.append(nn.Linear(in_features=512, out_features=512))
        classfication.append(nn.ReLU())
        classfication.append(nn.Dropout(p=0.5))
        classfication.append(nn.Linear(in_features=512, out_features=self.nums))

        self.classfication = nn.Sequential(*classfication)

    def forward(self, x):
        feature = self.main(x)  # 输入张量x
        feature = feature.view(x.size(0), -1)  # reshape x变成[batch_size,channels*width*height]
        result = self.classfication(feature)
        return result


# x = torch.rand(size=(8, 1, 2048))
# vgg16 = VGG16_1D_CH1_SRC3(nums=3)
# out = vgg16(x)
# print(out.shape)
# print(vgg16)
