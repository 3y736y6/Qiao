import torch  
import torch.nn as nn  
  
class AlexNet1D(torch.nn.Module):  
    def __init__(self,in_channels=1,classes=7):  
        super(AlexNet1D, self).__init__()  
        self.features = nn.Sequential(  
            nn.Conv1d(in_channels, 64, kernel_size=11, stride=4, padding=5),  
            nn.ReLU(inplace=True),  
            nn.MaxPool1d(kernel_size=3, stride=2),  
            nn.Conv1d(64, 192, kernel_size=5, padding=2),  
            nn.ReLU(inplace=True),  
            nn.MaxPool1d(kernel_size=3, stride=2),  
            nn.Conv1d(192, 384, kernel_size=3, padding=1),  
            nn.ReLU(inplace=True),  
            nn.Conv1d(384, 256, kernel_size=3, padding=1),  
            nn.ReLU(inplace=True),  
            nn.Conv1d(256, 256, kernel_size=3, padding=1),  
            nn.ReLU(inplace=True),  
            nn.MaxPool1d(kernel_size=3, stride=2),  
        )  
        self.avgpool = nn.AdaptiveAvgPool1d(6)
        self.classifier = nn.Sequential(  
            nn.Dropout(),  
            nn.Linear(256 * 6, 4096),  
            nn.ReLU(inplace=True),  
            nn.Dropout(),  
            nn.Linear(4096, 4096),  
            nn.ReLU(inplace=True),  
            nn.Linear(4096, classes),  
        )  
  
    def forward(self, x):  
        x = self.features(x)  
        x = self.avgpool(x)  
        x = torch.flatten(x, 1)  
        x = self.classifier(x)  
        return x  
