"""
Newton 方法：利用一阶导和二阶导做二次近似更新。
"""


def newton_optimize(initial_x: float, steps: int) -> list[float]:
    """优化 f(x) = (x-2)^4 + 1，返回参数轨迹。"""

    if steps < 0:
        raise ValueError("steps 不能为负数")
    x_value = initial_x
    history = [x_value]
    for _ in range(steps):
        gradient = 4 * (x_value - 2) ** 3
        hessian = 12 * (x_value - 2) ** 2
        if hessian == 0:
            break
        x_value -= gradient / hessian
        history.append(x_value)
    return history


if __name__ == "__main__":
    history = newton_optimize(5.0, 4)
    assert len(history) >= 2
    assert abs(history[-1] - 2.0) < 1.0

    print("021_newton_method: all examples passed")
