"""
AdamW：把权重衰减从梯度项中解耦。

意图：用一维参数轨迹展示 AdamW 的一阶矩、二阶矩、偏差修正和解耦权重
衰减。输入是初始参数和梯度序列，输出每一步更新后的参数历史。

时间复杂度：O(t)，t 为梯度步数。空间复杂度：O(t)，用于保存教学轨迹。
边界情况：学习率、epsilon 必须为正，weight_decay 非负，beta 必须落在
[0, 1) 内，否则偏差修正分母可能为 0 或动量语义不成立。
"""

from math import sqrt


def adamw_update(
    initial_x: float,
    gradients: list[float],
    learning_rate: float,
    weight_decay: float,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-8,
) -> list[float]:
    """执行 AdamW 更新。

    参数：initial_x 为一维参数，gradients 为每步梯度，beta1/beta2 为矩估计
    衰减系数。
    返回值：包含初始值和每次更新后参数的列表。
    关键算法点：权重衰减直接作用在参数上，不混入梯度矩估计。
    """

    if learning_rate <= 0 or weight_decay < 0:
        raise ValueError("learning_rate 必须为正，weight_decay 不能为负")
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
        x_value *= 1 - learning_rate * weight_decay
        x_value -= learning_rate * first_hat / (sqrt(second_hat) + epsilon)
        history.append(x_value)
    return history


if __name__ == "__main__":
    no_decay = adamw_update(1.0, [0.5, 0.5], 0.1, 0.0)
    with_decay = adamw_update(1.0, [0.5, 0.5], 0.1, 0.1)
    assert len(with_decay) == 3
    assert with_decay[-1] < no_decay[-1]
    assert adamw_update(1.0, [], 0.1, 0.0) == [1.0]
    try:
        adamw_update(1.0, [0.5], 0.1, 0.0, beta1=1.0)
        raise AssertionError("beta1=1 会导致偏差修正分母为 0")
    except ValueError:
        pass

    print("009_adamw: all examples passed")
