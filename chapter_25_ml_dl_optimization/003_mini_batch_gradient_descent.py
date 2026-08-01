"""
Mini-batch 梯度下降：每步在一小批样本上估计梯度。

文件意图：
- 介于 batch 和 SGD 之间，是深度学习实践中的常见默认形态。
- 用切片分批，避免引入数据加载器等额外复杂度。
"""


def batch_gradient(xs: list[float], ys: list[float], weight: float) -> float:
    """计算一个 mini-batch 上的平均梯度。"""

    if len(xs) != len(ys) or not xs:
        raise ValueError("xs 和 ys 必须等长且非空")
    total = 0.0
    for x_value, y_value in zip(xs, ys, strict=True):
        total += (weight * x_value - y_value) * x_value
    return total / len(xs)


def mini_batch_gradient_descent(
    xs: list[float],
    ys: list[float],
    initial_weight: float,
    learning_rate: float,
    batch_size: int,
    epochs: int,
) -> list[float]:
    """执行顺序 mini-batch GD，返回 epoch 轨迹。"""

    if batch_size <= 0 or learning_rate <= 0 or epochs < 0:
        raise ValueError("batch_size、learning_rate 必须为正，epochs 不能为负")
    if len(xs) != len(ys) or not xs:
        raise ValueError("xs 和 ys 必须等长且非空")

    weight = initial_weight
    history = [weight]
    for _ in range(epochs):
        for start in range(0, len(xs), batch_size):
            batch_xs = xs[start : start + batch_size]
            batch_ys = ys[start : start + batch_size]
            weight -= learning_rate * batch_gradient(batch_xs, batch_ys, weight)
        history.append(weight)
    return history


if __name__ == "__main__":
    xs = [1.0, 2.0, 3.0, 4.0]
    ys = [2.0, 4.0, 6.0, 8.0]
    history = mini_batch_gradient_descent(xs, ys, 0.0, 0.05, batch_size=2, epochs=5)
    assert len(history) == 6
    assert history[-1] > 1.5
    assert abs(batch_gradient([1.0, 2.0], [2.0, 4.0], 2.0)) < 1e-9

    print("003_mini_batch_gradient_descent: all examples passed")
