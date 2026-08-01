"""
文件意图：实现深度可分离卷积的前向与训练一步。
适用场景：MobileNet 等轻量 CNN，使用按通道空间卷积加 1x1 通道混合降低计算量。
核心思想：depthwise 卷积设置 groups=input_channels，仅提取每通道空间特征；pointwise 卷积混合通道。
输入输出：输入 NCHW 特征图，输出指定通道特征图。
时间复杂度：深度卷积 O(C*K^2) 加逐点卷积 O(C*O)，低于标准 O(C*O*K^2)。
空间复杂度：O(参数量与激活)。
关键边界：通道和 stride 必须为正；输入必须为四维 tensor。
"""

import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class DepthwiseSeparableConvolution(torch.nn.Module):
    """由 depthwise 与 pointwise 两阶段组成的卷积层。"""
    def __init__(self,input_channels:int,output_channels:int,kernel_size:int=3,stride:int=1)->None:
        """创建深度和逐点卷积。

        参数：通道、kernel_size、stride 必须为正。返回：无。
        边界情况：非法参数抛出 ValueError。
        关键算法点：groups=input_channels 保证每个输入通道使用独立空间核。
        """
        super().__init__()
        if input_channels<=0 or output_channels<=0 or kernel_size<=0 or stride<=0:raise ValueError("卷积参数必须为正")
        padding=kernel_size//2
        self.depthwise=torch.nn.Conv2d(input_channels,input_channels,kernel_size,stride=stride,padding=padding,groups=input_channels,bias=False)
        self.pointwise=torch.nn.Conv2d(input_channels,output_channels,1,bias=False)
    def forward(self,features:torch.Tensor)->torch.Tensor:
        """依次执行按通道空间卷积和逐点通道混合。

        参数：features 为 NCHW tensor。返回：输出特征图。
        边界情况：非四维输入抛出 ValueError。
        关键算法点：pointwise 仅用 1x1 核，负责跨通道信息交互。
        """
        if features.ndim!=4:raise ValueError("需要 NCHW 输入")
        return self.pointwise(self.depthwise(features))
    def training_step(self,features:torch.Tensor,target:torch.Tensor,learning_rate:float)->float:
        """以 MSE 执行一次反向与手写 SGD 更新。"""
        if learning_rate<=0:raise ValueError("learning_rate 必须为正")
        for parameter in self.parameters():
            if parameter.grad is not None:parameter.grad.zero_()
        output=self.forward(features)
        if output.shape!=target.shape:raise ValueError("target 形状不匹配")
        loss=torch.mean((output-target)**2);loss.backward()
        with torch.no_grad():
            for parameter in self.parameters():parameter-=learning_rate*parameter.grad
        return float(loss.detach())

if __name__=="__main__":
    layer=DepthwiseSeparableConvolution(3,5);data=torch.randn((2,3,8,8));output=layer(data)
    assert output.shape==(2,5,8,8) and layer.depthwise.groups==3
    before=layer.pointwise.weight.detach().clone();assert layer.training_step(data,torch.zeros_like(output),0.01)>=0.0
    assert not torch.equal(before,layer.pointwise.weight.detach())
    print("013_depthwise_separable_convolution: all examples passed")
