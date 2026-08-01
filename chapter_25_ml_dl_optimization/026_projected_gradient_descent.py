"""
投影梯度下降：每次梯度步后投影回可行域。
"""


def project_to_box(value: float, lower: float, upper: float) -> float:
    """投影到闭区间 [lower, upper]。"""

    if lower > upper:
        raise ValueError("lower 不能大于 upper")
    return max(lower, min(upper, value))


def projected_gradient_descent(initial_x: float, learning_rate: float, steps: int, lower: float, upper: float) -> list[float]:
    """优化 f(x)=0.5*(x-3)^2，并限制 x 落在区间内。"""

    if learning_rate <= 0 or steps < 0:
        raise ValueError("参数范围非法")
    x_value = initial_x
    history = [x_value]
    for _ in range(steps):
        gradient = x_value - 3.0
        x_value = project_to_box(x_value - learning_rate * gradient, lower, upper)
        history.append(x_value)
    return history


if __name__ == "__main__":
    history = projected_gradient_descent(0.0, 1.0, 3, lower=0.0, upper=2.0)
    assert history[-1] == 2.0
    assert project_to_box(-1.0, 0.0, 2.0) == 0.0

    print("026_projected_gradient_descent: all examples passed")
