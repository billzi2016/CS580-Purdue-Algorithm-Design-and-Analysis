"""
随机梯度下降：每一步只用一个样本更新参数。

文件意图：
- 展示样本级更新带来的噪声与更频繁的参数调整。
- 用固定顺序遍历样本，避免示例测试依赖随机打乱。
"""


def sgd_epoch(
    xs: list[float], ys: list[float], weight: float, learning_rate: float
) -> float:
    """执行一个 epoch 的顺序 SGD。"""

    if len(xs) != len(ys) or not xs:
        raise ValueError("xs 和 ys 必须等长且非空")
    if learning_rate <= 0:
        raise ValueError("learning_rate 必须为正数")
    for x_value, y_value in zip(xs, ys, strict=True):
        gradient = (weight * x_value - y_value) * x_value
        weight -= learning_rate * gradient
    return weight


def stochastic_gradient_descent(
    xs: list[float],
    ys: list[float],
    initial_weight: float,
    learning_rate: float,
    epochs: int,
) -> list[float]:
    """返回每个 epoch 结束后的参数。"""

    if epochs < 0:
        raise ValueError("epochs 不能为负数")
    weight = initial_weight
    history = [weight]
    for _ in range(epochs):
        weight = sgd_epoch(xs, ys, weight, learning_rate)
        history.append(weight)
    return history


if __name__ == "__main__":
    xs = [1.0, 2.0, 3.0]
    ys = [2.0, 4.0, 6.0]
    history = stochastic_gradient_descent(
        xs, ys, initial_weight=0.0, learning_rate=0.05, epochs=4
    )
    assert len(history) == 5
    assert history[-1] > history[1]
    assert abs(sgd_epoch(xs, ys, 2.0, 0.01) - 2.0) < 1e-9

    print("002_stochastic_gradient_descent: all examples passed")
