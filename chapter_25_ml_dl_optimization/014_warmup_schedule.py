"""
Warmup：训练初期逐步把学习率拉到目标值，减轻不稳定更新。
"""


def linear_warmup_lr(base_lr: float, step: int, warmup_steps: int) -> float:
    """线性 warmup；超过 warmup 阶段后返回 base_lr。"""

    if base_lr <= 0 or warmup_steps < 0 or step < 0:
        raise ValueError("参数范围非法")
    if warmup_steps == 0:
        return base_lr
    if step >= warmup_steps:
        return base_lr
    return base_lr * (step + 1) / warmup_steps


def warmup_then_constant(base_lr: float, step: int, warmup_steps: int) -> float:
    """显式封装 warmup 后恒定学习率。"""

    return linear_warmup_lr(base_lr, step, warmup_steps)


if __name__ == "__main__":
    assert linear_warmup_lr(0.1, 0, 5) == 0.02
    assert linear_warmup_lr(0.1, 4, 5) == 0.1
    assert warmup_then_constant(0.1, 8, 5) == 0.1

    print("014_warmup_schedule: all examples passed")
