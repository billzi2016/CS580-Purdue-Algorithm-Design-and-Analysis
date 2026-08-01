"""
Cosine Annealing：让学习率按余弦曲线平滑下降。
"""

from math import cos, pi


def cosine_annealing_lr(max_lr: float, min_lr: float, step: int, total_steps: int) -> float:
    """计算单周期余弦退火学习率。"""

    if max_lr <= 0 or min_lr < 0 or min_lr > max_lr or total_steps <= 0 or step < 0:
        raise ValueError("参数范围非法")
    clipped_step = min(step, total_steps)
    ratio = (1 + cos(pi * clipped_step / total_steps)) / 2
    return min_lr + (max_lr - min_lr) * ratio


if __name__ == "__main__":
    assert cosine_annealing_lr(0.1, 0.0, 0, 10) == 0.1
    assert round(cosine_annealing_lr(0.1, 0.0, 5, 10), 6) == 0.05
    assert cosine_annealing_lr(0.1, 0.0, 10, 10) == 0.0

    print("013_cosine_annealing: all examples passed")
