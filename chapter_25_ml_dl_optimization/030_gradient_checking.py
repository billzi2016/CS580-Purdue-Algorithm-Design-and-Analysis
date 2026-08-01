"""
数值梯度检查：比较解析梯度和有限差分梯度。
"""


def scalar_function(x_value: float) -> float:
    return x_value**3 - 2 * x_value


def scalar_gradient(x_value: float) -> float:
    return 3 * x_value * x_value - 2


def finite_difference_gradient(
    function, x_value: float, epsilon: float = 1e-6
) -> float:
    """中心差分近似梯度。"""

    if epsilon <= 0:
        raise ValueError("epsilon 必须为正数")
    return (function(x_value + epsilon) - function(x_value - epsilon)) / (2 * epsilon)


def gradient_check(
    function, gradient_function, x_value: float, tolerance: float = 1e-4
) -> bool:
    """判断解析梯度与数值梯度是否足够接近。"""

    numerical = finite_difference_gradient(function, x_value)
    analytic = gradient_function(x_value)
    return abs(numerical - analytic) <= tolerance


if __name__ == "__main__":
    assert gradient_check(scalar_function, scalar_gradient, 1.5)
    assert not gradient_check(scalar_function, lambda x_value: 0.0, 1.5)

    print("030_gradient_checking: all examples passed")
