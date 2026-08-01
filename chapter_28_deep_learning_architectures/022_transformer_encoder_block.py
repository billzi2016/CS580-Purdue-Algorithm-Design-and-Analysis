"""
文件意图：实现手写 Transformer encoder block 及其训练一步。
适用场景：编码上下文序列表示的自注意力网络。
核心思想：残差连接包裹多头自注意力和前馈网络，再配合层归一化稳定训练。
输入输出：输入输出均为 (batch,time,embed_dim) 张量。
时间复杂度：O(batch*time*time*embed_dim + batch*time*embed_dim*ffn_dim)。
空间复杂度：O(batch*time*embed_dim + batch*heads*time*time)。
关键边界情况：embed_dim 必须能被头数整除；mask 形状需匹配注意力分数矩阵。
"""

import math
import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class TransformerEncoderBlock(torch.nn.Module):
    """手写带残差与层归一化的编码器块。"""

    def __init__(self, embed_dim: int, num_heads: int, ffn_dim: int) -> None:
        """初始化多头注意力和前馈层参数。"""
        super().__init__()
        if embed_dim <= 0 or num_heads <= 0 or ffn_dim <= 0:
            raise ValueError("embed_dim、num_heads、ffn_dim 必须为正")
        if embed_dim % num_heads != 0:
            raise ValueError("embed_dim 必须能被 num_heads 整除")

        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        self.query_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)
        self.key_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)
        self.value_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)
        self.output_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)
        self.query_bias = torch.nn.Parameter(torch.zeros(embed_dim))
        self.key_bias = torch.nn.Parameter(torch.zeros(embed_dim))
        self.value_bias = torch.nn.Parameter(torch.zeros(embed_dim))
        self.output_bias = torch.nn.Parameter(torch.zeros(embed_dim))

        self.ffn_weight_1 = torch.nn.Parameter(torch.randn(embed_dim, ffn_dim) * 0.1)
        self.ffn_bias_1 = torch.nn.Parameter(torch.zeros(ffn_dim))
        self.ffn_weight_2 = torch.nn.Parameter(torch.randn(ffn_dim, embed_dim) * 0.1)
        self.ffn_bias_2 = torch.nn.Parameter(torch.zeros(embed_dim))

    def _layer_norm(self, tensor: torch.Tensor, epsilon: float = 1e-5) -> torch.Tensor:
        """按最后一维做基础层归一化。"""
        mean = tensor.mean(dim=-1, keepdim=True)
        variance = ((tensor - mean) ** 2).mean(dim=-1, keepdim=True)
        return (tensor - mean) / torch.sqrt(variance + epsilon)

    def _project(
        self, tensor: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor
    ) -> torch.Tensor:
        """线性投影并拆成多头。"""
        batch_size, time_steps, _ = tensor.shape
        projected = tensor @ weight + bias
        projected = projected.reshape(
            batch_size, time_steps, self.num_heads, self.head_dim
        )
        return projected.permute(0, 2, 1, 3)

    def _self_attention(
        self, inputs: torch.Tensor, mask: torch.Tensor | None
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """执行多头自注意力。"""
        query = self._project(inputs, self.query_weight, self.query_bias)
        key = self._project(inputs, self.key_weight, self.key_bias)
        value = self._project(inputs, self.value_weight, self.value_bias)

        scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(self.head_dim)
        if mask is not None:
            if mask.shape != scores.shape:
                raise ValueError("mask 形状必须为 (batch, heads, time, time)")
            scores = scores.masked_fill(mask == 0, -1e9)

        attention_weights = torch.softmax(scores, dim=-1)
        attended = torch.matmul(attention_weights, value)
        attended = attended.permute(0, 2, 1, 3).reshape(
            inputs.shape[0], inputs.shape[1], self.embed_dim
        )
        return attended @ self.output_weight + self.output_bias, attention_weights

    def forward(
        self, inputs: torch.Tensor, mask: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """返回编码器块输出和注意力权重。"""
        if inputs.ndim != 3 or inputs.shape[2] != self.embed_dim:
            raise ValueError("inputs 形状必须为 (batch,time,embed_dim)")

        attention_output, attention_weights = self._self_attention(inputs, mask)
        attention_residual = self._layer_norm(inputs + attention_output)

        feed_forward = torch.relu(
            attention_residual @ self.ffn_weight_1 + self.ffn_bias_1
        )
        feed_forward = feed_forward @ self.ffn_weight_2 + self.ffn_bias_2
        return self._layer_norm(attention_residual + feed_forward), attention_weights

    def training_step(
        self, inputs: torch.Tensor, target: torch.Tensor, learning_rate: float
    ) -> float:
        """执行一次 encoder block 训练步。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        output, _ = self.forward(inputs)
        if output.shape != target.shape:
            raise ValueError("target 形状必须与输出一致")

        loss = torch.mean((output - target) ** 2)
        loss.backward()

        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(19)

    block = TransformerEncoderBlock(8, 2, 12)
    inputs = torch.randn((2, 4, 8))
    outputs, weights = block(inputs)
    assert outputs.shape == (2, 4, 8)
    assert weights.shape == (2, 2, 4, 4)
    assert torch.allclose(weights.sum(dim=-1), torch.ones((2, 2, 4)), atol=1e-5)

    mask = torch.ones((2, 2, 4, 4))
    mask[:, :, :, -1] = 0
    _, masked_weights = block(inputs, mask)
    assert torch.all(masked_weights[:, :, :, -1] < 1e-6)

    previous_weight = block.ffn_weight_2.detach().clone()
    loss_value = block.training_step(inputs, torch.zeros_like(outputs), 0.01)
    assert loss_value >= 0.0
    assert not torch.equal(previous_weight, block.ffn_weight_2.detach())

    print("022_transformer_encoder_block: all examples passed")
