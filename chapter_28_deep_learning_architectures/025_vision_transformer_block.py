"""
文件意图：实现基础版 Vision Transformer block 及其训练一步。
适用场景：基于 patch 序列进行全局视觉建模。
核心思想：对 patch token 做多头自注意力和前馈网络，并保留残差连接与层归一化。
输入输出：输入输出均为 (batch,num_tokens,embed_dim) 张量。
时间复杂度：O(batch*num_tokens*num_tokens*embed_dim + batch*num_tokens*embed_dim*mlp_dim)。
空间复杂度：O(batch*heads*num_tokens*num_tokens)。
关键边界情况：embed_dim 必须能被头数整除；输入必须是三维张量。
"""

import math
import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class VisionTransformerBlock(torch.nn.Module):
    """手写 ViT block。"""

    def __init__(self, embed_dim: int, num_heads: int, mlp_dim: int) -> None:
        """初始化注意力和 MLP 参数。"""
        super().__init__()
        if embed_dim <= 0 or num_heads <= 0 or mlp_dim <= 0:
            raise ValueError("embed_dim、num_heads、mlp_dim 必须为正")
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

        self.mlp_weight_1 = torch.nn.Parameter(torch.randn(embed_dim, mlp_dim) * 0.1)
        self.mlp_bias_1 = torch.nn.Parameter(torch.zeros(mlp_dim))
        self.mlp_weight_2 = torch.nn.Parameter(torch.randn(mlp_dim, embed_dim) * 0.1)
        self.mlp_bias_2 = torch.nn.Parameter(torch.zeros(embed_dim))

    def _layer_norm(self, tensor: torch.Tensor, epsilon: float = 1e-5) -> torch.Tensor:
        """对最后一维做层归一化。"""
        mean = tensor.mean(dim=-1, keepdim=True)
        variance = ((tensor - mean) ** 2).mean(dim=-1, keepdim=True)
        return (tensor - mean) / torch.sqrt(variance + epsilon)

    def _project(self, tokens: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor) -> torch.Tensor:
        """投影到多头表示。"""
        batch_size, num_tokens, _ = tokens.shape
        projected = tokens @ weight + bias
        projected = projected.reshape(batch_size, num_tokens, self.num_heads, self.head_dim)
        return projected.permute(0, 2, 1, 3)

    def forward(self, tokens: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """返回 block 输出和注意力权重。"""
        if tokens.ndim != 3 or tokens.shape[2] != self.embed_dim:
            raise ValueError("tokens 形状必须为 (batch,num_tokens,embed_dim)")

        query = self._project(tokens, self.query_weight, self.query_bias)
        key = self._project(tokens, self.key_weight, self.key_bias)
        value = self._project(tokens, self.value_weight, self.value_bias)

        scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(self.head_dim)
        attention_weights = torch.softmax(scores, dim=-1)
        attended = torch.matmul(attention_weights, value)
        attended = attended.permute(0, 2, 1, 3).reshape(tokens.shape[0], tokens.shape[1], self.embed_dim)
        attention_output = attended @ self.output_weight + self.output_bias

        residual = self._layer_norm(tokens + attention_output)
        mlp_output = torch.relu(residual @ self.mlp_weight_1 + self.mlp_bias_1)
        mlp_output = mlp_output @ self.mlp_weight_2 + self.mlp_bias_2
        return self._layer_norm(residual + mlp_output), attention_weights

    def training_step(self, tokens: torch.Tensor, target: torch.Tensor, learning_rate: float) -> float:
        """执行一次 ViT block 训练步。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        output, _ = self.forward(tokens)
        if output.shape != target.shape:
            raise ValueError("target 形状必须与输出一致")

        loss = torch.mean((output - target) ** 2)
        loss.backward()

        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(31)

    block = VisionTransformerBlock(8, 2, 16)
    token_tensor = torch.randn((2, 5, 8))
    output_tensor, attention_tensor = block(token_tensor)
    assert output_tensor.shape == (2, 5, 8)
    assert attention_tensor.shape == (2, 2, 5, 5)
    assert torch.allclose(attention_tensor.sum(dim=-1), torch.ones((2, 2, 5)), atol=1e-5)

    previous_weight = block.mlp_weight_2.detach().clone()
    loss_value = block.training_step(token_tensor, torch.zeros_like(output_tensor), 0.01)
    assert loss_value >= 0.0
    assert not torch.equal(previous_weight, block.mlp_weight_2.detach())

    print("025_vision_transformer_block: all examples passed")
