"""
文件意图：手写实现单隐层多层感知机（MLP）的前向与交叉熵梯度训练。
适用场景：小型多分类问题，理解线性层、ReLU、softmax 与反向传播的组合。
核心思想：xW1+b1 经 ReLU 后接 xW2+b2；softmax 交叉熵梯度从输出层逐层链式回传。
输入输出：输入批量特征与类别标签，支持 predict 与 train_step。
时间复杂度：每步 O(batch*(input*hidden+hidden*classes))。空间复杂度：O(参数量)。
关键边界：标签必须在类别范围内；本基础版不含 dropout、批归一化或高级优化器。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class MultilayerPerceptron:
    """使用手写梯度更新的单隐层 ReLU 多分类 MLP。"""

    def __init__(self, input_size: int, hidden_size: int, class_count: int, seed: int = 0) -> None:
        """按小随机值初始化两层参数。

        参数：input_size、hidden_size、class_count 必须为正；seed 控制初始化可复现。
        返回：无。
        边界情况：非正维度抛出 ValueError。
        关键算法点：参数是普通 tensor，反向梯度由 train_step 显式计算而非 autograd 或高层模块。
        """
        if input_size <= 0 or hidden_size <= 0 or class_count <= 0:
            raise ValueError("网络维度必须为正")
        generator = torch.Generator().manual_seed(seed)
        self.weight_input_hidden = torch.randn(input_size, hidden_size, generator=generator, dtype=torch.float64) * 0.1
        self.bias_hidden = torch.zeros(hidden_size, dtype=torch.float64)
        self.weight_hidden_output = torch.randn(hidden_size, class_count, generator=generator, dtype=torch.float64) * 0.1
        self.bias_output = torch.zeros(class_count, dtype=torch.float64)

    def _forward(self, features: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """计算隐藏线性值、ReLU 激活和输出 logits。"""
        hidden_linear = features @ self.weight_input_hidden + self.bias_hidden
        hidden = torch.clamp(hidden_linear, min=0.0)
        logits = hidden @ self.weight_hidden_output + self.bias_output
        return hidden_linear, hidden, logits

    def predict(self, features: torch.Tensor) -> torch.Tensor:
        """返回每个样本 logits 最大的类别下标。

        参数：features 形状为 (batch,input_size)。
        返回：形状为 (batch,) 的整数类别 tensor。
        边界情况：特征维度不匹配抛出 ValueError。
        关键算法点：预测只需前向计算，不需要 softmax，因为 argmax 在 softmax 前后不变。
        """
        if features.ndim != 2 or features.shape[1] != self.weight_input_hidden.shape[0]:
            raise ValueError("features 形状不匹配")
        _, _, logits = self._forward(features.to(torch.float64))
        return torch.argmax(logits, dim=1)

    def train_step(self, features: torch.Tensor, labels: torch.Tensor, learning_rate: float) -> float:
        """执行一次批量交叉熵梯度下降，并返回更新前平均损失。

        参数：features 为二维批量，labels 为类别下标，learning_rate 为正数。
        返回：更新前的平均 softmax 交叉熵。
        边界情况：空批量、标签越界、形状不匹配或非正步长抛出 ValueError。
        关键算法点：输出梯度是 (softmax-one_hot)/batch，随后显式应用矩阵链式法则。
        """
        if features.ndim != 2 or labels.ndim != 1 or features.shape[0] == 0 or labels.numel() != features.shape[0] or features.shape[1] != self.weight_input_hidden.shape[0] or learning_rate <= 0:
            raise ValueError("训练数据形状或学习率无效")
        if torch.any(labels < 0) or torch.any(labels >= self.bias_output.numel()):
            raise ValueError("labels 包含无效类别")
        inputs = features.to(torch.float64)
        hidden_linear, hidden, logits = self._forward(inputs)
        shifted = logits - torch.max(logits, dim=1, keepdim=True).values
        probabilities = torch.exp(shifted)
        probabilities /= torch.sum(probabilities, dim=1, keepdim=True)
        batch_size = inputs.shape[0]
        loss = -torch.log(probabilities[torch.arange(batch_size), labels]).mean()
        output_gradient = probabilities.clone()
        output_gradient[torch.arange(batch_size), labels] -= 1.0
        output_gradient /= batch_size
        gradient_weight_hidden_output = hidden.T @ output_gradient
        gradient_bias_output = torch.sum(output_gradient, dim=0)
        hidden_gradient = output_gradient @ self.weight_hidden_output.T
        hidden_gradient[hidden_linear <= 0.0] = 0.0
        gradient_weight_input_hidden = inputs.T @ hidden_gradient
        gradient_bias_hidden = torch.sum(hidden_gradient, dim=0)
        self.weight_hidden_output -= learning_rate * gradient_weight_hidden_output
        self.bias_output -= learning_rate * gradient_bias_output
        self.weight_input_hidden -= learning_rate * gradient_weight_input_hidden
        self.bias_hidden -= learning_rate * gradient_bias_hidden
        return float(loss)


if __name__ == "__main__":
    features = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    labels = torch.tensor([0, 1, 1, 1])
    model = MultilayerPerceptron(2, 4, 2, seed=4)
    initial_loss = model.train_step(features, labels, 0.5)
    final_loss = initial_loss
    for _ in range(200):
        final_loss = model.train_step(features, labels, 0.5)
    assert final_loss < initial_loss
    assert torch.equal(model.predict(features), labels)
    print("002_multilayer_perceptron: all examples passed")
