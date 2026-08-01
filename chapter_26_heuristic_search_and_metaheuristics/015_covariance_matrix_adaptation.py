"""实现一维 CMA-ES 基础版以最小化有界连续目标。

适用场景：展示 CMA-ES 的采样、精英重组与步长自适应核心。核心思想：从正态分布采样，按精英加权更新均值和方差。
输入输出：输入一维目标和边界，输出最佳位置及值。时间 O(I×P)，空间 O(P)。
边界：仅一维，明确不含完整多维协方差矩阵与演化路径；用于教学而非工业优化。
"""

from __future__ import annotations
import math
import random
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class CMAESResult:
    position: float
    value: float


def cma_es_1d(
    objective: Callable[[float], float],
    lower: float,
    upper: float,
    population: int = 12,
    iterations: int = 80,
    seed: int | None = None,
) -> CMAESResult:
    """以一维高斯精英重组近似 CMA-ES 的均值与尺度更新。"""
    if lower >= upper or population < 2 or iterations < 0:
        raise ValueError("边界、种群或迭代次数无效")
    rng, mean, sigma = random.Random(seed), (lower + upper) / 2, (upper - lower) / 3
    best_position, best_value = mean, objective(mean)
    elite_count = population // 2
    for _ in range(iterations):
        samples = [
            min(upper, max(lower, rng.gauss(mean, sigma))) for _ in range(population)
        ]
        samples.sort(key=objective)
        if objective(samples[0]) < best_value:
            best_position, best_value = samples[0], objective(samples[0])
        elites = samples[:elite_count]
        mean = sum(elites) / elite_count
        sigma = max(
            (upper - lower) * 1e-6,
            math.sqrt(sum((sample - mean) ** 2 for sample in elites) / elite_count),
        )
    return CMAESResult(best_position, best_value)


if __name__ == "__main__":
    result = cma_es_1d(
        lambda value: (value - 1.25) ** 2,
        -5,
        5,
        iterations=300,
        seed=10,
    )
    assert result.value < 0.002
    assert -5 <= result.position <= 5
    print("015_covariance_matrix_adaptation: all examples passed")
