"""
RMSProp：对平方梯度做指数滑动平均，缓解 AdaGrad 学习率过快衰减。
"""

from math import sqrt


def rmsprop_update(
    initial_x: float,
    gradients: list[float],
    learning_rate: float,
    beta: float = 0.9,
    epsilon: float = 1e-8,
) -> list[float]:
    """按给定梯度序列执行 RMSProp。"""

    if learning_rate <= 0 or not 0 <= beta < 1 or epsilon <= 0:
        raise ValueError("参数范围非法")
    x_value = initial_x
    second_moment = 0.0
    history = [x_value]
    for gradient in gradients:
        second_moment = beta * second_moment + (1 - beta) * gradient * gradient
        x_value -= learning_rate * gradient / (sqrt(second_moment) + epsilon)
        history.append(x_value)
    return history


if __name__ == "__main__":
    history = rmsprop_update(0.0, [4.0, 2.0, 1.0], 0.1)
    assert len(history) == 4
    assert history[1] < 0.0
    assert history[-1] < history[1]

    print("007_rmsprop: all examples passed")
