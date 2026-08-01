"""
文件意图：实现基础图卷积层（GCN layer）及其训练一步。
适用场景：在图结构数据上聚合邻居特征进行节点表示学习。
核心思想：先加入自环，再对邻接矩阵做对称归一化，最后乘以节点特征和可学习权重。
输入输出：输入邻接矩阵和节点特征，输出更新后的节点特征。
时间复杂度：O(num_nodes^2*feature_dim + num_nodes*in_dim*out_dim)。
空间复杂度：O(num_nodes^2 + num_nodes*out_dim)。
关键边界情况：邻接矩阵必须为方阵；节点数需与特征矩阵第一维一致。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class GraphConvolutionLayer(torch.nn.Module):
    """手写基础 GCN 层。"""

    def __init__(self, input_dim: int, output_dim: int) -> None:
        """初始化线性映射参数。"""
        super().__init__()
        if input_dim <= 0 or output_dim <= 0:
            raise ValueError("input_dim 和 output_dim 必须为正")

        self.input_dim = input_dim
        self.output_dim = output_dim
        self.weight = torch.nn.Parameter(torch.randn(input_dim, output_dim) * 0.1)
        self.bias = torch.nn.Parameter(torch.zeros(output_dim))

    def forward(self, adjacency: torch.Tensor, features: torch.Tensor) -> torch.Tensor:
        """执行一次图卷积。"""
        if adjacency.ndim != 2 or adjacency.shape[0] != adjacency.shape[1]:
            raise ValueError("adjacency 必须是方阵")
        if features.ndim != 2 or features.shape[0] != adjacency.shape[0] or features.shape[1] != self.input_dim:
            raise ValueError("features 形状必须为 (num_nodes,input_dim)")

        identity = torch.eye(adjacency.shape[0], dtype=adjacency.dtype, device=adjacency.device)
        adjacency_with_self_loop = adjacency + identity
        degree = adjacency_with_self_loop.sum(dim=1)
        degree_inverse_sqrt = torch.pow(degree, -0.5)
        degree_inverse_sqrt[torch.isinf(degree_inverse_sqrt)] = 0.0
        normalized = degree_inverse_sqrt.unsqueeze(1) * adjacency_with_self_loop * degree_inverse_sqrt.unsqueeze(0)
        return normalized @ features @ self.weight + self.bias

    def training_step(
        self, adjacency: torch.Tensor, features: torch.Tensor, target: torch.Tensor, learning_rate: float
    ) -> float:
        """执行一次 GCN 层训练步。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        output = self.forward(adjacency, features)
        if output.shape != target.shape:
            raise ValueError("target 形状必须与输出一致")

        loss = torch.mean((output - target) ** 2)
        loss.backward()

        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(59)

    layer = GraphConvolutionLayer(3, 2)
    adjacency_matrix = torch.tensor(
        [[0.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]],
        dtype=torch.float32,
    )
    feature_matrix = torch.randn((3, 3))
    output_matrix = layer(adjacency_matrix, feature_matrix)
    assert output_matrix.shape == (3, 2)

    isolated_output = layer(torch.zeros((1, 1)), torch.ones((1, 3)))
    assert isolated_output.shape == (1, 2)

    previous_weight = layer.weight.detach().clone()
    loss_value = layer.training_step(adjacency_matrix, feature_matrix, torch.zeros_like(output_matrix), 0.01)
    assert loss_value >= 0.0
    assert not torch.equal(previous_weight, layer.weight.detach())

    print("031_graph_convolution_layer: all examples passed")
