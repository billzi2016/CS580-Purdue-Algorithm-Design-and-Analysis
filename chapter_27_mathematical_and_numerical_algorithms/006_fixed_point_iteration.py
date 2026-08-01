"""
不动点迭代。
"""


def fixed_point_iteration(mapping, initial_x: float, steps: int) -> list[float]:
    """返回迭代轨迹。"""

    if steps < 0:
        raise ValueError("steps 不能为负数")
    history = [initial_x]
    x_value = initial_x
    for _ in range(steps):
        x_value = mapping(x_value)
        history.append(x_value)
    return history


if __name__ == "__main__":
    history = fixed_point_iteration(lambda x_value: 0.5 * (x_value + 2.0 / x_value), 1.0, 5)
    assert round(history[-1], 6) == 1.414214

    print("006_fixed_point_iteration: all examples passed")
