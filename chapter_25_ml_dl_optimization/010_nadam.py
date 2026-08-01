"""
Nadam：把 Nesterov 动量思想并入 Adam。

意图：用一维参数展示 Nadam 如何在 Adam 的偏差修正矩估计上加入
Nesterov-style lookahead 梯度项。输入是初始参数和梯度序列，输出参数轨迹。

时间复杂度：O(t)，t 为梯度步数。空间复杂度：O(t)，用于保存教学轨迹。
边界情况：学习率、epsilon 必须为正，beta 必须在 [0, 1) 内。
"""

from math import sqrt


def nadam_update(
    initial_x: float,
    gradients: list[float],
    learning_rate: float,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-8,
) -> list[float]:
    """执行 Nadam 更新。

    参数：initial_x 为一维参数，gradients 为梯度序列，beta1/beta2 控制一阶和
    二阶矩的指数滑动平均。
    返回值：包含初始参数和每步更新后参数的历史。
    关键算法点：Nesterov 项使用当前梯度和一阶矩偏差修正组合得到。
    """

    if learning_rate <= 0:
        raise ValueError("learning_rate 必须为正数")
    if not 0 <= beta1 < 1 or not 0 <= beta2 < 1 or epsilon <= 0:
        raise ValueError("beta1/beta2 必须在 [0, 1) 内，epsilon 必须为正")
    x_value = initial_x
    first_moment = 0.0
    second_moment = 0.0
    history = [x_value]
    for step, gradient in enumerate(gradients, start=1):
        first_moment = beta1 * first_moment + (1 - beta1) * gradient
        second_moment = beta2 * second_moment + (1 - beta2) * gradient * gradient
        first_hat = first_moment / (1 - beta1**step)
        second_hat = second_moment / (1 - beta2**step)
        nesterov_term = beta1 * first_hat + (1 - beta1) * gradient / (1 - beta1**step)
        x_value -= learning_rate * nesterov_term / (sqrt(second_hat) + epsilon)
        history.append(x_value)
    return history


if __name__ == "__main__":
    history = nadam_update(0.0, [3.0, 2.0, 1.0], 0.1)
    assert len(history) == 4
    assert history[-1] < history[1]
    assert nadam_update(2.0, [], 0.1) == [2.0]
    try:
        nadam_update(0.0, [1.0], 0.1, beta2=1.0)
        raise AssertionError("beta2=1 会导致偏差修正分母为 0")
    except ValueError:
        pass

    print("010_nadam: all examples passed")
