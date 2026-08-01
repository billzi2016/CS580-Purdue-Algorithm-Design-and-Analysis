"""
文件意图：实现 DenseNet dense block 的特征级联与训练一步。
适用场景：需要复用所有此前层特征、增强梯度流的密集连接卷积网络。
核心思想：每层接收当前累计特征并生成 growth_rate 个新通道，再沿通道维拼接。
输入输出：输入 NCHW 特征图，输出通道数为 input_channels+layer_count*growth_rate。
时间复杂度：随层数增长而增加，因为后层卷积输入包含全部此前特征。空间复杂度：O(累计特征图)。
关键边界：层数、增长率和输入通道必须为正。
"""

import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class DenseNetBlock(torch.nn.Module):
    """使用 batch norm、ReLU、3x3 卷积的 DenseNet 特征级联块。"""

    def __init__(self, layer_count: int, input_channels: int, growth_rate: int) -> None:
        """构建指定层数的 dense layers。

        参数：layer_count、input_channels、growth_rate 均为正。
        返回：无。
        边界情况：非法维度抛出 ValueError。
        关键算法点：第 i 层卷积输入通道是 input_channels+i*growth_rate。
        """
        super().__init__()
        if layer_count <= 0 or input_channels <= 0 or growth_rate <= 0:
            raise ValueError("DenseNet 参数必须为正")
        self.layers = torch.nn.ModuleList()
        for index in range(layer_count):
            channels = input_channels + index * growth_rate
            self.layers.append(torch.nn.Sequential(torch.nn.BatchNorm2d(channels), torch.nn.ReLU(), torch.nn.Conv2d(channels, growth_rate, 3, padding=1)))

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        """逐层拼接新旧特征并返回全部累计特征。

        参数：features 是 NCHW tensor。
        返回：通道维累计后的特征图。
        边界情况：非四维输入抛出 ValueError。
        关键算法点：每层使用 torch.cat 获得所有此前层输出，而非仅连接相邻层。
        """
        if features.ndim != 4:
            raise ValueError("DenseNetBlock 需要 NCHW 输入")
        current = features
        for layer in self.layers:
            current = torch.cat((current, layer(current)), dim=1)
        return current

    def training_step(self, features: torch.Tensor, target: torch.Tensor, learning_rate: float) -> float:
        """以 MSE 进行一次反向和手写 SGD 更新。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")
        for parameter in self.parameters():
            if parameter.grad is not None: parameter.grad.zero_()
        output = self.forward(features)
        if output.shape != target.shape: raise ValueError("target 形状不匹配")
        loss = torch.mean((output-target)**2); loss.backward()
        with torch.no_grad():
            for parameter in self.parameters(): parameter -= learning_rate*parameter.grad
        return float(loss.detach())


if __name__ == "__main__":
    block=DenseNetBlock(2,3,4); data=torch.randn((2,3,8,8)); output=block(data)
    assert output.shape==(2,11,8,8)
    before=block.layers[0][2].weight.detach().clone(); assert block.training_step(data,torch.zeros_like(output),0.01)>=0.0
    assert not torch.equal(before,block.layers[0][2].weight.detach())
    print("011_densenet_block: all examples passed")
