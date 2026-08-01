"""
Nesterov Accelerated Gradient：先看一眼前瞻位置，再计算梯度。
"""


def nesterov_optimize(initial_x: float, learning_rate: float, momentum: float, steps: int) -> list[float]:
    """优化 f(x)=0.5*(x-3)^2，返回参数轨迹。"""

    if learning_rate <= 0 or not 0 <= momentum < 1 or steps < 0:
        raise ValueError("参数范围非法")
    x_value = initial_x
    velocity = 0.0
    history = [x_value]
    for _ in range(steps):
        look_ahead = x_value + momentum * velocity
        gradient = look_ahead - 3.0
        velocity = momentum * velocity - learning_rate * gradient
        x_value += velocity
        history.append(x_value)
    return history


if __name__ == "__main__":
    path = nesterov_optimize(0.0, 0.1, 0.9, 6)
    assert len(path) == 7
    assert path[-1] > 2.0
    assert path[2] > path[1]

    print("005_nesterov_accelerated_gradient: all examples passed")
