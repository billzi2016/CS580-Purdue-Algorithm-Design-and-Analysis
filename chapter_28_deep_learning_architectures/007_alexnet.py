"""
文件意图：实现 AlexNet 风格图像分类网络的显式层级结构。
适用场景：理解大卷积核起始层、ReLU、最大池化、dropout 和多层全连接分类器的组合。
核心思想：五个卷积层提取空间特征，adaptive pooling 固定分类器输入尺寸，三层线性层输出类别 logits。
输入输出：输入 RGB NCHW 图像，返回类别 logits；支持一次交叉熵反向传播与手写 SGD 更新。
时间复杂度：由卷积层主导。空间复杂度：O(参数量和中间特征图)。
关键边界：输入必须是 RGB 四维 tensor；本教学实现不加载预训练权重，也不使用 torch.optim。
"""

import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import torch


class AlexNet(torch.nn.Module):
    """显式定义 AlexNet 风格层序列的分类网络。"""

    def __init__(self, class_count: int = 1000, dropout: float = 0.5) -> None:
        """创建 AlexNet 风格网络。

        参数：class_count 为正类别数，dropout 必须在 [0,1) 内。
        返回：无。
        边界情况：非法参数抛出 ValueError。
        关键算法点：每层单独声明，便于审查卷积核、步长、池化和分类器的拓扑。
        """
        super().__init__()
        if class_count <= 0 or not 0 <= dropout < 1:
            raise ValueError("class_count 或 dropout 无效")
        self.features = torch.nn.Sequential(
            torch.nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2), torch.nn.ReLU(), torch.nn.MaxPool2d(3, stride=2),
            torch.nn.Conv2d(64, 192, kernel_size=5, padding=2), torch.nn.ReLU(), torch.nn.MaxPool2d(3, stride=2),
            torch.nn.Conv2d(192, 384, kernel_size=3, padding=1), torch.nn.ReLU(),
            torch.nn.Conv2d(384, 256, kernel_size=3, padding=1), torch.nn.ReLU(),
            torch.nn.Conv2d(256, 256, kernel_size=3, padding=1), torch.nn.ReLU(), torch.nn.MaxPool2d(3, stride=2),
        )
        self.pool = torch.nn.AdaptiveAvgPool2d((6, 6))
        self.classifier = torch.nn.Sequential(
            torch.nn.Dropout(dropout), torch.nn.Linear(256 * 6 * 6, 4096), torch.nn.ReLU(),
            torch.nn.Dropout(dropout), torch.nn.Linear(4096, 4096), torch.nn.ReLU(), torch.nn.Linear(4096, class_count),
        )

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        """返回 RGB 图像批量的类别 logits。

        参数：images 为形状 (batch,3,height,width) 的浮点 tensor。
        返回：形状为 (batch,class_count) 的 logits。
        边界情况：非 RGB NCHW 输入抛出 ValueError；任意正空间尺寸经 adaptive pooling 可进入分类器。
        关键算法点：先提取卷积特征，再固定到 6x6，最后展平交给全连接分类器。
        """
        if images.ndim != 4 or images.shape[1] != 3:
            raise ValueError("AlexNet 需要 RGB NCHW 输入")
        features = self.pool(self.features(images))
        return self.classifier(torch.flatten(features, 1))

    def training_step(self, images: torch.Tensor, labels: torch.Tensor, learning_rate: float) -> float:
        """执行一次交叉熵反向传播和手写 SGD 参数更新。

        参数：images 是 RGB NCHW 批量，labels 是对应类别下标，learning_rate 为正步长。
        返回：更新前的平均交叉熵损失。
        边界情况：标签数、类别范围或学习率无效时抛出 ValueError。
        关键算法点：loss.backward() 生成所有参数梯度；随后在 no_grad 上下文中逐参数执行 param-=lr*grad，避免使用优化器黑箱。
        """
        if learning_rate <= 0 or labels.ndim != 1 or labels.numel() != images.shape[0] or torch.any(labels < 0) or torch.any(labels >= self.classifier[-1].out_features):
            raise ValueError("labels 或 learning_rate 无效")
        self.train()
        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()
        logits = self.forward(images)
        loss = torch.nn.functional.cross_entropy(logits, labels)
        loss.backward()
        with torch.no_grad():
            for parameter in self.parameters():
                if parameter.grad is not None:
                    parameter -= learning_rate * parameter.grad
        return float(loss.detach())


if __name__ == "__main__":
    model = AlexNet(class_count=4, dropout=0.0)
    images = torch.zeros((1, 3, 224, 224))
    labels = torch.tensor([2])
    model.eval()
    assert model(images).shape == (1, 4)
    before = model.classifier[-1].weight.detach().clone()
    assert model.training_step(images, labels, 0.001) >= 0.0
    assert not torch.equal(before, model.classifier[-1].weight.detach())
    print("007_alexnet: all examples passed")
