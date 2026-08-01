"""
文件意图：实现 Transformer 常用的正弦位置编码。
适用场景：为不含递归结构的注意力模型注入序列位置信息。
核心思想：偶数维使用正弦，奇数维使用余弦，不同维度采用不同频率。
输入输出：输入位置长度与嵌入维度，输出对应位置编码矩阵；也支持把编码加到输入序列上。
时间复杂度：O(length*embed_dim)。空间复杂度：O(length*embed_dim)。
关键边界情况：长度和嵌入维度必须为正；输入序列长度不能超过预生成的最大长度。
"""

import math
import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class PositionalEncoding(torch.nn.Module):
    """手写正弦位置编码。"""

    def __init__(self, embed_dim: int, max_length: int) -> None:
        """预计算最大长度内的位置编码。"""
        super().__init__()
        if embed_dim <= 0 or max_length <= 0:
            raise ValueError("embed_dim 和 max_length 必须为正")

        self.embed_dim = embed_dim
        self.max_length = max_length

        position = torch.arange(max_length, dtype=torch.float32).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, embed_dim, 2, dtype=torch.float32)
            * (-math.log(10000.0) / embed_dim)
        )

        encoding = torch.zeros((max_length, embed_dim), dtype=torch.float32)
        encoding[:, 0::2] = torch.sin(position * div_term)
        if embed_dim > 1:
            encoding[:, 1::2] = torch.cos(
                position * div_term[: encoding[:, 1::2].shape[1]]
            )

        self.encoding = torch.nn.Parameter(encoding, requires_grad=False)

    def get_encoding(self, length: int) -> torch.Tensor:
        """返回前 `length` 个位置的编码矩阵。"""
        if length <= 0 or length > self.max_length:
            raise ValueError("length 必须在 1 到 max_length 之间")
        return self.encoding[:length]

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """把位置编码逐批加到输入上。"""
        if inputs.ndim != 3 or inputs.shape[2] != self.embed_dim:
            raise ValueError("inputs 形状必须为 (batch,time,embed_dim)")
        if inputs.shape[1] > self.max_length:
            raise ValueError("输入时间长度超过 max_length")

        return inputs + self.encoding[: inputs.shape[1]].to(inputs.device, inputs.dtype)

    def training_step(
        self, inputs: torch.Tensor, target: torch.Tensor, learning_rate: float
    ) -> float:
        """对输入张量执行一次梯度更新，验证位置编码能参与反向传播。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        learned_inputs = torch.nn.Parameter(inputs.clone())
        if learned_inputs.grad is not None:
            learned_inputs.grad.zero_()

        output = self.forward(learned_inputs)
        if output.shape != target.shape:
            raise ValueError("target 形状必须与输出一致")

        loss = torch.mean((output - target) ** 2)
        loss.backward()

        with torch.no_grad():
            learned_inputs -= learning_rate * learned_inputs.grad

        return float(loss.detach())


if __name__ == "__main__":
    module = PositionalEncoding(6, 10)
    encoding = module.get_encoding(4)
    assert encoding.shape == (4, 6)
    assert torch.allclose(encoding[0, 0::2], torch.zeros(3), atol=1e-6)
    assert torch.allclose(encoding[0, 1::2], torch.ones(3), atol=1e-6)

    inputs = torch.zeros((2, 4, 6))
    outputs = module(inputs)
    assert outputs.shape == (2, 4, 6)
    assert torch.allclose(outputs[0], encoding, atol=1e-6)

    loss_value = module.training_step(inputs, torch.zeros_like(outputs), 0.01)
    assert loss_value >= 0.0

    print("021_positional_encoding: all examples passed")
