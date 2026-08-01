"""
文件意图：手写实现单隐层自编码器的重构前向传播。
适用场景：理解瓶颈表示如何通过编码器和解码器重构输入。
核心思想：输入经线性编码与 ReLU 得到 latent，再用线性解码恢复原维度。
输入输出：输入二维批量 tensor，返回重构值和 latent 表示。
时间复杂度：O(batch*input*latent)。空间复杂度：O(参数量加批量激活)。
关键边界：特征维度必须匹配；本基础版只展示前向与 MSE，不含完整训练循环。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class Autoencoder:
    """手写线性编码器与解码器的基础自编码器。"""

    def __init__(self, input_size: int, latent_size: int, seed: int = 0) -> None:
        """初始化编码器和解码器参数。

        参数：input_size、latent_size 均为正；seed 用于可复现初始化。
        返回：无。
        边界情况：非正维度抛出 ValueError。
        关键算法点：编码/解码均由显式矩阵乘实现，不使用高层层对象。
        """
        if input_size <= 0 or latent_size <= 0:
            raise ValueError("网络维度必须为正")
        generator = torch.Generator().manual_seed(seed)
        self.encoder_weight = (
            torch.randn(
                input_size, latent_size, generator=generator, dtype=torch.float64
            )
            * 0.1
        )
        self.encoder_bias = torch.zeros(latent_size, dtype=torch.float64)
        self.decoder_weight = (
            torch.randn(
                latent_size, input_size, generator=generator, dtype=torch.float64
            )
            * 0.1
        )
        self.decoder_bias = torch.zeros(input_size, dtype=torch.float64)

    def forward(self, features: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """返回输入的重构值和 latent 表示。

        参数：features 形状为 (batch,input_size)。
        返回：(reconstruction, latent) 两个 float64 tensor。
        边界情况：输入维度不匹配抛出 ValueError。
        关键算法点：ReLU 限制 latent 非负，解码层将其映回原特征空间。
        """
        if features.ndim != 2 or features.shape[1] != self.encoder_weight.shape[0]:
            raise ValueError("features 形状不匹配")
        latent = torch.clamp(
            features.to(torch.float64) @ self.encoder_weight + self.encoder_bias,
            min=0.0,
        )
        reconstruction = latent @ self.decoder_weight + self.decoder_bias
        return reconstruction, latent

    def reconstruction_loss(self, features: torch.Tensor) -> float:
        """计算平均平方重构误差。

        参数：features 为有效输入批量。
        返回：标量 MSE。
        边界情况：输入校验与 forward 相同。
        关键算法点：损失直接比较重构与原输入，不需外部标签。
        """
        reconstruction, _ = self.forward(features)
        return float(torch.mean((reconstruction - features.to(torch.float64)) ** 2))


if __name__ == "__main__":
    model = Autoencoder(3, 2, seed=3)
    data = torch.tensor([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0]])
    reconstruction, latent = model.forward(data)
    assert reconstruction.shape == data.shape and latent.shape == (2, 2)
    assert model.reconstruction_loss(data) >= 0.0
    print("003_autoencoder: all examples passed")
