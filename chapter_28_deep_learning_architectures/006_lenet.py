"""
文件意图：手写实现 LeNet 风格卷积分类网络的前向核心。
适用场景：学习经典 CNN 中卷积、tanh、平均池化与线性分类器的串联。
核心思想：两轮 valid 5x5 卷积和 2x2 平均池化将 32x32 图像压缩为 16x5x5 特征。
输入输出：输入 (batch,1,32,32) 图像，返回类别 logits。
时间复杂度：由滑窗卷积主导。空间复杂度：O(中间特征图与参数)。
关键边界：本基础版固定单通道 32x32 输入，不含训练循环或工业级初始化。
"""

import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


def _valid_conv(inputs: torch.Tensor, weights: torch.Tensor, bias: torch.Tensor) -> torch.Tensor:
    """以循环手写 stride=1、无 padding 的 NCHW 交叉相关卷积。"""
    batch, channels, height, width = inputs.shape
    outputs, kernel_channels, kernel_height, kernel_width = weights.shape
    if channels != kernel_channels:
        raise ValueError("卷积通道数不匹配")
    result = torch.zeros((batch, outputs, height - kernel_height + 1, width - kernel_width + 1), dtype=torch.float64)
    for sample in range(batch):
        for output in range(outputs):
            for row in range(result.shape[2]):
                for column in range(result.shape[3]):
                    value = float(bias[output])
                    for channel in range(channels):
                        for kernel_row in range(kernel_height):
                            for kernel_column in range(kernel_width):
                                value += float(inputs[sample, channel, row + kernel_row, column + kernel_column] * weights[output, channel, kernel_row, kernel_column])
                    result[sample, output, row, column] = value
    return result


def _average_pool_2x2(inputs: torch.Tensor) -> torch.Tensor:
    """以 stride=2 手写 2x2 平均池化。"""
    batch, channels, height, width = inputs.shape
    if height % 2 or width % 2:
        raise ValueError("池化输入高宽必须为偶数")
    result = torch.zeros((batch, channels, height // 2, width // 2), dtype=torch.float64)
    for row in range(height // 2):
        for column in range(width // 2):
            result[:, :, row, column] = torch.mean(inputs[:, :, 2 * row:2 * row + 2, 2 * column:2 * column + 2], dim=(2, 3))
    return result


class LeNet:
    """自包含的 LeNet 风格前向网络。"""

    def __init__(self, class_count: int = 10, seed: int = 0) -> None:
        """初始化两层卷积与线性分类参数。

        参数：class_count 为正类别数，seed 控制初始化。
        返回：无。
        边界情况：非正类别数抛出 ValueError。
        关键算法点：参数由基础 tensor 持有，不使用高层卷积或网络模块。
        """
        if class_count <= 0:
            raise ValueError("class_count 必须为正")
        generator = torch.Generator().manual_seed(seed)
        self.conv1_weight = torch.randn(6, 1, 5, 5, generator=generator, dtype=torch.float64) * 0.05
        self.conv1_bias = torch.zeros(6, dtype=torch.float64)
        self.conv2_weight = torch.randn(16, 6, 5, 5, generator=generator, dtype=torch.float64) * 0.05
        self.conv2_bias = torch.zeros(16, dtype=torch.float64)
        self.classifier_weight = torch.randn(400, class_count, generator=generator, dtype=torch.float64) * 0.05
        self.classifier_bias = torch.zeros(class_count, dtype=torch.float64)

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        """返回输入图像的分类 logits。

        参数：images 形状必须为 (batch,1,32,32)。
        返回：形状为 (batch,class_count) 的 float64 logits。
        边界情况：形状不符抛出 ValueError。
        关键算法点：卷积后 tanh 和池化逐步扩大感受野，再展平进行分类。
        """
        if images.ndim != 4 or tuple(images.shape[1:]) != (1, 32, 32):
            raise ValueError("LeNet 基础版只支持 (batch,1,32,32) 输入")
        first = _average_pool_2x2(torch.tanh(_valid_conv(images.to(torch.float64), self.conv1_weight, self.conv1_bias)))
        second = _average_pool_2x2(torch.tanh(_valid_conv(first, self.conv2_weight, self.conv2_bias)))
        return second.reshape(second.shape[0], 400) @ self.classifier_weight + self.classifier_bias


if __name__ == "__main__":
    model = LeNet(class_count=3, seed=1)
    assert model.forward(torch.zeros((2, 1, 32, 32))).shape == (2, 3)
    print("006_lenet: all examples passed")
