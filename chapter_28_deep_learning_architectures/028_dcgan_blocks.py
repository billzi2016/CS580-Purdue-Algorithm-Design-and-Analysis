"""
文件意图：实现 DCGAN 的生成器块、判别器块及其训练一步。
适用场景：基于卷积的图像生成与判别教学实现。
核心思想：生成器使用转置卷积逐步上采样，判别器使用卷积逐步下采样。
输入输出：生成器输入噪声张量，判别器输入图像张量，输出真假分数。
时间复杂度：与卷积核大小、空间尺寸和通道数成正比。
空间复杂度：与中间特征图尺寸和通道数成正比。
关键边界情况：本基础版只实现单个生成器块和单个判别器块，不覆盖完整 DCGAN pipeline。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch
import torch.nn.functional as F


class DCGANBlocks(torch.nn.Module):
    """手写最小 DCGAN 生成器块和判别器块。"""

    def __init__(
        self, noise_channels: int, feature_channels: int, image_channels: int
    ) -> None:
        """初始化转置卷积和卷积参数。"""
        super().__init__()
        if noise_channels <= 0 or feature_channels <= 0 or image_channels <= 0:
            raise ValueError("通道数必须为正")

        self.noise_channels = noise_channels
        self.image_channels = image_channels

        self.generator_block = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(
                noise_channels, feature_channels, kernel_size=4, stride=1, padding=0
            ),
            torch.nn.BatchNorm2d(feature_channels),
            torch.nn.ReLU(),
            torch.nn.ConvTranspose2d(
                feature_channels, image_channels, kernel_size=4, stride=2, padding=1
            ),
            torch.nn.Tanh(),
        )
        self.discriminator_block = torch.nn.Sequential(
            torch.nn.Conv2d(
                image_channels, feature_channels, kernel_size=4, stride=2, padding=1
            ),
            torch.nn.LeakyReLU(0.2),
            torch.nn.Conv2d(feature_channels, 1, kernel_size=4, stride=1, padding=0),
            torch.nn.Sigmoid(),
        )

    def generate(self, noise: torch.Tensor) -> torch.Tensor:
        """由噪声张量生成图像。"""
        if noise.ndim != 4 or noise.shape[1] != self.noise_channels:
            raise ValueError("noise 形状必须为 (batch,noise_channels,1,1)")
        return self.generator_block(noise)

    def discriminate(self, images: torch.Tensor) -> torch.Tensor:
        """输出图像为真的概率图。"""
        if images.ndim != 4 or images.shape[1] != self.image_channels:
            raise ValueError("images 形状必须为 (batch,image_channels,height,width)")
        return self.discriminator_block(images)

    def training_step(
        self, real_images: torch.Tensor, noise: torch.Tensor, learning_rate: float
    ) -> tuple[float, float]:
        """执行一次最小 DCGAN 训练步。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        fake_images = self.generate(noise).detach()
        real_scores = self.discriminate(real_images)
        fake_scores = self.discriminate(fake_images)
        discriminator_loss = F.binary_cross_entropy(
            real_scores, torch.ones_like(real_scores)
        ) + F.binary_cross_entropy(fake_scores, torch.zeros_like(fake_scores))
        discriminator_loss.backward()

        with torch.no_grad():
            for parameter in self.discriminator_block.parameters():
                if parameter.grad is not None:
                    parameter -= learning_rate * parameter.grad

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        generated = self.generate(noise)
        generator_scores = self.discriminate(generated)
        generator_loss = F.binary_cross_entropy(
            generator_scores, torch.ones_like(generator_scores)
        )
        generator_loss.backward()

        with torch.no_grad():
            for parameter in self.generator_block.parameters():
                if parameter.grad is not None:
                    parameter -= learning_rate * parameter.grad

        return float(discriminator_loss.detach()), float(generator_loss.detach())


if __name__ == "__main__":
    torch.manual_seed(43)

    model = DCGANBlocks(4, 8, 3)
    noise_tensor = torch.randn((2, 4, 1, 1))
    fake_images = model.generate(noise_tensor)
    assert fake_images.shape == (2, 3, 8, 8)

    fake_scores = model.discriminate(fake_images)
    assert fake_scores.shape == (2, 1, 1, 1)

    real_images = torch.randn((2, 3, 8, 8))
    previous_generator = model.generator_block[0].weight.detach().clone()
    previous_discriminator = model.discriminator_block[0].weight.detach().clone()
    discriminator_loss, generator_loss = model.training_step(
        real_images, noise_tensor, 0.001
    )
    assert discriminator_loss >= 0.0
    assert generator_loss >= 0.0
    assert not torch.equal(previous_generator, model.generator_block[0].weight.detach())
    assert not torch.equal(
        previous_discriminator, model.discriminator_block[0].weight.detach()
    )

    print("028_dcgan_blocks: all examples passed")
