"""
文件意图：实现手写 scaled dot-product attention 及其训练一步。
适用场景：Transformer 及其他基于注意力的序列建模模块。
核心思想：用 query 与 key 的点积衡量相关性，经缩放和 softmax 后作为 value 的加权系数。
输入输出：输入 query、key、value 张量，输出注意力结果与注意力权重。
时间复杂度：O(batch*heads*query_len*key_len*head_dim)。
空间复杂度：O(batch*heads*query_len*key_len)。
关键边界情况：query/key/value 的批量维、头数和特征维必须匹配。
"""

import math
import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class ScaledDotProductAttention(torch.nn.Module):
    """手写缩放点积注意力。"""

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        mask: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """计算注意力输出与权重。

        参数：`query`、`key`、`value` 形状均为 `(batch, heads, time, dim)`。
        返回值：`(output, attention_weights)`。
        边界情况：维度不一致或 head_dim 为 0 时抛出 `ValueError`。
        关键算法点：缩放因子使用 `sqrt(dim)`，mask 为 0 的位置被压到极小值。
        """
        if query.ndim != 4 or key.ndim != 4 or value.ndim != 4:
            raise ValueError("query/key/value 必须都是四维张量")
        if query.shape[:2] != key.shape[:2] or key.shape[:2] != value.shape[:2]:
            raise ValueError("batch 和 heads 维度必须匹配")
        if key.shape[2] != value.shape[2] or key.shape[3] != query.shape[3]:
            raise ValueError("key 与 value 长度或 key 与 query 特征维不匹配")

        head_dim = query.shape[3]
        if head_dim <= 0:
            raise ValueError("head_dim 必须为正")

        scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(head_dim)
        if mask is not None:
            if mask.shape != scores.shape:
                raise ValueError("mask 形状必须与分数矩阵一致")
            scores = scores.masked_fill(mask == 0, -1e9)

        attention_weights = torch.softmax(scores, dim=-1)
        output = torch.matmul(attention_weights, value)
        return output, attention_weights

    def training_step(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        target: torch.Tensor,
        learning_rate: float,
    ) -> float:
        """用可学习 query 参数执行一次训练步。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        learned_query = torch.nn.Parameter(query.clone())
        if learned_query.grad is not None:
            learned_query.grad.zero_()

        output, _ = self.forward(learned_query, key, value)
        if output.shape != target.shape:
            raise ValueError("target 形状必须与注意力输出一致")

        loss = torch.mean((output - target) ** 2)
        loss.backward()

        with torch.no_grad():
            learned_query -= learning_rate * learned_query.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(13)

    attention = ScaledDotProductAttention()
    query_tensor = torch.randn((2, 3, 4, 5))
    key_tensor = torch.randn((2, 3, 6, 5))
    value_tensor = torch.randn((2, 3, 6, 7))
    output_tensor, weight_tensor = attention(query_tensor, key_tensor, value_tensor)
    assert output_tensor.shape == (2, 3, 4, 7)
    assert weight_tensor.shape == (2, 3, 4, 6)
    assert torch.allclose(weight_tensor.sum(dim=-1), torch.ones((2, 3, 4)), atol=1e-5)

    mask_tensor = torch.ones((2, 3, 4, 6))
    mask_tensor[:, :, :, -1] = 0
    _, masked_weights = attention(query_tensor, key_tensor, value_tensor, mask_tensor)
    assert torch.all(masked_weights[:, :, :, -1] < 1e-6)

    loss_value = attention.training_step(
        query_tensor,
        key_tensor,
        value_tensor,
        torch.zeros_like(output_tensor),
        0.01,
    )
    assert loss_value >= 0.0

    print("019_scaled_dot_product_attention: all examples passed")
