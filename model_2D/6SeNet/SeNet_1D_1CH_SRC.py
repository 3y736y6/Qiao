import torch  
import torch.nn as nn  
import torch.nn.functional as F  
  
class SEBlock(nn.Module):  
    def __init__(self, channel, reduction=16):  
        super(SEBlock, self).__init__()  
        self.avg_pool = nn.AdaptiveAvgPool1d(1)  
        self.fc = nn.Sequential(  
            nn.Linear(channel, channel // reduction, bias=False),  
            nn.ReLU(inplace=True),  
            nn.Linear(channel // reduction, channel, bias=False),  
            nn.Sigmoid()  
        )  
  
    def forward(self, x):  
        b, c, _ = x.size()  
        y = self.avg_pool(x).view(b, c)  
        y = self.fc(y).view(b, c, 1)  
        return x * y.expand_as(x)  
  
class SENet1D(nn.Module):  
    def __init__(self, classes, in_channels, num_blocks=3, reduction=16):  
        super(SENet1D, self).__init__()  
          
        self.layer1 = self._make_layer(in_channels, 64, num_blocks, reduction)  
        self.layer2 = self._make_layer(64, 128, num_blocks, reduction)  
        self.layer3 = self._make_layer(128, 256, num_blocks, reduction)  
          
        self.fc = nn.Linear(6400 , classes)  # Adjust the dimension accordingly  
  
    def _make_layer(self, in_channels, out_channels, num_blocks, reduction):  
        layers = []  
        layers.append(nn.Conv1d(in_channels, out_channels, kernel_size=3, padding=1))  
        layers.append(nn.BatchNorm1d(out_channels))  
        layers.append(nn.ReLU(inplace=True))  
        layers.append(nn.MaxPool1d(2))  
  
        for _ in range(num_blocks):  
            layers.append(nn.Conv1d(out_channels, out_channels, kernel_size=3, padding=1))  
            layers.append(nn.BatchNorm1d(out_channels))  
            layers.append(nn.ReLU(inplace=True))  
            layers.append(SEBlock(out_channels, reduction))  
  
        return nn.Sequential(*layers)  
  
    def forward(self, x):  
        out = self.layer1(x)  
        out = self.layer2(out)  
        out = self.layer3(out)  
        out = F.avg_pool1d(out, 8)  
        out = out.view(out.size(0), -1)  # 展平除批处理维度外的所有维度  
        out = self.fc(out)  
        return out  
  
