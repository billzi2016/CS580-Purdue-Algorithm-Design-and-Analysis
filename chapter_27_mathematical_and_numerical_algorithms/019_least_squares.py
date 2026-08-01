"""
最小二乘：用正规方程拟合 y = a*x + b。
"""


def linear_least_squares(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """返回斜率和截距。"""

    if len(xs) != len(ys) or not xs:
        raise ValueError("xs 和 ys 必须等长且非空")
    n_value = len(xs)
    sum_x = sum(xs)
    sum_y = sum(ys)
    sum_xx = sum(x_value * x_value for x_value in xs)
    sum_xy = sum(x_value * y_value for x_value, y_value in zip(xs, ys, strict=True))
    denominator = n_value * sum_xx - sum_x * sum_x
    if denominator == 0:
        raise ValueError("样本 x 不足以拟合直线")
    slope = (n_value * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n_value
    return slope, intercept


if __name__ == "__main__":
    slope, intercept = linear_least_squares([1.0, 2.0, 3.0], [2.0, 4.0, 6.0])
    assert round(slope, 6) == 2.0
    assert round(intercept, 6) == 0.0

    print("019_least_squares: all examples passed")
