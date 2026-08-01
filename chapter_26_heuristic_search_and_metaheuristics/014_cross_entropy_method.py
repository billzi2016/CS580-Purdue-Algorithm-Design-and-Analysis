"""用伯努利交叉熵方法（CEM）最大化二进制染色体目标。

适用场景：可从参数化分布采样的离散优化。核心思想：采样后保留精英样本，并把各位概率更新为精英频率。
输入输出：输入适应度、长度和采样参数，输出最佳染色体。时间 O(I×S×L)，空间 O(S×L)。
边界：概率裁剪防止过早退化；这是独立伯努利基础版，不表达位间相关性。
"""

from __future__ import annotations
import random
from collections.abc import Callable
from dataclasses import dataclass

@dataclass(frozen=True)
class CEMResult:
    chromosome: tuple[int, ...]
    score: float

def cross_entropy_method(fitness: Callable[[tuple[int, ...]], float], length: int, samples: int = 50, iterations: int = 50, elite_fraction: float = 0.2, seed: int | None = None) -> CEMResult:
    """以精英样本频率反复更新每个位为 1 的采样概率。"""
    if length < 1 or samples < 2 or iterations < 0 or not 0 < elite_fraction <= 1:
        raise ValueError("CEM 参数无效")
    rng, probabilities = random.Random(seed), [0.5] * length
    best, best_score = tuple(0 for _ in range(length)), float("-inf")
    elite_count = max(1, int(samples * elite_fraction))
    for _ in range(iterations):
        population = [tuple(int(rng.random() < probability) for probability in probabilities) for _ in range(samples)]
        ranked = sorted(population, key=fitness, reverse=True)
        if fitness(ranked[0]) > best_score:
            best, best_score = ranked[0], fitness(ranked[0])
        elites = ranked[:elite_count]
        probabilities = [min(0.99, max(0.01, sum(item[index] for item in elites) / elite_count)) for index in range(length)]
    return CEMResult(best, best_score)

if __name__ == "__main__":
    result = cross_entropy_method(sum, 10, samples=60, iterations=40, seed=9)
    assert result.score == 10
    print("014_cross_entropy_method: all examples passed")
