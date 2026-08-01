"""
文件意图：手写实现变分自编码器（VAE）的核心重参数化与 KL 损失。
适用场景：理解潜变量高斯分布、可微采样和 ELBO 中的正则项。
核心思想：编码器输出 mean/log_variance，采样 z=mean+exp(0.5*log_variance)*epsilon。
输入输出：输入编码特征，返回均值、对数方差和 latent；提供 KL 项计算。
时间复杂度：O(batch*input*latent)。空间复杂度：O(参数量加批量张量)。
关键边界：输入维度须匹配；训练/评估模式分别使用随机采样与均值 latent。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class VariationalAutoencoderCore:
    """仅包含 VAE 编码分布与重参数化的教学核心。"""

    def __init__(self, input_size: int, latent_size: int, seed: int = 0) -> None:
        """初始化从输入到 mean 与 log_variance 的两组线性参数。

        参数：input_size 和 latent_size 必须为正，seed 用于可复现初始化。
        返回：无。
        边界情况：非正维度抛出 ValueError。
        关键算法点：均值和对数方差分别参数化，确保方差通过指数始终为正。
        """
        if input_size <= 0 or latent_size <= 0:
            raise ValueError("网络维度必须为正")
        generator = torch.Generator().manual_seed(seed)
        self.mean_weight = (
            torch.randn(
                input_size, latent_size, generator=generator, dtype=torch.float64
            )
            * 0.1
        )
        self.mean_bias = torch.zeros(latent_size, dtype=torch.float64)
        self.log_variance_weight = (
            torch.randn(
                input_size, latent_size, generator=generator, dtype=torch.float64
            )
            * 0.1
        )
        self.log_variance_bias = torch.zeros(latent_size, dtype=torch.float64)

    def encode(self, features: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """计算近似后验的均值和对数方差。

        参数：features 形状为 (batch,input_size)。
        返回：(mean, log_variance)。
        边界情况：输入维度不匹配抛出 ValueError。
        关键算法点：log_variance 直接参数化，避免直接优化正方差带来的非负约束。
        """
        if features.ndim != 2 or features.shape[1] != self.mean_weight.shape[0]:
            raise ValueError("features 形状不匹配")
        data = features.to(torch.float64)
        return (
            data @ self.mean_weight + self.mean_bias,
            data @ self.log_variance_weight + self.log_variance_bias,
        )

    def reparameterize(
        self, mean: torch.Tensor, log_variance: torch.Tensor, training: bool = True
    ) -> torch.Tensor:
        """以重参数化技巧从对角高斯后验获得 latent。

        参数：mean、log_variance 形状相同；training 控制是否注入标准正态噪声。
        返回：与 mean 同形状的 latent tensor。
        边界情况：形状不匹配抛出 ValueError；评估模式直接返回 mean。
        关键算法点：把随机性移动到 epsilon，使 mean/log_variance 保留可微路径。
        """
        if mean.shape != log_variance.shape:
            raise ValueError("mean 与 log_variance 形状必须一致")
        if not training:
            return mean
        return mean + torch.exp(0.5 * log_variance) * torch.randn_like(mean)

    def forward(
        self, features: torch.Tensor, training: bool = True
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """返回 mean、log_variance 和重参数化 latent。

        参数：features 是输入批量，training 控制采样方式。
        返回：(mean, log_variance, latent)。
        边界情况：同 encode 与 reparameterize。
        关键算法点：该核心可接任意手写 decoder，当前不把不完整 VAE 包装成工业模型。
        """
        mean, log_variance = self.encode(features)
        return mean, log_variance, self.reparameterize(mean, log_variance, training)

    @staticmethod
    def kl_divergence(mean: torch.Tensor, log_variance: torch.Tensor) -> torch.Tensor:
        """计算每个样本 q(z|x) 相对标准正态先验的 KL 散度。

        参数：mean 与 log_variance 形状为 (batch,latent)。
        返回：形状为 (batch,) 的非负 KL tensor。
        边界情况：形状不匹配抛出 ValueError。
        关键算法点：对角高斯到 N(0,I) 的 KL 可解析求和，无需采样估计。
        """
        if mean.shape != log_variance.shape or mean.ndim != 2:
            raise ValueError("mean 与 log_variance 必须是同形二维张量")
        return -0.5 * torch.sum(
            1.0 + log_variance - mean.square() - torch.exp(log_variance), dim=1
        )


if __name__ == "__main__":
    model = VariationalAutoencoderCore(3, 2, seed=5)
    data = torch.tensor([[1.0, 0.0, 1.0]])
    mean, log_variance, latent = model.forward(data, training=False)
    assert torch.equal(latent, mean)
    assert torch.all(
        VariationalAutoencoderCore.kl_divergence(mean, log_variance) >= 0.0
    )
    print("004_variational_autoencoder_core: all examples passed")
