"""
文件意图：手写实现 NCHW 张量的二维卷积前向传播。
适用场景：理解 CNN 中每个输出像素如何由输入滑窗、卷积核和通道求和得到。
核心思想：对 batch、输出通道和输出空间位置逐项累加 kernel 与带 padding 输入窗口的乘积。
输入输出：输入 NCHW tensor、OICHW kernel 和可选 bias，返回卷积输出。
时间复杂度：O(N*O*Hout*Wout*C*Kh*Kw)。空间复杂度：O(N*O*Hout*Wout)。
关键边界：仅支持正步长与非负 padding；kernel 通道数必须匹配输入。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


def conv2d_manual(
    inputs: torch.Tensor,
    kernel: torch.Tensor,
    bias: torch.Tensor | None = None,
    stride: int = 1,
    padding: int = 0,
) -> torch.Tensor:
    """执行手写二维交叉相关卷积。

    参数：inputs 形状为 (N,C,H,W)，kernel 为 (O,C,Kh,Kw)，bias 可为 (O,)；stride 为正整数，padding 为非负整数。
    返回：形状为 (N,O,Hout,Wout) 的 float64 输出。
    边界情况：输出尺寸非正、形状不匹配或参数非法时抛出 ValueError。
    关键算法点：深度学习框架常称的卷积实际计算交叉相关，因此 kernel 不翻转。
    """
    if inputs.ndim != 4 or kernel.ndim != 4 or stride <= 0 or padding < 0:
        raise ValueError("输入、kernel、stride 或 padding 无效")
    batch, input_channels, height, width = inputs.shape
    output_channels, kernel_channels, kernel_height, kernel_width = kernel.shape
    if input_channels != kernel_channels or (
        bias is not None and (bias.ndim != 1 or bias.numel() != output_channels)
    ):
        raise ValueError("通道或 bias 形状不匹配")
    output_height = (height + 2 * padding - kernel_height) // stride + 1
    output_width = (width + 2 * padding - kernel_width) // stride + 1
    if output_height <= 0 or output_width <= 0:
        raise ValueError("kernel 与输入尺寸不兼容")
    padded = torch.zeros(
        (batch, input_channels, height + 2 * padding, width + 2 * padding),
        dtype=torch.float64,
    )
    padded[:, :, padding : padding + height, padding : padding + width] = inputs.to(
        torch.float64
    )
    result = torch.zeros(
        (batch, output_channels, output_height, output_width), dtype=torch.float64
    )
    weights = kernel.to(torch.float64)
    for sample in range(batch):
        for output_channel in range(output_channels):
            for row in range(output_height):
                for column in range(output_width):
                    total = float(bias[output_channel]) if bias is not None else 0.0
                    for input_channel in range(input_channels):
                        for kernel_row in range(kernel_height):
                            for kernel_column in range(kernel_width):
                                total += float(
                                    padded[
                                        sample,
                                        input_channel,
                                        row * stride + kernel_row,
                                        column * stride + kernel_column,
                                    ]
                                    * weights[
                                        output_channel,
                                        input_channel,
                                        kernel_row,
                                        kernel_column,
                                    ]
                                )
                    result[sample, output_channel, row, column] = total
    return result


if __name__ == "__main__":
    image = torch.tensor([[[[1.0, 2.0], [3.0, 4.0]]]])
    kernel = torch.tensor([[[[1.0, 0.0], [0.0, 1.0]]]])
    assert torch.equal(
        conv2d_manual(image, kernel), torch.tensor([[[[5.0]]]], dtype=torch.float64)
    )
    assert conv2d_manual(image, kernel, padding=1).shape == (1, 1, 3, 3)
    print("005_manual_2d_convolution: all examples passed")
