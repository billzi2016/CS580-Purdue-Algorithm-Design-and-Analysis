"""
近端梯度：梯度步后接 proximal 映射，常用于 L1 正则。
"""


def soft_threshold(value: float, threshold: float) -> float:
    """L1 正则的 proximal 映射。"""

    if threshold < 0:
        raise ValueError("threshold 不能为负数")
    if value > threshold:
        return value - threshold
    if value < -threshold:
        return value + threshold
    return 0.0


def proximal_gradient(initial_x: float, learning_rate: float, lambda_l1: float, steps: int) -> list[float]:
    """优化 0.5*(x-3)^2 + lambda*|x|。"""

    if learning_rate <= 0 or lambda_l1 < 0 or steps < 0:
        raise ValueError("参数范围非法")
    x_value = initial_x
    history = [x_value]
    for _ in range(steps):
        gradient = x_value - 3.0
        tentative = x_value - learning_rate * gradient
        x_value = soft_threshold(tentative, learning_rate * lambda_l1)
        history.append(x_value)
    return history


if __name__ == "__main__":
    history = proximal_gradient(0.0, 0.5, 0.5, 4)
    assert history[-1] > 1.0
    assert soft_threshold(0.2, 0.3) == 0.0

    print("027_proximal_gradient_method: all examples passed")
