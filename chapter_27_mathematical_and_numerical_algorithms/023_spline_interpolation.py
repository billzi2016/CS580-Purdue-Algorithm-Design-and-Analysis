"""
样条插值基础：自然三次样条的一维求值。
"""


def natural_cubic_spline_coefficients(
    xs: list[float], ys: list[float]
) -> tuple[list[float], list[float], list[float], list[float]]:
    """返回每段样条的 a,b,c,d 系数。"""

    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("需要至少两个点")
    if any(xs[i] >= xs[i + 1] for i in range(len(xs) - 1)):
        raise ValueError("xs 必须严格递增")
    n_value = len(xs) - 1
    h_values = [xs[i + 1] - xs[i] for i in range(n_value)]
    alpha = [0.0] * (n_value + 1)
    for i in range(1, n_value):
        alpha[i] = 3 / h_values[i] * (ys[i + 1] - ys[i]) - 3 / h_values[i - 1] * (
            ys[i] - ys[i - 1]
        )
    l_values = [1.0] + [0.0] * n_value
    mu_values = [0.0] * (n_value + 1)
    z_values = [0.0] * (n_value + 1)
    for i in range(1, n_value):
        l_values[i] = 2 * (xs[i + 1] - xs[i - 1]) - h_values[i - 1] * mu_values[i - 1]
        mu_values[i] = h_values[i] / l_values[i]
        z_values[i] = (alpha[i] - h_values[i - 1] * z_values[i - 1]) / l_values[i]
    l_values[n_value] = 1.0
    c_values = [0.0] * (n_value + 1)
    b_values = [0.0] * n_value
    d_values = [0.0] * n_value
    a_values = ys[:-1]
    for j in range(n_value - 1, -1, -1):
        c_values[j] = z_values[j] - mu_values[j] * c_values[j + 1]
        b_values[j] = (ys[j + 1] - ys[j]) / h_values[j] - h_values[j] * (
            c_values[j + 1] + 2 * c_values[j]
        ) / 3
        d_values[j] = (c_values[j + 1] - c_values[j]) / (3 * h_values[j])
    return a_values, b_values, c_values[:-1], d_values


def evaluate_spline(
    xs: list[float],
    coefficients: tuple[list[float], list[float], list[float], list[float]],
    x_value: float,
) -> float:
    """在所属区间内计算自然三次样条值。"""

    if not xs or x_value < xs[0] or x_value > xs[-1]:
        raise ValueError("x_value 必须落在样条定义域内")
    a_values, b_values, c_values, d_values = coefficients
    interval = max(i for i in range(len(xs) - 1) if xs[i] <= x_value)
    if interval == len(xs) - 1:
        interval -= 1
    delta = x_value - xs[interval]
    return (
        a_values[interval]
        + b_values[interval] * delta
        + c_values[interval] * delta**2
        + d_values[interval] * delta**3
    )


if __name__ == "__main__":
    xs = [0.0, 1.0, 2.0]
    ys = [0.0, 1.0, 0.0]
    coeffs = natural_cubic_spline_coefficients(xs, ys)
    assert round(evaluate_spline(xs, coeffs, 1.0), 6) == 1.0
    assert round(evaluate_spline(xs, coeffs, 0.5), 6) == 0.6875
    try:
        evaluate_spline(xs, coeffs, 3.0)
        raise AssertionError("定义域外求值应触发异常")
    except ValueError:
        pass

    print("023_spline_interpolation: all examples passed")
