"""
Backtracking Line Search：用 Armijo 条件递减步长。
"""


def quadratic_value(x_value: float) -> float:
    return 0.5 * (x_value - 3.0) ** 2


def quadratic_gradient(x_value: float) -> float:
    return x_value - 3.0


def backtracking_line_search(
    x_value: float,
    direction: float,
    alpha: float = 1.0,
    beta: float = 0.5,
    c: float = 1e-4,
) -> float:
    """返回满足 Armijo 条件的步长。"""

    if alpha <= 0 or not 0 < beta < 1 or not 0 < c < 1:
        raise ValueError("参数范围非法")
    gradient = quadratic_gradient(x_value)
    while (
        quadratic_value(x_value + alpha * direction)
        > quadratic_value(x_value) + c * alpha * gradient * direction
    ):
        alpha *= beta
    return alpha


if __name__ == "__main__":
    step = backtracking_line_search(0.0, direction=3.0)
    assert 0 < step <= 1.0
    assert quadratic_value(0.0 + step * 3.0) < quadratic_value(0.0)

    print("031_backtracking_line_search: all examples passed")
