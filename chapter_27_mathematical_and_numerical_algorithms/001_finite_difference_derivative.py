"""
有限差分求导：用函数值近似一阶导数。
"""


def forward_difference(function, x_value: float, step: float) -> float:
    """前向差分。"""

    if step <= 0:
        raise ValueError("step 必须为正数")
    return (function(x_value + step) - function(x_value)) / step


def central_difference(function, x_value: float, step: float) -> float:
    """中心差分，通常比前向差分更精确。"""

    if step <= 0:
        raise ValueError("step 必须为正数")
    return (function(x_value + step) - function(x_value - step)) / (2 * step)


if __name__ == "__main__":
    square = lambda x_value: x_value * x_value
    assert round(forward_difference(square, 3.0, 1e-4), 3) == 6.0
    assert round(central_difference(square, 3.0, 1e-4), 6) == 6.0

    print("001_finite_difference_derivative: all examples passed")
