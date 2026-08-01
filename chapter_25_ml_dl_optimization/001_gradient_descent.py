"""
批量梯度下降：每一步都用全部样本的平均梯度更新参数。

文件意图：
- 展示最基础的优化器更新规则。
- 用一元线性回归的平方损失作为例子，避免把注意力浪费在模型结构上。
- 返回完整参数轨迹，便于后续和 SGD、Mini-batch 对比。
"""


def mean_squared_error_gradient(xs: list[float], ys: list[float], weight: float) -> float:
    """计算一元线性模型 y_hat = weight * x 的平均平方损失梯度。"""

    if len(xs) != len(ys) or not xs:
        raise ValueError("xs 和 ys 必须等长且非空")
    gradient = 0.0
    for x_value, y_value in zip(xs, ys, strict=True):
        gradient += (weight * x_value - y_value) * x_value
    return gradient / len(xs)


def gradient_descent(
    xs: list[float],
    ys: list[float],
    initial_weight: float,
    learning_rate: float,
    steps: int,
) -> list[float]:
    """执行批量梯度下降，返回每步更新后的参数轨迹。"""

    if learning_rate <= 0 or steps < 0:
        raise ValueError("learning_rate 必须为正数，steps 不能为负数")
    weight = initial_weight
    history = [weight]
    for _ in range(steps):
        weight -= learning_rate * mean_squared_error_gradient(xs, ys, weight)
        history.append(weight)
    return history


if __name__ == "__main__":
    xs = [1.0, 2.0, 3.0]
    ys = [2.0, 4.0, 6.0]
    track = gradient_descent(xs, ys, initial_weight=0.0, learning_rate=0.1, steps=5)
    assert len(track) == 6
    assert track[0] == 0.0
    assert track[-1] > 1.5
    assert mean_squared_error_gradient(xs, ys, 2.0) == 0.0

    print("001_gradient_descent: all examples passed")
