"""
文件意图：实现 VGG 风格的重复 3x3 卷积块及其训练一步。
适用场景：构建 VGG、UNet 等网络的局部特征提取模块。
核心思想：多个同通道 3x3 卷积与 ReLU 保持空间尺寸，最后用 2x2 最大池化下采样。
输入输出：输入 NCHW 特征图，输出通道数为指定值且高宽减半的特征图。
时间复杂度：由卷积数和特征图大小决定。空间复杂度：O(参数量与激活)。
关键边界：卷积数和通道数必须为正；高宽必须至少为二以进行池化。
"""

import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class VGGBlock(torch.nn.Module):
    """显式堆叠 3x3 卷积、ReLU 和末尾最大池化的 VGG 模块。"""

    def __init__(self, convolution_count: int, input_channels: int, output_channels: int) -> None:
        """构建 VGG 卷积块。

        参数：convolution_count、input_channels、output_channels 必须为正。
        返回：无。
        边界情况：非法维度抛出 ValueError。
        关键算法点：第一层改变通道数，后续卷积保持 output_channels，padding=1 保持池化前空间尺寸。
        """
        super().__init__()
        if convolution_count <= 0 or input_channels <= 0 or output_channels <= 0:
            raise ValueError("卷积数量和通道数必须为正")
        layers: list[torch.nn.Module] = []
        current_channels = input_channels
        for _ in range(convolution_count):
            layers.append(torch.nn.Conv2d(current_channels, output_channels, kernel_size=3, padding=1))
            layers.append(torch.nn.ReLU())
            current_channels = output_channels
        self.convolutions = torch.nn.Sequential(*layers)
        self.pool = torch.nn.MaxPool2d(kernel_size=2, stride=2)

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        """提取并下采样输入特征图。

        参数：features 为形状 (batch,input_channels,height,width) 的浮点 tensor。
        返回：形状 (batch,output_channels,height//2,width//2) 的特征图。
        边界情况：非四维输入或高宽小于二会由模块/池化拒绝。
        关键算法点：卷积组先提取同尺度局部特征，池化才执行尺度缩减。
        """
        if features.ndim != 4:
            raise ValueError("VGGBlock 需要 NCHW 输入")
        return self.pool(self.convolutions(features))

    def training_step(self, features: torch.Tensor, target: torch.Tensor, learning_rate: float) -> float:
        """以 MSE 目标执行一次反向传播和手写 SGD 更新。

        参数：features 为输入，target 与 forward 输出同形，learning_rate 为正数。
        返回：更新前 MSE 损失。
        边界情况：目标形状或步长无效时抛出 ValueError。
        关键算法点：使用 autograd 计算局部卷积梯度，但参数更新逐项手写而不使用优化器。
        """
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")
        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()
        output = self.forward(features)
        if output.shape != target.shape:
            raise ValueError("target 形状必须与输出一致")
        loss = torch.mean((output - target) ** 2)
        loss.backward()
        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad
        return float(loss.detach())


if __name__ == "__main__":
    block = VGGBlock(2, 3, 8)
    inputs = torch.ones((1, 3, 8, 8))
    output = block(inputs)
    assert output.shape == (1, 8, 4, 4)
    before = block.convolutions[0].weight.detach().clone()
    assert block.training_step(inputs, torch.zeros_like(output), 0.01) >= 0.0
    assert not torch.equal(before, block.convolutions[0].weight.detach())
    print("008_vgg_block: all examples passed")
