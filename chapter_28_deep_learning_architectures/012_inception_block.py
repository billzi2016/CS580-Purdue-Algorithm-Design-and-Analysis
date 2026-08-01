"""
文件意图：实现 Inception 风格多分支卷积块及训练一步。
适用场景：同时提取不同感受野的局部特征并控制计算量。
核心思想：1x1、1x1-3x3、1x1-5x5、池化-1x1 四分支并行计算后沿通道维拼接。
输入输出：输入 NCHW 特征图，返回四分支通道拼接特征。
时间复杂度：为四条卷积分支成本之和。空间复杂度：O(分支激活与参数)。
关键边界：所有通道参数必须为正；输入必须为四维 NCHW tensor。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class InceptionBlock(torch.nn.Module):
    """显式定义四条分支的 Inception 卷积块。"""

    def __init__(
        self, input_channels: int, channels: tuple[int, int, int, int, int, int]
    ) -> None:
        """创建四分支模块。

        参数：channels=(one,three_reduce,three,five_reduce,five,pool_proj)，所有值为正。
        返回：无。边界情况：非法通道抛出 ValueError。
        关键算法点：较大卷积前先 1x1 降维以减少参数和运算。
        """
        super().__init__()
        if (
            input_channels <= 0
            or len(channels) != 6
            or any(value <= 0 for value in channels)
        ):
            raise ValueError("Inception 通道参数无效")
        one, three_reduce, three, five_reduce, five, pool_proj = channels
        self.branch1 = torch.nn.Conv2d(input_channels, one, 1)
        self.branch2 = torch.nn.Sequential(
            torch.nn.Conv2d(input_channels, three_reduce, 1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(three_reduce, three, 3, padding=1),
        )
        self.branch3 = torch.nn.Sequential(
            torch.nn.Conv2d(input_channels, five_reduce, 1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(five_reduce, five, 5, padding=2),
        )
        self.branch4 = torch.nn.Sequential(
            torch.nn.MaxPool2d(3, stride=1, padding=1),
            torch.nn.Conv2d(input_channels, pool_proj, 1),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        """计算四个分支并按通道维拼接。

        参数：features 是 NCHW tensor。返回：拼接特征图。
        边界情况：非四维输入抛出 ValueError。
        关键算法点：padding 与 stride 保证四分支空间尺寸一致，才能安全拼接。
        """
        if features.ndim != 4:
            raise ValueError("InceptionBlock 需要 NCHW 输入")
        return torch.cat(
            (
                self.branch1(features),
                self.branch2(features),
                self.branch3(features),
                self.branch4(features),
            ),
            dim=1,
        )

    def training_step(
        self, features: torch.Tensor, target: torch.Tensor, learning_rate: float
    ) -> float:
        """以 MSE 反向传播并手写 SGD 更新全部四分支参数。"""
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
    block = InceptionBlock(3, (2, 2, 3, 2, 4, 1))
    data = torch.randn((1, 3, 8, 8))
    output = block(data)
    assert output.shape == (1, 10, 8, 8)
    before = block.branch1.weight.detach().clone()
    assert block.training_step(data, torch.zeros_like(output), 0.01) >= 0.0
    assert not torch.equal(before, block.branch1.weight.detach())
    print("012_inception_block: all examples passed")
