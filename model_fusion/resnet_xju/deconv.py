import torch
import torch.nn as nn

# stride = 1    out = in + kernel - 1 
# stride > 1    out = stride * (in - 1) + kernel

# H_out = (H_in - 1) * stride[0] - 2 * padding[0] + kernel_size[0] + output_padding[0]
# W_out = (W_in - 1) * stride[1] - 2 * padding[1] + kernel_size[1] + output_padding[1]

class DeconvExample(nn.Module):
    def __init__(self):
        super(DeconvExample, self).__init__()
        self.deconv = nn.ConvTranspose2d(
            in_channels=1,    
            out_channels=32,   
            kernel_size=(11, 1),  
            stride=(6, 2),    
            padding=(0, 17),   
            output_padding=(5, 1) 
        )

    def forward(self, x):
        return self.deconv(x)

# 创建一个输入图像，形状为 (batch_size, channels, height, width)
input_tensor = torch.randn(1, 1, 17, 129)  # 输入特征图为 17x97
model = DeconvExample()

# 通过反卷积进行上采样
output_tensor = model(input_tensor)
print("输出尺寸: ", output_tensor.shape)
