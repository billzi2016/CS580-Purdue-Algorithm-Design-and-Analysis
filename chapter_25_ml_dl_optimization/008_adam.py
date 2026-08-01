"""
Adam：一阶矩和二阶矩的偏差校正自适应优化器。
"""

from math import sqrt


def adam_update(
    initial_x: float,
    gradients: list[float],
    learning_rate: float,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-8,
) -> list[float]:
    """按给定梯度序列执行 Adam。"""

    if learning_rate <= 0 or not 0 <= beta1 < 1 or not 0 <= beta2 < 1 or epsilon <= 0:
        raise ValueError("参数范围非法")
    x_value = initial_x
    first_moment = 0.0
    second_moment = 0.0
    history = [x_value]
    for step, gradient in enumerate(gradients, start=1):
        first_moment = beta1 * first_moment + (1 - beta1) * gradient
        second_moment = beta2 * second_moment + (1 - beta2) * gradient * gradient
        first_hat = first_moment / (1 - beta1**step)
        second_hat = second_moment / (1 - beta2**step)
        x_value -= learning_rate * first_hat / (sqrt(second_hat) + epsilon)
        history.append(x_value)
    return history


if __name__ == "__main__":
    history = adam_update(0.0, [4.0, 2.0, 1.0], 0.1)
    assert len(history) == 4
    assert history[1] < 0.0
    assert history[-1] < history[1]

    print("008_adam: all examples passed")
