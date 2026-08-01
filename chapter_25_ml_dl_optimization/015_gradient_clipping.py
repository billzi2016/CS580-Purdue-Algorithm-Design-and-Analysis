"""
梯度裁剪：限制梯度过大导致的更新爆炸。
"""

from math import sqrt


def clip_by_value(gradients: list[float], clip_value: float) -> list[float]:
    """把每个梯度限制在 [-clip_value, clip_value]。"""

    if clip_value < 0:
        raise ValueError("clip_value 不能为负数")
    return [max(-clip_value, min(clip_value, gradient)) for gradient in gradients]


def clip_by_global_norm(gradients: list[float], max_norm: float) -> list[float]:
    """按全局 L2 范数缩放整组梯度。"""

    if max_norm < 0:
        raise ValueError("max_norm 不能为负数")
    norm = sqrt(sum(gradient * gradient for gradient in gradients))
    if norm <= max_norm or norm == 0:
        return gradients[:]
    scale = max_norm / norm
    return [gradient * scale for gradient in gradients]


if __name__ == "__main__":
    assert clip_by_value([3.0, -5.0, 1.0], 2.0) == [2.0, -2.0, 1.0]
    clipped = clip_by_global_norm([3.0, 4.0], 2.5)
    assert round(sqrt(sum(value * value for value in clipped)), 6) == 2.5

    print("015_gradient_clipping: all examples passed")
