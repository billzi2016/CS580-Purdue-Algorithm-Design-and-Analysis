"""
文件意图：实现 Vision Transformer 的 patch embedding。
适用场景：把二维图像切分为 patch 序列，再送入 Transformer。
核心思想：按固定 patch 大小切块，拉平成向量后通过线性层映射到嵌入空间。
输入输出：输入为 (batch,channels,height,width)，输出为 (batch,num_patches,embed_dim)。
时间复杂度：O(batch*num_patches*patch_area*embed_dim)。
空间复杂度：O(batch*num_patches*embed_dim)。
关键边界情况：图像高宽必须能被 patch 大小整除；patch 尺寸必须为正。
"""

import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import torch


class VisionTransformerPatchEmbedding(torch.nn.Module):
    """手写图像 patch 切分与嵌入。"""

    def __init__(self, in_channels: int, patch_size: int, embed_dim: int) -> None:
        """初始化 patch 投影参数。"""
        super().__init__()
        if in_channels <= 0 or patch_size <= 0 or embed_dim <= 0:
            raise ValueError("in_channels、patch_size、embed_dim 必须为正")

        self.in_channels = in_channels
        self.patch_size = patch_size
        self.embed_dim = embed_dim
        self.patch_area = in_channels * patch_size * patch_size

        self.projection_weight = torch.nn.Parameter(
            torch.randn(self.patch_area, embed_dim) * 0.1
        )
        self.projection_bias = torch.nn.Parameter(torch.zeros(embed_dim))

    def _extract_patches(self, images: torch.Tensor) -> torch.Tensor:
        """手写提取所有 patch，并保持扫描顺序稳定。"""
        if images.ndim != 4 or images.shape[1] != self.in_channels:
            raise ValueError("images 形状必须为 (batch,channels,height,width)")
        if images.shape[2] % self.patch_size != 0 or images.shape[3] % self.patch_size != 0:
            raise ValueError("图像高宽必须能被 patch_size 整除")

        batch_size, _, height, width = images.shape
        patches: list[torch.Tensor] = []

        for top in range(0, height, self.patch_size):
            for left in range(0, width, self.patch_size):
                patch = images[
                    :,
                    :,
                    top : top + self.patch_size,
                    left : left + self.patch_size,
                ]
                patches.append(patch.reshape(batch_size, self.patch_area))

        return torch.stack(patches, dim=1)

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        """返回 patch 序列嵌入。"""
        patches = self._extract_patches(images)
        return patches @ self.projection_weight + self.projection_bias

    def training_step(self, images: torch.Tensor, target: torch.Tensor, learning_rate: float) -> float:
        """执行一次 patch embedding 训练步。"""
        if learning_rate <= 0:
            raise ValueError("learning_rate 必须为正")

        for parameter in self.parameters():
            if parameter.grad is not None:
                parameter.grad.zero_()

        output = self.forward(images)
        if output.shape != target.shape:
            raise ValueError("target 形状必须与输出一致")

        loss = torch.mean((output - target) ** 2)
        loss.backward()

        with torch.no_grad():
            for parameter in self.parameters():
                parameter -= learning_rate * parameter.grad

        return float(loss.detach())


if __name__ == "__main__":
    torch.manual_seed(29)

    module = VisionTransformerPatchEmbedding(3, 2, 8)
    image_tensor = torch.arange(0, 3 * 4 * 4, dtype=torch.float32).reshape(1, 3, 4, 4)
    patch_tensor = module._extract_patches(image_tensor)
    assert patch_tensor.shape == (1, 4, 12)

    output_tensor = module(image_tensor)
    assert output_tensor.shape == (1, 4, 8)

    random_images = torch.randn((2, 3, 4, 4))
    random_outputs = module(random_images)
    previous_weight = module.projection_weight.detach().clone()
    loss_value = module.training_step(random_images, torch.zeros_like(random_outputs), 0.01)
    assert loss_value >= 0.0
    assert not torch.equal(previous_weight, module.projection_weight.detach())

    print("024_vision_transformer_patch_embedding: all examples passed")
