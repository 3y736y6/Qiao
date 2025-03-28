import torch
import torch.nn as nn



class convExample(nn.Module):
    def __init__(self):
        super(convExample, self).__init__()
        self.Yconv = nn.Conv2d(
            in_channels=1, 
            out_channels=1,
            kernel_size=(5,11) ,
            stride=(1,6),
            padding=(0,2),
            dilation=(4,20)
            )

    def forward(self, x):
        return self.Yconv(x)

# 创建一个输入图像，形状为 (batch_size, channels, height, width)
input_tensor = torch.randn(1, 1, 128, 1536)  # 输入特征图为 17x97
model = convExample()

# 通过反卷积进行上采样
output_tensor = model(input_tensor)
print("输出尺寸: ", output_tensor.shape)
