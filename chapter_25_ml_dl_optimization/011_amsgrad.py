"""
AMSGrad：在 Adam 上对二阶矩取历史最大值，增强收敛稳定性。

意图：展示 AMSGrad 与 Adam 的关键差异：更新分母使用历史最大二阶矩，避免
有效学习率因二阶矩下降而反复变大。输入是一维参数和梯度序列。

时间复杂度：O(t)，t 为梯度步数。空间复杂度：O(t)，保存参数和最大二阶矩轨迹。
边界情况：学习率、epsilon 必须为正，beta 必须在 [0, 1) 内。
"""

from math import sqrt


def amsgrad_update(
    initial_x: float,
    gradients: list[float],
    learning_rate: float,
    beta1: float = 0.9,
    beta2: float = 0.999,
    epsilon: float = 1e-8,
) -> tuple[list[float], list[float]]:
    """返回参数轨迹和历史最大二阶矩轨迹。

    参数：initial_x 为一维参数，gradients 为梯度序列。
    返回值：第一个列表是参数历史，第二个列表是未偏差修正的最大二阶矩历史。
    关键算法点：`max_second` 单调不减，这是 AMSGrad 的稳定性核心。
    """

    if learning_rate <= 0:
        raise ValueError("learning_rate 必须为正数")
    if not 0 <= beta1 < 1 or not 0 <= beta2 < 1 or epsilon <= 0:
        raise ValueError("beta1/beta2 必须在 [0, 1) 内，epsilon 必须为正")
    x_value = initial_x
    first_moment = 0.0
    second_moment = 0.0
    max_second = 0.0
    history = [x_value]
    max_history = [max_second]
    for step, gradient in enumerate(gradients, start=1):
        first_moment = beta1 * first_moment + (1 - beta1) * gradient
        second_moment = beta2 * second_moment + (1 - beta2) * gradient * gradient
        max_second = max(max_second, second_moment)
        first_hat = first_moment / (1 - beta1**step)
        x_value -= learning_rate * first_hat / (sqrt(max_second) + epsilon)
        history.append(x_value)
        max_history.append(max_second)
    return history, max_history


if __name__ == "__main__":
    params, maxima = amsgrad_update(0.0, [3.0, 2.0, 1.0], 0.1)
    assert len(params) == 4
    assert maxima[1] <= maxima[2] <= maxima[3]
    assert amsgrad_update(5.0, [], 0.1)[0] == [5.0]
    try:
        amsgrad_update(0.0, [1.0], 0.1, epsilon=0.0)
        raise AssertionError("epsilon=0 应触发异常")
    except ValueError:
        pass

    print("011_amsgrad: all examples passed")
