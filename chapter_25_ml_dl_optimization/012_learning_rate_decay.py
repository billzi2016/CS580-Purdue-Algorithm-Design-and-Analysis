"""
学习率衰减：按训练步数逐步降低步长。
"""


def step_decay(initial_lr: float, step: int, drop_factor: float, drop_every: int) -> float:
    """阶梯衰减。"""

    if initial_lr <= 0 or not 0 < drop_factor <= 1 or drop_every <= 0 or step < 0:
        raise ValueError("参数范围非法")
    return initial_lr * (drop_factor ** (step // drop_every))


def exponential_decay(initial_lr: float, step: int, decay_rate: float) -> float:
    """指数衰减。"""

    if initial_lr <= 0 or not 0 < decay_rate <= 1 or step < 0:
        raise ValueError("参数范围非法")
    return initial_lr * (decay_rate**step)


if __name__ == "__main__":
    assert step_decay(0.1, step=0, drop_factor=0.5, drop_every=10) == 0.1
    assert step_decay(0.1, step=20, drop_factor=0.5, drop_every=10) == 0.025
    assert round(exponential_decay(0.1, step=3, decay_rate=0.9), 6) == 0.0729

    print("012_learning_rate_decay: all examples passed")
