"""
文件意图：实现基础版 U-Net 编码器-解码器结构及其训练一步。
适用场景：语义分割、医学图像分割和需要多尺度局部细节恢复的视觉任务。
核心思想：编码路径逐步下采样提取上下文，解码路径逐步上采样并与浅层特征做跳连融合。
输入输出：输入为 (batch,in_channels,height,width)，输出为 (batch,out_channels,height,width)。
时间复杂度：O(batch*height*width*channels^2)，这里给出的是基础卷积版的数量级。
空间复杂度：O(batch*height*width*channels)。
关键边界情况：本基础版要求输入高宽为 2 的倍数，并只做一级下采样与上采样。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch
import torch.nn.functional as F


class UNet(torch.nn.Module):
    """手写一级 U-Net。"""

    def __init__(self, in_channels: int, base_channels: int, out_channels: int) -> None:
        """初始化编码、瓶颈、解码和输出卷积。"""
        super().__init__()
        if in_channels <= 0 or base_channels <= 0 or out_channels <= 0:
            raise ValueError("通道数必须为正")

        self.encoder_conv1 = torch.nn.Conv2d(
            in_channels, base_channels, kernel_size=3, padding=1
        )
        self.encoder_conv2 = torch.nn.Conv2d(
            base_channels, base_channels, kernel_size=3, padding=1
        )
        self.bottleneck_conv1 = torch.nn.Conv2d(
            base_channels, base_channels * 2, kernel_size=3, padding=1
        )
        self.bottleneck_conv2 = torch.nn.Conv2d(
            base_channels * 2, base_channels * 2, kernel_size=3, padding=1
        )
        self.decoder_conv1 = torch.nn.Conv2d(
            base_channels * 3, base_channels, kernel_size=3, padding=1
        )
        self.decoder_conv2 = torch.nn.Conv2d(
            base_channels, base_channels, kernel_size=3, padding=1
        )
        self.output_conv = torch.nn.Conv2d(base_channels, out_channels, kernel_size=1)

    def _double_conv(
        self, first: torch.nn.Conv2d, second: torch.nn.Conv2d, inputs: torch.Tensor
    ) -> torch.Tensor:
        """执行两次卷积与 ReLU。"""
        hidden = torch.relu(first(inputs))
        return torch.relu(second(hidden))

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """执行一级 U-Net 前向传播。"""
        if inputs.ndim != 4:
            raise ValueError("inputs 必须是四维张量")
        if inputs.shape[2] % 2 != 0 or inputs.shape[3] % 2 != 0:
            raise ValueError("输入高宽必须为 2 的倍数")

        encoder_features = self._double_conv(
            self.encoder_conv1, self.encoder_conv2, inputs
        )
        pooled = F.max_pool2d(encoder_features, kernel_size=2, stride=2)
        bottleneck = self._double_conv(
            self.bottleneck_conv1, self.bottleneck_conv2, pooled
        )

        upsampled = F.interpolate(bottleneck, scale_factor=2, mode="nearest")
        merged = torch.cat((upsampled, encoder_features), dim=1)
        decoded = self._double_conv(self.decoder_conv1, self.decoder_conv2, merged)
        return self.output_conv(decoded)

    def training_step(
        self, inputs: torch.Tensor, target: torch.Tensor, learning_rate: float
    ) -> float:
        """执行一次 U-Net 训练步。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        output = self.forward(inputs)
        if output.shape != target.shape:
            raise ValueError("target 形状必须与输出一致")

        loss = torch.mean((output - target) ** 2)
        loss.backward()

        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(37)

    model = UNet(3, 4, 2)
    image_tensor = torch.randn((2, 3, 8, 8))
    output_tensor = model(image_tensor)
    assert output_tensor.shape == (2, 2, 8, 8)

    zero_output = model(torch.zeros((1, 3, 8, 8)))
    assert zero_output.shape == (1, 2, 8, 8)

    previous_weight = model.output_conv.weight.detach().clone()
    loss_value = model.training_step(
        image_tensor, torch.zeros_like(output_tensor), 0.001
    )
    assert loss_value >= 0.0
    assert not torch.equal(previous_weight, model.output_conv.weight.detach())

    print("026_unet: all examples passed")
