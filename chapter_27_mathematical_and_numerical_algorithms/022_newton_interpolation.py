"""
Newton 插值：先构造差商，再用嵌套形式求值。
"""


def divided_differences(xs: list[float], ys: list[float]) -> list[float]:
    """返回 Newton 形式的差商系数。"""

    if len(xs) != len(ys) or not xs:
        raise ValueError("xs 和 ys 必须等长且非空")
    coefficients = ys[:]
    for order in range(1, len(xs)):
        for index in range(len(xs) - 1, order - 1, -1):
            coefficients[index] = (coefficients[index] - coefficients[index - 1]) / (
                xs[index] - xs[index - order]
            )
    return coefficients


def evaluate_newton_form(
    xs: list[float], coefficients: list[float], x_value: float
) -> float:
    """用嵌套乘法求值。"""

    result = coefficients[-1]
    for index in range(len(coefficients) - 2, -1, -1):
        result = result * (x_value - xs[index]) + coefficients[index]
    return result


if __name__ == "__main__":
    xs = [0.0, 1.0, 2.0]
    coeffs = divided_differences(xs, [1.0, 2.0, 5.0])
    assert [round(value, 6) for value in coeffs] == [1.0, 1.0, 1.0]
    assert evaluate_newton_form(xs, coeffs, 3.0) == 10.0

    print("022_newton_interpolation: all examples passed")
