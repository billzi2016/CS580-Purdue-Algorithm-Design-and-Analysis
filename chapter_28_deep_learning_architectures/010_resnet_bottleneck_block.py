"""
文件意图：实现 ResNet bottleneck 残差块的前向与训练一步。
适用场景：构建 ResNet-50/101/152 等深层残差网络。
核心思想：1x1 降维、3x3 空间卷积、1x1 扩展通道，再与投影捷径相加。
输入输出：输入 NCHW 特征图，输出 output_channels*expansion 通道特征图。
时间复杂度：由三层卷积主导。空间复杂度：O(参数与激活)。
关键边界：通道、stride、expansion 必须为正；形状不一致时使用投影捷径。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class ResNetBottleneckBlock(torch.nn.Module):
    """三层卷积的 bottleneck 残差块。"""

    def __init__(
        self,
        input_channels: int,
        bottleneck_channels: int,
        stride: int = 1,
        expansion: int = 4,
    ) -> None:
        """创建 bottleneck 残差分支与捷径。

        参数：input_channels、bottleneck_channels、stride、expansion 均为正。
        返回：无。
        边界情况：非法参数抛出 ValueError。
        关键算法点：最终输出通道为 bottleneck_channels*expansion，捷径必须投影到同一形状。
        """
        super().__init__()
        if (
            input_channels <= 0
            or bottleneck_channels <= 0
            or stride <= 0
            or expansion <= 0
        ):
            raise ValueError("bottleneck 参数必须为正")
        output_channels = bottleneck_channels * expansion
        self.conv1 = torch.nn.Conv2d(input_channels, bottleneck_channels, 1, bias=False)
        self.norm1 = torch.nn.BatchNorm2d(bottleneck_channels)
        self.conv2 = torch.nn.Conv2d(
            bottleneck_channels,
            bottleneck_channels,
            3,
            stride=stride,
            padding=1,
            bias=False,
        )
        self.norm2 = torch.nn.BatchNorm2d(bottleneck_channels)
        self.conv3 = torch.nn.Conv2d(
            bottleneck_channels, output_channels, 1, bias=False
        )
        self.norm3 = torch.nn.BatchNorm2d(output_channels)
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
        """返回 bottleneck 残差块输出。

        参数：features 是 NCHW tensor。
        返回：三个卷积层残差与捷径相加后的 ReLU 特征。
        边界情况：非四维输入抛出 ValueError。
        关键算法点：最后一层卷积后不先激活，保留残差相加的线性通路。
        """
        if features.ndim != 4:
            raise ValueError("ResNetBottleneckBlock 需要 NCHW 输入")
        hidden = self.relu(self.norm1(self.conv1(features)))
        hidden = self.relu(self.norm2(self.conv2(hidden)))
        residual = self.norm3(self.conv3(hidden))
        return self.relu(residual + self.shortcut(features))

    def training_step(
        self, features: torch.Tensor, target: torch.Tensor, learning_rate: float
    ) -> float:
        """以 MSE 执行一次反向传播和手写 SGD。

        参数：features 为输入，target 与输出同形，learning_rate 为正。
        返回：更新前 MSE。
        边界情况：无效目标形状或步长抛出 ValueError。
        关键算法点：所有卷积、归一化及投影捷径参数都通过同一个计算图获得梯度。
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
    block = ResNetBottleneckBlock(4, 3, stride=2)
    torch.manual_seed(3)
    inputs = torch.randn((2, 4, 8, 8))
    output = block(inputs)
    assert output.shape == (2, 12, 4, 4)
    before = block.conv1.weight.detach().clone()
    assert block.training_step(inputs, torch.zeros_like(output), 0.01) >= 0.0
    assert not torch.equal(before, block.conv1.weight.detach())
    print("010_resnet_bottleneck_block: all examples passed")
