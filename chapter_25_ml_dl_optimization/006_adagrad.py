"""
AdaGrad：按历史平方梯度缩放学习率。
"""

from math import sqrt


def adagrad_update(
    initial_x: float,
    gradients: list[float],
    learning_rate: float,
    epsilon: float = 1e-8,
) -> list[float]:
    """按给定梯度序列执行 AdaGrad。"""

    if learning_rate <= 0 or epsilon <= 0:
        raise ValueError("learning_rate 和 epsilon 必须为正")
    x_value = initial_x
    accumulator = 0.0
    history = [x_value]
    for gradient in gradients:
        accumulator += gradient * gradient
        x_value -= learning_rate * gradient / (sqrt(accumulator) + epsilon)
        history.append(x_value)
    return history


if __name__ == "__main__":
    history = adagrad_update(0.0, [4.0, 2.0, 1.0], 1.0)
    assert len(history) == 4
    assert history[1] == -0.9999999975 or history[1] < 0.0
    assert abs(history[-1]) > abs(history[-2])

    print("006_adagrad: all examples passed")
