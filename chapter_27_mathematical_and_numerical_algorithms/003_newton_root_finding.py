"""
Newton 求根。
"""


def newton_root(function, derivative, initial_x: float, steps: int, tolerance: float = 1e-10) -> float:
    """用 Newton 迭代求根。"""

    if steps < 0 or tolerance <= 0:
        raise ValueError("参数范围非法")
    x_value = initial_x
    for _ in range(steps):
        slope = derivative(x_value)
        if abs(slope) < tolerance:
            break
        x_value = x_value - function(x_value) / slope
    return x_value


if __name__ == "__main__":
    root = newton_root(lambda x_value: x_value * x_value - 2.0, lambda x_value: 2.0 * x_value, 1.0, 8)
    assert round(root, 6) == 1.414214

    print("003_newton_root_finding: all examples passed")
