"""
RK4：经典四阶 Runge-Kutta ODE 方法。
"""


def runge_kutta_4(
    derivative, x0: float, y0: float, step: float, steps: int
) -> list[tuple[float, float]]:
    """返回 RK4 轨迹。"""

    if step <= 0 or steps < 0:
        raise ValueError("参数范围非法")
    x_value, y_value = x0, y0
    history = [(x_value, y_value)]
    for _ in range(steps):
        k1 = derivative(x_value, y_value)
        k2 = derivative(x_value + step / 2, y_value + step * k1 / 2)
        k3 = derivative(x_value + step / 2, y_value + step * k2 / 2)
        k4 = derivative(x_value + step, y_value + step * k3)
        y_value += step * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x_value += step
        history.append((x_value, y_value))
    return history


if __name__ == "__main__":
    history = runge_kutta_4(lambda _x, y_value: y_value, 0.0, 1.0, 0.1, 2)
    assert round(history[-1][1], 6) == 1.221403

    print("013_runge_kutta_4: all examples passed")
