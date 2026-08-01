"""
Euler ODE 方法。
"""


def euler_method(derivative, x0: float, y0: float, step: float, steps: int) -> list[tuple[float, float]]:
    """求解 y' = f(x,y) 的显式 Euler 轨迹。"""

    if step <= 0 or steps < 0:
        raise ValueError("参数范围非法")
    x_value, y_value = x0, y0
    history = [(x_value, y_value)]
    for _ in range(steps):
        y_value += step * derivative(x_value, y_value)
        x_value += step
        history.append((x_value, y_value))
    return history


if __name__ == "__main__":
    history = euler_method(lambda _x, y_value: y_value, 0.0, 1.0, 0.1, 3)
    assert [round(item[1], 3) for item in history] == [1.0, 1.1, 1.21, 1.331]

    print("012_euler_method_ode: all examples passed")
