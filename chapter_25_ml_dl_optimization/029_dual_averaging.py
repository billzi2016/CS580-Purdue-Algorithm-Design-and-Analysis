"""
Dual Averaging：累积全部历史梯度，再统一决定当前参数。
"""


def dual_averaging(initial_x: float, gradients: list[float], learning_rate: float) -> list[float]:
    """返回 dual averaging 参数轨迹。"""

    if learning_rate <= 0:
        raise ValueError("learning_rate 必须为正数")
    history = [initial_x]
    accumulated = 0.0
    for step, gradient in enumerate(gradients, start=1):
        accumulated += gradient
        history.append(initial_x - learning_rate * accumulated / step)
    return history


if __name__ == "__main__":
    history = dual_averaging(0.0, [3.0, 1.0, -1.0], 0.5)
    assert history == [0.0, -1.5, -1.0, -0.5]

    print("029_dual_averaging: all examples passed")
