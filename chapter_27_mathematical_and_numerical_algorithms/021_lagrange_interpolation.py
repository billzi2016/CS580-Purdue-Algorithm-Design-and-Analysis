"""
Lagrange 插值。
"""


def lagrange_interpolation(xs: list[float], ys: list[float], x_value: float) -> float:
    """直接按 Lagrange 基函数求值。"""

    if len(xs) != len(ys) or not xs:
        raise ValueError("xs 和 ys 必须等长且非空")
    total = 0.0
    for i, yi in enumerate(ys):
        basis = 1.0
        for j, xj in enumerate(xs):
            if i == j:
                continue
            basis *= (x_value - xj) / (xs[i] - xj)
        total += yi * basis
    return total


if __name__ == "__main__":
    assert lagrange_interpolation([0.0, 1.0, 2.0], [1.0, 2.0, 5.0], 3.0) == 10.0

    print("021_lagrange_interpolation: all examples passed")
