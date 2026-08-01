"""
文件意图：实现手写 multi-head attention 及其训练一步。
适用场景：Transformer 编码器、解码器以及需要并行关注不同子空间的场景。
核心思想：先把输入投影为多个头上的 query、key、value，再分别做缩放点积注意力并拼接。
输入输出：输入 query、key、value 为 (batch,time,embed_dim) 张量，输出同形状结果。
时间复杂度：O(batch*heads*time*head_dim*(time+embed_dim))。
空间复杂度：O(batch*heads*time*time)。
关键边界情况：embed_dim 必须能被 num_heads 整除；mask 若提供则必须扩展到每个头。
"""

import math
import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class MultiHeadAttention(torch.nn.Module):
    """手写多头注意力，不依赖 torch.nn.MultiheadAttention。"""

    def __init__(self, embed_dim: int, num_heads: int) -> None:
        """初始化线性投影参数。"""
        super().__init__()
        if embed_dim <= 0 or num_heads <= 0:
            raise ValueError("embed_dim 和 num_heads 必须为正")
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

    def _project(
        self, tensor: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor
    ) -> torch.Tensor:
        """把输入投影并重排成多头表示。"""
        batch_size, time_steps, _ = tensor.shape
        projected = tensor @ weight + bias
        projected = projected.reshape(
            batch_size, time_steps, self.num_heads, self.head_dim
        )
        return projected.permute(0, 2, 1, 3)

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        mask: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """计算多头注意力输出和权重。"""
        if query.ndim != 3 or key.ndim != 3 or value.ndim != 3:
            raise ValueError("query/key/value 必须都是三维张量")
        if query.shape[0] != key.shape[0] or key.shape[0] != value.shape[0]:
            raise ValueError("batch 维度必须匹配")
        if key.shape[1] != value.shape[1]:
            raise ValueError("key 与 value 的时间长度必须一致")
        if (
            query.shape[2] != self.embed_dim
            or key.shape[2] != self.embed_dim
            or value.shape[2] != self.embed_dim
        ):
            raise ValueError("输入最后一维必须等于 embed_dim")

        projected_query = self._project(query, self.query_weight, self.query_bias)
        projected_key = self._project(key, self.key_weight, self.key_bias)
        projected_value = self._project(value, self.value_weight, self.value_bias)

        scores = torch.matmul(
            projected_query, projected_key.transpose(-2, -1)
        ) / math.sqrt(self.head_dim)
        if mask is not None:
            if mask.shape != scores.shape:
                raise ValueError("mask 形状必须为 (batch, heads, query_time, key_time)")
            scores = scores.masked_fill(mask == 0, -1e9)

        attention_weights = torch.softmax(scores, dim=-1)
        attended = torch.matmul(attention_weights, projected_value)
        attended = attended.permute(0, 2, 1, 3).reshape(
            query.shape[0], query.shape[1], self.embed_dim
        )
        return attended @ self.output_weight + self.output_bias, attention_weights

    def training_step(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        target: torch.Tensor,
        learning_rate: float,
    ) -> float:
        """执行一次前向、反向和手写 SGD 更新。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        output, _ = self.forward(query, key, value)
        if output.shape != target.shape:
            raise ValueError("target 形状必须与输出一致")

        loss = torch.mean((output - target) ** 2)
        loss.backward()

        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(17)

    module = MultiHeadAttention(8, 2)
    query_tensor = torch.randn((2, 4, 8))
    key_tensor = torch.randn((2, 5, 8))
    value_tensor = torch.randn((2, 5, 8))
    outputs, weights = module(query_tensor, key_tensor, value_tensor)
    assert outputs.shape == (2, 4, 8)
    assert weights.shape == (2, 2, 4, 5)
    assert torch.allclose(weights.sum(dim=-1), torch.ones((2, 2, 4)), atol=1e-5)

    mask_tensor = torch.ones((2, 2, 4, 5))
    mask_tensor[:, :, :, 0] = 0
    _, masked_weights = module(query_tensor, key_tensor, value_tensor, mask_tensor)
    assert torch.all(masked_weights[:, :, :, 0] < 1e-6)

    previous_output_weight = module.output_weight.detach().clone()
    loss_value = module.training_step(
        query_tensor,
        key_tensor,
        value_tensor,
        torch.zeros_like(outputs),
        0.01,
    )
    assert loss_value >= 0.0
    assert not torch.equal(previous_output_weight, module.output_weight.detach())

    print("020_multi_head_attention: all examples passed")
