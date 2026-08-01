"""
文件意图：实现扩散模型单步反向去噪公式及其训练一步。
适用场景：理解 DDPM 采样阶段如何从 x_t 逐步恢复到更干净的样本。
核心思想：根据预测噪声估计 posterior mean，再注入与 beta 对应的随机项完成一步反向采样。
输入输出：输入当前 noisy sample、时间步和预测噪声，输出上一步样本估计。
时间复杂度：O(batch*feature_count)。空间复杂度：O(batch*feature_count)。
关键边界情况：时间步必须在合法范围内；样本与预测噪声形状必须一致。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class DiffusionReverseStep(torch.nn.Module):
    """手写 DDPM 单步反向过程。"""

    def __init__(self, num_steps: int, beta_start: float, beta_end: float) -> None:
        """初始化 beta、alpha 与 alpha_bar 日程。"""
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
        self.alpha_bars = torch.nn.Parameter(torch.cumprod(self.alphas, dim=0), requires_grad=False)

    def forward(
        self,
        noisy_samples: torch.Tensor,
        time_steps: torch.Tensor,
        predicted_noise: torch.Tensor,
        stochastic_noise: torch.Tensor | None = None,
    ) -> torch.Tensor:
        """执行一步反向采样。"""
        if noisy_samples.shape != predicted_noise.shape:
            raise ValueError("noisy_samples 与 predicted_noise 形状必须一致")
        if time_steps.ndim != 1 or time_steps.shape[0] != noisy_samples.shape[0]:
            raise ValueError("time_steps 形状必须为 (batch,)")
        if torch.any(time_steps < 0) or torch.any(time_steps >= self.num_steps):
            raise ValueError("time_steps 超出范围")

        if stochastic_noise is None:
            stochastic_noise = torch.zeros_like(noisy_samples)
        if stochastic_noise.shape != noisy_samples.shape:
            raise ValueError("stochastic_noise 形状必须与样本一致")

        beta_t = self.betas[time_steps].reshape((-1,) + (1,) * (noisy_samples.ndim - 1))
        alpha_t = self.alphas[time_steps].reshape((-1,) + (1,) * (noisy_samples.ndim - 1))
        alpha_bar_t = self.alpha_bars[time_steps].reshape((-1,) + (1,) * (noisy_samples.ndim - 1))

        mean = (noisy_samples - beta_t / torch.sqrt(1.0 - alpha_bar_t) * predicted_noise) / torch.sqrt(alpha_t)
        nonzero_mask = (time_steps > 0).reshape((-1,) + (1,) * (noisy_samples.ndim - 1)).to(noisy_samples.dtype)
        return mean + nonzero_mask * torch.sqrt(beta_t) * stochastic_noise

    def training_step(
        self,
        noisy_samples: torch.Tensor,
        time_steps: torch.Tensor,
        target_previous_samples: torch.Tensor,
        learning_rate: float,
    ) -> float:
        """对可学习预测噪声执行一次梯度更新。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        predicted_noise = torch.nn.Parameter(torch.randn_like(noisy_samples))
        if predicted_noise.grad is not None:
            predicted_noise.grad.zero_()

        estimated_previous = self.forward(noisy_samples, time_steps, predicted_noise)
        if estimated_previous.shape != target_previous_samples.shape:
            raise ValueError("target_previous_samples 形状必须与输出一致")

        loss = torch.mean((estimated_previous - target_previous_samples) ** 2)
        loss.backward()

        with torch.no_grad():
            predicted_noise -= learning_rate * predicted_noise.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(53)

    step = DiffusionReverseStep(5, 0.1, 0.2)
    noisy_tensor = torch.ones((2, 3))
    predicted_noise_tensor = torch.zeros((2, 3))
    time_tensor = torch.tensor([0, 4], dtype=torch.long)
    previous_tensor = step(noisy_tensor, time_tensor, predicted_noise_tensor, torch.zeros_like(noisy_tensor))
    assert previous_tensor.shape == (2, 3)
    assert torch.allclose(previous_tensor[0], noisy_tensor[0] / torch.sqrt(step.alphas[0]), atol=1e-6)

    loss_value = step.training_step(noisy_tensor, time_tensor, torch.zeros_like(noisy_tensor), 0.01)
    assert loss_value >= 0.0

    print("030_diffusion_reverse_step: all examples passed")
