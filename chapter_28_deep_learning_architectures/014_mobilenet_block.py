"""
文件意图：实现 MobileNet v1 风格 depthwise-separable 卷积块。
适用场景：移动端轻量 CNN，结合深度可分离卷积、批归一化和 ReLU6。
核心思想：先逐通道进行空间卷积，再用 1x1 卷积混合通道，每阶段用 BatchNorm 和 ReLU6 稳定训练。
输入输出：输入 NCHW 特征图，返回指定通道与步长后的特征。
时间复杂度：由深度卷积和 1x1 卷积组成，显著低于同尺寸标准卷积。空间复杂度：O(参数与激活)。
关键边界：通道、kernel 和 stride 必须为正。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class MobileNetBlock(torch.nn.Module):
    """MobileNet v1 的深度可分离卷积、BN、ReLU6 模块。"""

    def __init__(
        self, input_channels: int, output_channels: int, stride: int = 1
    ) -> None:
        """创建深度与逐点两个卷积阶段。

        参数：input_channels、output_channels、stride 均为正。返回：无。
        边界情况：非法参数抛出 ValueError。
        关键算法点：depthwise 的 groups 等于输入通道，pointwise 执行跨通道投影。
        """
        super().__init__()
        if input_channels <= 0 or output_channels <= 0 or stride <= 0:
            raise ValueError("MobileNet 参数必须为正")
        self.depthwise = torch.nn.Conv2d(
            input_channels,
            input_channels,
            3,
            stride=stride,
            padding=1,
            groups=input_channels,
            bias=False,
        )
        self.depth_norm = torch.nn.BatchNorm2d(input_channels)
        self.pointwise = torch.nn.Conv2d(input_channels, output_channels, 1, bias=False)
        self.point_norm = torch.nn.BatchNorm2d(output_channels)
        self.relu6 = torch.nn.ReLU6()

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        """计算 depthwise-BN-ReLU6 后接 pointwise-BN-ReLU6 的输出。

        参数：features 为 NCHW tensor。返回：输出特征图。
        边界情况：非四维输入抛出 ValueError。
        关键算法点：ReLU6 把激活上界截到六，符合 MobileNet v1 的量化友好激活设计。
        """
        if features.ndim != 4:
            raise ValueError("MobileNetBlock 需要 NCHW 输入")
        hidden = self.relu6(self.depth_norm(self.depthwise(features)))
        return self.relu6(self.point_norm(self.pointwise(hidden)))

    def training_step(
        self, features: torch.Tensor, target: torch.Tensor, learning_rate: float
    ) -> float:
        """以 MSE 完成一次反向传播与手写 SGD 参数更新。"""
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
    block = MobileNetBlock(3, 6, stride=2)
    data = torch.randn((2, 3, 8, 8))
    output = block(data)
    assert output.shape == (2, 6, 4, 4) and block.depthwise.groups == 3
    before = block.pointwise.weight.detach().clone()
    assert block.training_step(data, torch.zeros_like(output), 0.01) >= 0.0
    assert not torch.equal(before, block.pointwise.weight.detach())
    print("014_mobilenet_block: all examples passed")
