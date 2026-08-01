"""
AMSGrad：在 Adam 上对二阶矩取历史最大值，增强收敛稳定性。
"""

from math import sqrt


def amsgrad_update(
    initial_x: float,
    gradients: list[float],
    learning_rate: float,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-8,
) -> tuple[list[float], list[float]]:
    """返回参数轨迹和历史最大二阶矩轨迹。"""

    if learning_rate <= 0:
        raise ValueError("learning_rate 必须为正数")
    x_value = initial_x
    first_moment = 0.0
    second_moment = 0.0
    max_second = 0.0
    history = [x_value]
    max_history = [max_second]
    for step, gradient in enumerate(gradients, start=1):
        first_moment = beta1 * first_moment + (1 - beta1) * gradient
        second_moment = beta2 * second_moment + (1 - beta2) * gradient * gradient
        max_second = max(max_second, second_moment)
        first_hat = first_moment / (1 - beta1**step)
        x_value -= learning_rate * first_hat / (sqrt(max_second) + epsilon)
        history.append(x_value)
        max_history.append(max_second)
    return history, max_history


if __name__ == "__main__":
    params, maxima = amsgrad_update(0.0, [3.0, 2.0, 1.0], 0.1)
    assert len(params) == 4
    assert maxima[1] <= maxima[2] <= maxima[3]

    print("011_amsgrad: all examples passed")
