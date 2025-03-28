import math  
import copy  
from functools import partial  
from collections import OrderedDict  
from typing import Optional, Callable  
import torch  
import torch.nn as nn  
from torch import Tensor  
from torch.nn import functional as F  
  
def _make_divisible(ch, divisor=8, min_ch=None):  
    """  
    This function ensures that all layers have a channel number that is divisible by 8.  
    """  
    if min_ch is None:  
        min_ch = divisor  
    new_ch = max(min_ch, int(ch + divisor / 2) // divisor * divisor)  
    # Make sure that round down does not go down by more than 10%.  
    if new_ch < 0.9 * ch:  
        new_ch += divisor  
    return new_ch  
  
class ConvBNActivation(nn.Sequential):  
    def __init__(self, in_planes: int, out_planes: int, kernel_size: int = 3, stride: int = 1, groups: int = 1,  
                 norm_layer: Optional[Callable[..., nn.Module]] = None, activation_layer: Optional[Callable[..., nn.Module]] = None):  
        padding = (kernel_size - 1) // 2  
        if norm_layer is None:  
            norm_layer = nn.BatchNorm2d  
        if activation_layer is None:  
            activation_layer = nn.SiLU  # alias Swish (torch>=1.7)  
        super(ConvBNActivation, self).__init__(  
            nn.Conv2d(in_channels=in_planes, out_channels=out_planes, kernel_size=kernel_size, stride=stride, padding=padding,  
                       groups=groups, bias=False),  
            norm_layer(out_planes),  
            activation_layer()  
        )  
  
class SqueezeExcitation(nn.Module):  
    def __init__(self, input_c: int, expand_c: int, squeeze_factor: int = 4):  
        super(SqueezeExcitation, self).__init__()  
        squeeze_c = input_c // squeeze_factor  
        self.fc1 = nn.Conv2d(expand_c, squeeze_c, 1)  
        self.ac1 = nn.SiLU()  # alias Swish  
        self.fc2 = nn.Conv2d(squeeze_c, expand_c, 1)  
        self.ac2 = nn.Sigmoid()  
  
    def forward(self, x: Tensor) -> Tensor:  
        scale = F.adaptive_avg_pool2d(x, output_size=(1, 1))  
        scale = self.fc1(scale)  
        scale = self.ac1(scale)  
        scale = self.fc2(scale)  
        scale = self.ac2(scale)  
        return scale * x  
  
class InvertedResidualConfig:  
    def __init__(self, kernel: int, input_c: int, out_c: int, exp_ratio: int, strides: int, use_se: bool, drop_connect_rate: float):  
        self.kernel = kernel  
        self.input_c = input_c  
        self.out_c = out_c  
        self.exp_ratio = exp_ratio  
        self.strides = strides  
        self.use_se = use_se  
        self.drop_connect_rate = drop_connect_rate  
  
    def adjust_channels(self, width_coefficient: float):  
        self.input_c = _make_divisible(self.input_c * width_coefficient)  
        self.out_c = _make_divisible(self.out_c * width_coefficient)  
        self.exp_ratio = (self.exp_ratio * width_coefficient)  
  
class MBConvBlock(nn.Module):  
    def __init__(self, exp_ratio: int, kernel: int, stride: int, in_channels: int, out_channels: int, use_se: bool, drop_connect_rate: float):  
        super(MBConvBlock, self).__init__()  
        self.use_shortcut = stride == 1 and in_channels == out_channels  
  
        # pointwise expand  
        self.expand_conv = ConvBNActivation(in_channels=in_channels, out_planes=in_channels * exp_ratio, kernel_size=1)  
  
        # depthwise conv  
        self.depthwise_conv = ConvBNActivation(in_channels=in_channels * exp_ratio, out_planes=in_channels * exp_ratio, kernel_size=kernel,  
                                               groups=in_channels * exp_ratio, stride=stride, padding=kernel // 2)  
  
        # squeeze and excitation  
        self.se_module = SqueezeExcitation(input_c=in_channels, expand_c=in_channels * exp_ratio) if use_se else nn.Identity()  
  
        # pointwise linear  
        self.project_conv = ConvBNActivation(in_channels=in_channels * exp_ratio, out_planes=out_channels, kernel_size=1, activation_layer=None)  
  
        self.drop_connect_rate = drop_connect_rate  
  
    def forward(self, x: Tensor) -> Tensor:  
        if self.training and self.drop_connect_rate > 0:  
            x = drop_path(x, self.drop_connect_rate, self.training)  
  
        # expansion phase  
        x = self.expand_conv(x)  
  
        # depthwise conv  
        x = self.depthwise_conv(x)  
  
        # squeeze and excitation  
        x = self.se_module(x)  
  
        # pointwise linear  
        x = self.project_conv(x)  
  
        # shortcut  
        if self.use_shortcut:  
            x = x + self.shortcut(x)  
  
        return x  
  
class EfficientNet(nn.Module):  
    def __init__(self, blocks_args=None, global_params=None):  
        super(EfficientNet, self).__init__()  
        self._blocks = nn.ModuleList([])  
        self._global_params = global_params  
  
        # Stem  
        in_channels = 3  # rgb  
        out_channels = _make_divisible(32, global_params.width_coefficient)  
        self._conv_stem = ConvBNActivation(in_channels=in_channels, out_planes=out_channels, kernel_size=3, stride=2)  
  
        # Build blocks  
        for block_args in blocks_args:  
            # Adjust number of channels in block args  
            block_args.adjust_channels(global_params.width_coefficient)  
  
            # Update block input and output channels based on depth multiplier.  
            block_args.input_c = block_args.input_c // global_params.depth_coefficient  
            block_args.out_c = block_args.out_c // global_params.depth_coefficient  
  
            # The first block needs to take care of stride and filter size increase.  
            self._blocks.append(MBConvBlock(  
                exp_ratio=block_args.exp_ratio,  
                kernel=block_args.kernel,  
                stride=block_args.strides,  
                in_channels=block_args.input_c,  
                out_channels=block_args.out_c,  
                use_se=block_args.use_se,  
                drop_connect_rate=global_params.drop_connect_rate  
            ))  
  
        # Head  
        in_channels = block_args.out_c  
        self._conv_head = ConvBNActivation(in_channels=in_channels, out_planes=1280, kernel_size=1)  
  
        # Final linear layer  
        self._avg_pooling = nn.AdaptiveAvgPool2d(1)  
        self._dropout = nn.Dropout(0.2)  
        self._fc = nn.Linear(1280, global_params.num_classes)  
  
    def extract_features(self, inputs: Tensor) -> Tensor:  
        # Stem  
        x = self._swish(self._bn0(self._conv_stem(inputs)))  
  
        # Blocks  
        for idx, block in enumerate(self._blocks):  
            drop_connect_rate = self._global_params.drop_connect_rate  
            if drop_connect_rate:  
                drop_connect_rate *= float(idx) / len(self._blocks)  
            x = block(x, drop_connect_rate=drop_connect_rate)  
  
        # Head  
        x = self._swish(self._bn1