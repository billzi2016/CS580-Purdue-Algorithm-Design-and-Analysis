"""
AdamW：把权重衰减从梯度项中解耦。
"""

from math import sqrt


def adamw_update(
    initial_x: float,
    gradients: list[float],
    learning_rate: float,
    weight_decay: float,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-8,
) -> list[float]:
    """执行 AdamW 更新。"""

    if learning_rate <= 0 or weight_decay < 0:
        raise ValueError("learning_rate 必须为正，weight_decay 不能为负")
    x_value = initial_x
    first_moment = 0.0
    second_moment = 0.0
    history = [x_value]
    for step, gradient in enumerate(gradients, start=1):
        first_moment = beta1 * first_moment + (1 - beta1) * gradient
        second_moment = beta2 * second_moment + (1 - beta2) * gradient * gradient
        first_hat = first_moment / (1 - beta1**step)
        second_hat = second_moment / (1 - beta2**step)
        x_value *= 1 - learning_rate * weight_decay
        x_value -= learning_rate * first_hat / (sqrt(second_hat) + epsilon)
        history.append(x_value)
    return history


if __name__ == "__main__":
    no_decay = adamw_update(1.0, [0.5, 0.5], 0.1, 0.0)
    with_decay = adamw_update(1.0, [0.5, 0.5], 0.1, 0.1)
    assert len(with_decay) == 3
    assert with_decay[-1] < no_decay[-1]

    print("009_adamw: all examples passed")
