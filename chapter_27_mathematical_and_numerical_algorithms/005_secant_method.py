"""
割线法求根。
"""


def secant_root(function, x0: float, x1: float, steps: int, tolerance: float = 1e-10) -> float:
    """用两点割线替代导数。"""

    if steps < 0 or tolerance <= 0:
        raise ValueError("参数范围非法")
    for _ in range(steps):
        f0 = function(x0)
        f1 = function(x1)
        if abs(f1 - f0) < tolerance:
            break
        x0, x1 = x1, x1 - f1 * (x1 - x0) / (f1 - f0)
    return x1


if __name__ == "__main__":
    root = secant_root(lambda x_value: x_value * x_value - 2.0, 1.0, 2.0, 8)
    assert round(root, 6) == 1.414214

    print("005_secant_method: all examples passed")
