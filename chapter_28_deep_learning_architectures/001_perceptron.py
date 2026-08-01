"""
文件意图：手写实现二分类感知机及其在线更新规则。
适用场景：线性可分二分类的基础教学实验，也是理解线性分类器与梯度式训练的起点。
核心思想：预测使用 w·x+b 的符号；误分类样本用 y*x 和 y 更新权重与偏置。
输入输出：输入二维样本与 {-1,1} 标签，训练后可对新样本预测。
时间复杂度：O(epochs * n * d)。空间复杂度：O(d)。
关键边界：标签必须为 -1 或 1；空训练集不修改参数；线性不可分数据不保证在轮数内收敛。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class Perceptron:
    """使用手写误分类更新的二分类感知机。"""

    def __init__(self, feature_count: int, learning_rate: float = 1.0) -> None:
        """创建零初始化感知机。

        参数：feature_count 是正特征维度，learning_rate 是正更新步长。
        返回：无。
        边界情况：非正维度或步长抛出 ValueError。
        关键算法点：参数是普通 tensor，不使用高层网络层或优化器。
        """
        if feature_count <= 0 or learning_rate <= 0:
            raise ValueError("feature_count 和 learning_rate 必须为正")
        self.weights = torch.zeros(feature_count, dtype=torch.float64)
        self.bias = torch.tensor(0.0, dtype=torch.float64)
        self.learning_rate = learning_rate

    def score(self, features: torch.Tensor) -> float:
        """计算样本线性得分。

        参数：features 是一维、长度等于特征维度的 tensor。
        返回：w·x+b 的浮点值。
        边界情况：维度不匹配抛出 ValueError。
        关键算法点：点积和偏置构成感知机的线性决策函数。
        """
        if features.ndim != 1 or features.numel() != self.weights.numel():
            raise ValueError("features 维度不匹配")
        return float(torch.dot(self.weights, features.to(torch.float64)) + self.bias)

    def predict(self, features: torch.Tensor) -> int:
        """按线性得分符号预测 -1 或 1。

        参数：features 为有效特征向量。
        返回：得分非负时为 1，否则为 -1。
        边界情况：决策边界上的样本归入正类。
        关键算法点：二分类符号函数把实数得分转为离散标签。
        """
        return 1 if self.score(features) >= 0 else -1

    def fit(self, features: torch.Tensor, labels: torch.Tensor, epochs: int) -> int:
        """按样本顺序训练最多 epochs 轮，并返回实际训练轮数。

        参数：features 形状为 (n,d)，labels 形状为 (n,)，元素必须为 -1 或 1；epochs 为非负整数。
        返回：训练轮数；若某轮无误分类则提前停止。
        边界情况：空数据返回零；形状、标签或轮数无效时抛出 ValueError。
        关键算法点：只有 y*(w·x+b)<=0 的误分类或边界样本才触发 y*x、y 更新。
        """
        if features.ndim != 2 or features.shape[1] != self.weights.numel() or labels.ndim != 1 or labels.numel() != features.shape[0] or epochs < 0:
            raise ValueError("训练数据形状或 epochs 无效")
        if any(int(label) not in (-1, 1) for label in labels):
            raise ValueError("labels 必须只包含 -1 和 1")
        for epoch in range(epochs):
            mistakes = 0
            for row, label_tensor in zip(features, labels):
                label = int(label_tensor)
                row = row.to(torch.float64)
                if label * self.score(row) <= 0:
                    self.weights += self.learning_rate * label * row
                    self.bias += self.learning_rate * label
                    mistakes += 1
            if mistakes == 0:
                return epoch + 1
        return epochs


if __name__ == "__main__":
    data = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    labels = torch.tensor([-1, -1, -1, 1])
    model = Perceptron(2)
    assert model.fit(data, labels, 20) <= 20
    assert [model.predict(row) for row in data] == [-1, -1, -1, 1]
    print("001_perceptron: all examples passed")
