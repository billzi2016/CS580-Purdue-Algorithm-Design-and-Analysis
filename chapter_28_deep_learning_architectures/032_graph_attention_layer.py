"""
文件意图：实现基础图注意力层（GAT layer）及其训练一步。
适用场景：在图结构数据上为不同邻居分配不同的重要性权重。
核心思想：先对节点特征做线性投影，再对边两端特征拼接打分，最后按邻域 softmax 聚合。
输入输出：输入邻接矩阵和节点特征，输出更新后的节点表征与注意力矩阵。
时间复杂度：O(num_nodes^2*out_dim)。
空间复杂度：O(num_nodes^2 + num_nodes*out_dim)。
关键边界情况：邻接矩阵必须是方阵；本基础版实现单头 GAT。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class GraphAttentionLayer(torch.nn.Module):
    """手写单头 GAT 层。"""

    def __init__(self, input_dim: int, output_dim: int, negative_slope: float = 0.2) -> None:
        """初始化线性投影和边打分参数。"""
        super().__init__()
        if input_dim <= 0 or output_dim <= 0:
            raise ValueError("input_dim 和 output_dim 必须为正")

        self.input_dim = input_dim
        self.output_dim = output_dim
        self.negative_slope = negative_slope
        self.weight = torch.nn.Parameter(torch.randn(input_dim, output_dim) * 0.1)
        self.attention_vector = torch.nn.Parameter(torch.randn(2 * output_dim) * 0.1)

    def forward(self, adjacency: torch.Tensor, features: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """执行一次图注意力聚合。"""
        if adjacency.ndim != 2 or adjacency.shape[0] != adjacency.shape[1]:
            raise ValueError("adjacency 必须是方阵")
        if features.ndim != 2 or features.shape[0] != adjacency.shape[0] or features.shape[1] != self.input_dim:
            raise ValueError("features 形状必须为 (num_nodes,input_dim)")

        num_nodes = adjacency.shape[0]
        projected = features @ self.weight
        scores = torch.full((num_nodes, num_nodes), -1e9, dtype=features.dtype, device=features.device)

        for source_index in range(num_nodes):
            for target_index in range(num_nodes):
                if adjacency[source_index, target_index] > 0 or source_index == target_index:
                    concatenated = torch.cat((projected[source_index], projected[target_index]), dim=0)
                    raw_score = torch.dot(concatenated, self.attention_vector)
                    scores[source_index, target_index] = torch.where(
                        raw_score >= 0,
                        raw_score,
                        self.negative_slope * raw_score,
                    )

        attention_weights = torch.softmax(scores, dim=1)
        return attention_weights @ projected, attention_weights

    def training_step(
        self, adjacency: torch.Tensor, features: torch.Tensor, target: torch.Tensor, learning_rate: float
    ) -> float:
        """执行一次 GAT 层训练步。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        output, _ = self.forward(adjacency, features)
        if output.shape != target.shape:
            raise ValueError("target 形状必须与输出一致")

        loss = torch.mean((output - target) ** 2)
        loss.backward()

        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(61)

    layer = GraphAttentionLayer(3, 2)
    adjacency_matrix = torch.tensor(
        [[0.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]],
        dtype=torch.float32,
    )
    feature_matrix = torch.randn((3, 3))
    output_matrix, attention_matrix = layer(adjacency_matrix, feature_matrix)
    assert output_matrix.shape == (3, 2)
    assert attention_matrix.shape == (3, 3)
    assert torch.allclose(attention_matrix.sum(dim=1), torch.ones(3), atol=1e-5)

    self_only_output, self_only_attention = layer(torch.zeros((1, 1)), torch.ones((1, 3)))
    assert self_only_output.shape == (1, 2)
    assert torch.allclose(self_only_attention, torch.ones((1, 1)), atol=1e-6)

    previous_weight = layer.weight.detach().clone()
    loss_value = layer.training_step(adjacency_matrix, feature_matrix, torch.zeros_like(output_matrix), 0.01)
    assert loss_value >= 0.0
    assert not torch.equal(previous_weight, layer.weight.detach())

    print("032_graph_attention_layer: all examples passed")
