"""
文件意图：实现扩散模型的前向加噪过程及其训练一步。
适用场景：理解 DDPM 类模型如何把数据逐步扰动为近似高斯噪声。
核心思想：根据 beta 日程累积得到 alpha_bar，再把原样本与噪声按闭式公式混合。
输入输出：输入原始样本、时间步和噪声，输出对应时间步的加噪样本。
时间复杂度：O(batch*feature_count)。空间复杂度：O(batch*feature_count)。
关键边界情况：时间步索引必须落在预定义日程内；样本和噪声形状必须一致。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class DiffusionForwardProcess(torch.nn.Module):
    """手写 DDPM 风格前向过程。"""

    def __init__(self, num_steps: int, beta_start: float, beta_end: float) -> None:
        """初始化 beta 日程和 alpha 累积乘积。"""
        super().__init__()
        if num_steps <= 0:
            raise ValueError("num_steps 必须为正")
        if not (0.0 < beta_start <= beta_end < 1.0):
            raise ValueError("beta 范围必须满足 0 < beta_start <= beta_end < 1")

        self.num_steps = num_steps
        self.betas = torch.nn.Parameter(
            torch.linspace(beta_start, beta_end, steps=num_steps), requires_grad=False
        )
        self.alphas = torch.nn.Parameter(1.0 - self.betas, requires_grad=False)
        self.alpha_bars = torch.nn.Parameter(
            torch.cumprod(self.alphas, dim=0), requires_grad=False
        )

    def forward(
        self, samples: torch.Tensor, time_steps: torch.Tensor, noise: torch.Tensor
    ) -> torch.Tensor:
        """根据闭式公式生成加噪样本。"""
        if samples.shape != noise.shape:
            raise ValueError("samples 与 noise 形状必须一致")
        if time_steps.ndim != 1 or time_steps.shape[0] != samples.shape[0]:
            raise ValueError("time_steps 形状必须为 (batch,)")
        if torch.any(time_steps < 0) or torch.any(time_steps >= self.num_steps):
            raise ValueError("time_steps 超出可用范围")

        alpha_bar = self.alpha_bars[time_steps].reshape(
            (-1,) + (1,) * (samples.ndim - 1)
        )
        return torch.sqrt(alpha_bar) * samples + torch.sqrt(1.0 - alpha_bar) * noise

    def training_step(
        self,
        clean_samples: torch.Tensor,
        time_steps: torch.Tensor,
        target_noisy_samples: torch.Tensor,
        learning_rate: float,
    ) -> float:
        """对可学习噪声执行一次梯度更新，验证前向公式可参与反向传播。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        learned_noise = torch.nn.Parameter(torch.randn_like(clean_samples))
        if learned_noise.grad is not None:
            learned_noise.grad.zero_()

        noisy_samples = self.forward(clean_samples, time_steps, learned_noise)
        if noisy_samples.shape != target_noisy_samples.shape:
            raise ValueError("target_noisy_samples 形状必须与输出一致")

        loss = torch.mean((noisy_samples - target_noisy_samples) ** 2)
        loss.backward()

        with torch.no_grad():
            learned_noise -= learning_rate * learned_noise.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(47)

    process = DiffusionForwardProcess(5, 0.1, 0.2)
    clean_tensor = torch.ones((2, 3))
    noise_tensor = torch.zeros((2, 3))
    time_tensor = torch.tensor([0, 4], dtype=torch.long)
    noisy_tensor = process(clean_tensor, time_tensor, noise_tensor)
    assert noisy_tensor.shape == (2, 3)
    assert torch.all(noisy_tensor[0] < 1.0)
    assert torch.all(noisy_tensor[1] < noisy_tensor[0])

    target_tensor = torch.zeros((2, 3))
    loss_value = process.training_step(clean_tensor, time_tensor, target_tensor, 0.01)
    assert loss_value >= 0.0

    print("029_diffusion_forward_process: all examples passed")
