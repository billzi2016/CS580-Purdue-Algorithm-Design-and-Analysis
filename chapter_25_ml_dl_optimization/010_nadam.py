"""
Nadam：把 Nesterov 动量思想并入 Adam。
"""

from math import sqrt


def nadam_update(
    initial_x: float,
    gradients: list[float],
    learning_rate: float,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-8,
) -> list[float]:
    """执行 Nadam 更新。"""

    if learning_rate <= 0:
        raise ValueError("learning_rate 必须为正数")
    x_value = initial_x
    first_moment = 0.0
    second_moment = 0.0
    history = [x_value]
    for step, gradient in enumerate(gradients, start=1):
        first_moment = beta1 * first_moment + (1 - beta1) * gradient
        second_moment = beta2 * second_moment + (1 - beta2) * gradient * gradient
        first_hat = first_moment / (1 - beta1**step)
        second_hat = second_moment / (1 - beta2**step)
        nesterov_term = beta1 * first_hat + (1 - beta1) * gradient / (1 - beta1**step)
        x_value -= learning_rate * nesterov_term / (sqrt(second_hat) + epsilon)
        history.append(x_value)
    return history


if __name__ == "__main__":
    history = nadam_update(0.0, [3.0, 2.0, 1.0], 0.1)
    assert len(history) == 4
    assert history[-1] < history[1]

    print("010_nadam: all examples passed")
