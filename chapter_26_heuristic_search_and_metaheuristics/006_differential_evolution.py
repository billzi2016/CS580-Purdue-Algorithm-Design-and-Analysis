"""手写差分进化（DE/rand/1/bin）最大化有界连续目标。

适用场景：非凸、无导数连续优化。核心思想：三个不同个体的差分形成变异向量，再以二项交叉产生试验个体。
输入输出：输入目标和边界，输出最优向量。时间 O(G×P×D)，空间 O(P×D)。
边界：种群至少四个；试验向量截断到边界；基础版不含自适应 F/CR 或并行评估。
"""

from __future__ import annotations
import random
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class DEResult:
    position: tuple[float, ...]
    score: float


def differential_evolution(
    objective: Callable[[tuple[float, ...]], float],
    bounds: list[tuple[float, float]],
    population_size: int = 20,
    generations: int = 100,
    differential_weight: float = 0.8,
    crossover_rate: float = 0.7,
    seed: int | None = None,
) -> DEResult:
    """以 DE/rand/1/bin 在盒约束内最大化目标。

    关键点：每个目标向量只和自己的试验向量比较，贪心选择保证该位置适应度不会下降。
    """
    if (
        not bounds
        or population_size < 4
        or generations < 0
        or any(low > high for low, high in bounds)
        or not 0 <= crossover_rate <= 1
    ):
        raise ValueError("DE 参数或边界无效")
    rng = random.Random(seed)
    population = [
        tuple(rng.uniform(low, high) for low, high in bounds)
        for _ in range(population_size)
    ]
    scores = [objective(point) for point in population]
    for _ in range(generations):
        for target_index, target in enumerate(population):
            choices = [
                index for index in range(population_size) if index != target_index
            ]
            first, second, third = rng.sample(choices, 3)
            forced_dimension = rng.randrange(len(bounds))
            trial = []
            for dimension, (low, high) in enumerate(bounds):
                mutant = population[first][dimension] + differential_weight * (
                    population[second][dimension] - population[third][dimension]
                )
                value = (
                    mutant
                    if dimension == forced_dimension or rng.random() < crossover_rate
                    else target[dimension]
                )
                trial.append(min(high, max(low, value)))
            candidate = tuple(trial)
            candidate_score = objective(candidate)
            if candidate_score >= scores[target_index]:
                population[target_index], scores[target_index] = (
                    candidate,
                    candidate_score,
                )
    best_index = max(range(population_size), key=lambda index: scores[index])
    return DEResult(population[best_index], scores[best_index])


if __name__ == "__main__":
    result = differential_evolution(
        lambda point: -((point[0] - 1.5) ** 2),
        [(-4, 4)],
        population_size=20,
        generations=100,
        seed=6,
    )
    assert result.score > -0.001
    assert -4 <= result.position[0] <= 4
    print("006_differential_evolution: all examples passed")
