"""
Momentum：在梯度下降中累积速度，减小锯齿方向震荡。
"""


def momentum_optimize(
    initial_x: float,
    learning_rate: float,
    momentum: float,
    steps: int,
) -> list[float]:
    """优化 f(x)=0.5*(x-3)^2，返回参数轨迹。"""

    if learning_rate <= 0 or not 0 <= momentum < 1 or steps < 0:
        raise ValueError("参数范围非法")
    x_value = initial_x
    velocity = 0.0
    history = [x_value]
    for _ in range(steps):
        gradient = x_value - 3.0
        velocity = momentum * velocity - learning_rate * gradient
        x_value += velocity
        history.append(x_value)
    return history


if __name__ == "__main__":
    path = momentum_optimize(initial_x=0.0, learning_rate=0.1, momentum=0.9, steps=6)
    assert len(path) == 7
    assert abs(path[-1] - 3.0) < 1.5
    assert path[1] > path[0]

    print("004_momentum: all examples passed")
