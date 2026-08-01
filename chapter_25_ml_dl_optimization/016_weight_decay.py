"""
权重衰减：在每一步更新前或更新时缩小参数幅度。
"""


def decoupled_weight_decay(weight: float, learning_rate: float, decay: float) -> float:
    """AdamW 风格：直接衰减参数。"""

    if learning_rate < 0 or decay < 0:
        raise ValueError("learning_rate 和 decay 不能为负数")
    return weight * (1 - learning_rate * decay)


def l2_penalty_gradient(weight: float, decay: float) -> float:
    """L2 正则项 0.5*decay*w^2 对参数的梯度。"""

    if decay < 0:
        raise ValueError("decay 不能为负数")
    return decay * weight


if __name__ == "__main__":
    assert decoupled_weight_decay(2.0, 0.1, 0.5) == 1.9
    assert abs(l2_penalty_gradient(3.0, 0.2) - 0.6) < 1e-12

    print("016_weight_decay: all examples passed")
