"""
文件意图：实现 ResNet BasicBlock 的残差前向与训练一步。
适用场景：构建 ResNet-18/34 风格网络，缓解深层网络训练中的恒等映射学习困难。
核心思想：两层 3x3 卷积形成残差分支，与恒等或 1x1 投影捷径相加后再 ReLU。
输入输出：输入 NCHW 特征图，输出指定通道和步长后的特征图。
时间复杂度：由两层卷积主导。空间复杂度：O(参数量与激活)。
关键边界：输入通道、输出通道和步长必须为正；形状变化时自动建立投影捷径。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class ResNetBasicBlock(torch.nn.Module):
    """两层卷积的 ResNet 残差基本块。"""

    def __init__(
        self, input_channels: int, output_channels: int, stride: int = 1
    ) -> None:
        """创建残差分支与匹配形状的捷径分支。

        参数：通道数为正，stride 为正整数。
        返回：无。
        边界情况：非法参数抛出 ValueError。
        关键算法点：通道或空间尺寸改变时，1x1 投影把捷径变换到可相加形状。
        """
        super().__init__()
        if input_channels <= 0 or output_channels <= 0 or stride <= 0:
            raise ValueError("通道数和 stride 必须为正")
        self.conv1 = torch.nn.Conv2d(
            input_channels, output_channels, 3, stride=stride, padding=1, bias=False
        )
        self.norm1 = torch.nn.BatchNorm2d(output_channels)
        self.conv2 = torch.nn.Conv2d(
            output_channels, output_channels, 3, padding=1, bias=False
        )
        self.norm2 = torch.nn.BatchNorm2d(output_channels)
        self.shortcut = (
            torch.nn.Identity()
            if input_channels == output_channels and stride == 1
            else torch.nn.Sequential(
                torch.nn.Conv2d(
                    input_channels, output_channels, 1, stride=stride, bias=False
                ),
                torch.nn.BatchNorm2d(output_channels),
            )
        )
        self.relu = torch.nn.ReLU()

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        """计算残差块输出。

        参数：features 是四维 NCHW tensor。
        返回：残差分支与捷径相加再 ReLU 的特征图。
        边界情况：非 NCHW 输入抛出 ValueError。
        关键算法点：加法要求两路径形状一致，shortcut 负责在需要时完成投影。
        """
        if features.ndim != 4:
            raise ValueError("ResNetBasicBlock 需要 NCHW 输入")
        residual = self.norm2(self.conv2(self.relu(self.norm1(self.conv1(features)))))
        return self.relu(residual + self.shortcut(features))

    def training_step(
        self, features: torch.Tensor, target: torch.Tensor, learning_rate: float
    ) -> float:
        """以 MSE 执行一次反向传播和手写 SGD 更新。

        参数：target 形状需匹配 forward 输出，learning_rate 为正。
        返回：更新前 MSE。
        边界情况：目标形状或步长无效时抛出 ValueError。
        关键算法点：残差与捷径参数均从同一损失反向获得梯度。
        """
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")
        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()
        output = self.forward(features)
        if output.shape != target.shape:
            raise ValueError("target 形状不匹配")
        loss = torch.mean((output - target) ** 2)
        loss.backward()
        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad
        return float(loss.detach())


if __name__ == "__main__":
    block = ResNetBasicBlock(3, 6, stride=2)
    inputs = torch.ones((2, 3, 8, 8))
    output = block(inputs)
    assert output.shape == (2, 6, 4, 4)
    before = block.conv1.weight.detach().clone()
    assert block.training_step(inputs, torch.zeros_like(output), 0.01) >= 0.0
    assert not torch.equal(before, block.conv1.weight.detach())
    print("009_resnet_basic_block: all examples passed")
