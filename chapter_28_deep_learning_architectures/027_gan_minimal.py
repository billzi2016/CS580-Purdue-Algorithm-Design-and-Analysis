"""
文件意图：实现最小可训练 GAN，包括生成器、判别器和一轮交替训练。
适用场景：理解对抗生成模型的基本博弈过程。
核心思想：判别器区分真实样本和生成样本，生成器通过欺骗判别器来学习数据分布。
输入输出：输入噪声为 (batch,noise_dim)，真实样本为 (batch,data_dim)，输出生成样本与判别分数。
时间复杂度：O(batch*(noise_dim*hidden_dim + data_dim*hidden_dim))。
空间复杂度：O(batch*(hidden_dim + data_dim))。
关键边界情况：输入必须是二维张量；本基础版仅实现全连接生成器和判别器。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch
import torch.nn.functional as F


class MinimalGAN(torch.nn.Module):
    """手写基础 GAN。"""

    def __init__(self, noise_dim: int, hidden_dim: int, data_dim: int) -> None:
        """初始化生成器和判别器参数。"""
        super().__init__()
        if noise_dim <= 0 or hidden_dim <= 0 or data_dim <= 0:
            raise ValueError("所有维度都必须为正")

        self.noise_dim = noise_dim
        self.data_dim = data_dim

        self.generator_fc1 = torch.nn.Linear(noise_dim, hidden_dim)
        self.generator_fc2 = torch.nn.Linear(hidden_dim, data_dim)
        self.discriminator_fc1 = torch.nn.Linear(data_dim, hidden_dim)
        self.discriminator_fc2 = torch.nn.Linear(hidden_dim, 1)

    def generate(self, noise: torch.Tensor) -> torch.Tensor:
        """由噪声生成样本。"""
        if noise.ndim != 2 or noise.shape[1] != self.noise_dim:
            raise ValueError("noise 形状必须为 (batch,noise_dim)")
        hidden = torch.relu(self.generator_fc1(noise))
        return torch.tanh(self.generator_fc2(hidden))

    def discriminate(self, samples: torch.Tensor) -> torch.Tensor:
        """输出样本为真的概率。"""
        if samples.ndim != 2 or samples.shape[1] != self.data_dim:
            raise ValueError("samples 形状必须为 (batch,data_dim)")
        hidden = torch.relu(self.discriminator_fc1(samples))
        return torch.sigmoid(self.discriminator_fc2(hidden))

    def forward(self, noise: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """生成样本并给出判别器对生成样本的判断。"""
        fake_samples = self.generate(noise)
        return fake_samples, self.discriminate(fake_samples)

    def training_step(self, real_samples: torch.Tensor, noise: torch.Tensor, learning_rate: float) -> tuple[float, float]:
        """执行一轮判别器更新和生成器更新。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")
        if real_samples.ndim != 2 or real_samples.shape[1] != self.data_dim:
            raise ValueError("real_samples 形状必须为 (batch,data_dim)")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        fake_samples = self.generate(noise).detach()
        real_scores = self.discriminate(real_samples)
        fake_scores = self.discriminate(fake_samples)
        discriminator_loss = (
            F.binary_cross_entropy(real_scores, torch.ones_like(real_scores))
            + F.binary_cross_entropy(fake_scores, torch.zeros_like(fake_scores))
        )
        discriminator_loss.backward()

        with torch.no_grad():
            for parameter in self.discriminator_fc1.parameters():
                parameter -= learning_rate * parameter.grad
            for parameter in self.discriminator_fc2.parameters():
                parameter -= learning_rate * parameter.grad

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        generated = self.generate(noise)
        generator_scores = self.discriminate(generated)
        generator_loss = F.binary_cross_entropy(generator_scores, torch.ones_like(generator_scores))
        generator_loss.backward()

        with torch.no_grad():
            for parameter in self.generator_fc1.parameters():
                parameter -= learning_rate * parameter.grad
            for parameter in self.generator_fc2.parameters():
                parameter -= learning_rate * parameter.grad

        return float(discriminator_loss.detach()), float(generator_loss.detach())


if __name__ == "__main__":
    torch.manual_seed(41)

    model = MinimalGAN(3, 6, 2)
    noise_tensor = torch.randn((4, 3))
    fake_samples, fake_scores = model(noise_tensor)
    assert fake_samples.shape == (4, 2)
    assert fake_scores.shape == (4, 1)
    assert torch.all(fake_scores >= 0.0) and torch.all(fake_scores <= 1.0)

    real_samples = torch.randn((4, 2))
    previous_generator = model.generator_fc2.weight.detach().clone()
    previous_discriminator = model.discriminator_fc2.weight.detach().clone()
    discriminator_loss, generator_loss = model.training_step(real_samples, noise_tensor, 0.01)
    assert discriminator_loss >= 0.0
    assert generator_loss >= 0.0
    assert not torch.equal(previous_generator, model.generator_fc2.weight.detach())
    assert not torch.equal(previous_discriminator, model.discriminator_fc2.weight.detach())

    print("027_gan_minimal: all examples passed")
