"""
文件意图：实现手写 Transformer decoder block 及其训练一步。
适用场景：需要自回归生成并同时读取编码器上下文的序列建模任务。
核心思想：先做带因果约束的自注意力，再做 encoder-decoder cross attention，最后经过前馈网络。
输入输出：输入 target 与 memory 为 (batch,time,embed_dim) 张量，输出 target 同形状结果。
时间复杂度：O(batch*time*time*embed_dim + batch*tgt_time*src_time*embed_dim)。
空间复杂度：O(batch*heads*(tgt_time*tgt_time + tgt_time*src_time))。
关键边界情况：embed_dim 必须能被头数整除；target 和 memory 的最后一维必须一致。
"""

import math
import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class TransformerDecoderBlock(torch.nn.Module):
    """手写解码器块。"""

    def __init__(self, embed_dim: int, num_heads: int, ffn_dim: int) -> None:
        """初始化两层注意力和前馈参数。"""
        super().__init__()
        if embed_dim <= 0 or num_heads <= 0 or ffn_dim <= 0:
            raise ValueError("embed_dim、num_heads、ffn_dim 必须为正")
        if embed_dim % num_heads != 0:
            raise ValueError("embed_dim 必须能被 num_heads 整除")

        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        self.self_query_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)
        self.self_key_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)
        self.self_value_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)

        self.cross_query_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)
        self.cross_key_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)
        self.cross_value_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)

        self.self_output_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)
        self.cross_output_weight = torch.nn.Parameter(torch.randn(embed_dim, embed_dim) * 0.1)
        self.self_bias = torch.nn.Parameter(torch.zeros(embed_dim))
        self.cross_bias = torch.nn.Parameter(torch.zeros(embed_dim))

        self.ffn_weight_1 = torch.nn.Parameter(torch.randn(embed_dim, ffn_dim) * 0.1)
        self.ffn_bias_1 = torch.nn.Parameter(torch.zeros(ffn_dim))
        self.ffn_weight_2 = torch.nn.Parameter(torch.randn(ffn_dim, embed_dim) * 0.1)
        self.ffn_bias_2 = torch.nn.Parameter(torch.zeros(embed_dim))

    def _layer_norm(self, tensor: torch.Tensor, epsilon: float = 1e-5) -> torch.Tensor:
        """按最后一维做层归一化。"""
        mean = tensor.mean(dim=-1, keepdim=True)
        variance = ((tensor - mean) ** 2).mean(dim=-1, keepdim=True)
        return (tensor - mean) / torch.sqrt(variance + epsilon)

    def _project(self, tensor: torch.Tensor, weight: torch.Tensor) -> torch.Tensor:
        """线性投影并拆成多头。"""
        batch_size, time_steps, _ = tensor.shape
        projected = tensor @ weight
        projected = projected.reshape(batch_size, time_steps, self.num_heads, self.head_dim)
        return projected.permute(0, 2, 1, 3)

    def _attention(
        self,
        query_source: torch.Tensor,
        key_value_source: torch.Tensor,
        query_weight: torch.Tensor,
        key_weight: torch.Tensor,
        value_weight: torch.Tensor,
        output_weight: torch.Tensor,
        output_bias: torch.Tensor,
        mask: torch.Tensor | None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """执行一次多头注意力。"""
        query = self._project(query_source, query_weight)
        key = self._project(key_value_source, key_weight)
        value = self._project(key_value_source, value_weight)

        scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(self.head_dim)
        if mask is not None:
            if mask.shape != scores.shape:
                raise ValueError("mask 形状不匹配")
            scores = scores.masked_fill(mask == 0, -1e9)

        weights = torch.softmax(scores, dim=-1)
        attended = torch.matmul(weights, value)
        attended = attended.permute(0, 2, 1, 3).reshape(query_source.shape[0], query_source.shape[1], self.embed_dim)
        return attended @ output_weight + output_bias, weights

    def forward(
        self,
        target: torch.Tensor,
        memory: torch.Tensor,
        self_mask: torch.Tensor | None = None,
        cross_mask: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """返回解码器输出、自注意力权重和交叉注意力权重。"""
        if target.ndim != 3 or memory.ndim != 3:
            raise ValueError("target 和 memory 必须都是三维张量")
        if target.shape[0] != memory.shape[0] or target.shape[2] != self.embed_dim or memory.shape[2] != self.embed_dim:
            raise ValueError("target 与 memory 的 batch/embed_dim 必须匹配")

        self_output, self_weights = self._attention(
            target,
            target,
            self.self_query_weight,
            self.self_key_weight,
            self.self_value_weight,
            self.self_output_weight,
            self.self_bias,
            self_mask,
        )
        self_residual = self._layer_norm(target + self_output)

        cross_output, cross_weights = self._attention(
            self_residual,
            memory,
            self.cross_query_weight,
            self.cross_key_weight,
            self.cross_value_weight,
            self.cross_output_weight,
            self.cross_bias,
            cross_mask,
        )
        cross_residual = self._layer_norm(self_residual + cross_output)

        feed_forward = torch.relu(cross_residual @ self.ffn_weight_1 + self.ffn_bias_1)
        feed_forward = feed_forward @ self.ffn_weight_2 + self.ffn_bias_2
        return self._layer_norm(cross_residual + feed_forward), self_weights, cross_weights

    def training_step(
        self,
        target: torch.Tensor,
        memory: torch.Tensor,
        expected: torch.Tensor,
        learning_rate: float,
    ) -> float:
        """执行一次 decoder block 训练步。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        output, _, _ = self.forward(target, memory)
        if output.shape != expected.shape:
            raise ValueError("expected 形状必须与输出一致")

        loss = torch.mean((output - expected) ** 2)
        loss.backward()

        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(23)

    block = TransformerDecoderBlock(8, 2, 12)
    target_tensor = torch.randn((2, 4, 8))
    memory_tensor = torch.randn((2, 5, 8))
    outputs, self_weights, cross_weights = block(target_tensor, memory_tensor)
    assert outputs.shape == (2, 4, 8)
    assert self_weights.shape == (2, 2, 4, 4)
    assert cross_weights.shape == (2, 2, 4, 5)
    assert torch.allclose(self_weights.sum(dim=-1), torch.ones((2, 2, 4)), atol=1e-5)
    assert torch.allclose(cross_weights.sum(dim=-1), torch.ones((2, 2, 4)), atol=1e-5)

    causal_mask = torch.tril(torch.ones((4, 4))).reshape(1, 1, 4, 4).repeat(2, 2, 1, 1)
    _, masked_self_weights, _ = block(target_tensor, memory_tensor, causal_mask, None)
    assert torch.all(masked_self_weights[:, :, 0, 1:] < 1e-6)

    previous_weight = block.ffn_weight_2.detach().clone()
    loss_value = block.training_step(target_tensor, memory_tensor, torch.zeros_like(outputs), 0.01)
    assert loss_value >= 0.0
    assert not torch.equal(previous_weight, block.ffn_weight_2.detach())

    print("023_transformer_decoder_block: all examples passed")
