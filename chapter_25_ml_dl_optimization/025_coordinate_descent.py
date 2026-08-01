"""
坐标下降：每步只优化一个坐标。
"""


def coordinate_descent(
    initial_x: float, initial_y: float, steps: int
) -> list[tuple[float, float]]:
    """优化 f(x,y)=(x-1)^2 + (y+2)^2。"""

    if steps < 0:
        raise ValueError("steps 不能为负数")
    x_value, y_value = initial_x, initial_y
    history = [(x_value, y_value)]
    for step in range(steps):
        if step % 2 == 0:
            x_value = 1.0
        else:
            y_value = -2.0
        history.append((x_value, y_value))
    return history


if __name__ == "__main__":
    history = coordinate_descent(5.0, 5.0, 4)
    assert history[1] == (1.0, 5.0)
    assert history[2] == (1.0, -2.0)

    print("025_coordinate_descent: all examples passed")
