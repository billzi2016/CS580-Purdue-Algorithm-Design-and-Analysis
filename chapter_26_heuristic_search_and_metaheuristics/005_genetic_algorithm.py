"""用二进制染色体的遗传算法最大化离散适应度函数。

适用场景：变量可编码为固定长度 bitstring 的组合优化。核心思想：锦标赛选择保留优者，单点交叉重组，逐位变异维持多样性。
输入输出：输入适应度和染色体长度，输出最佳染色体及适应度。时间 O(G×P×L)，空间 O(P×L)。
边界：这是教学基础版，不含精英以外的复杂选择、实数编码或多目标优化；固定种子可复现。
"""

from __future__ import annotations
import random
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class GeneticResult:
    """遗传算法历史最优的不可变二进制染色体与适应度。"""

    chromosome: tuple[int, ...]
    fitness: float


def genetic_algorithm(
    fitness: Callable[[tuple[int, ...]], float],
    length: int,
    population_size: int = 30,
    generations: int = 100,
    mutation_rate: float = 0.02,
    seed: int | None = None,
) -> GeneticResult:
    """执行带精英保留的二进制遗传算法。

    关键点：每代把历史最佳直接放入下一代，交叉和变异只作用于新子代，避免最佳解随机丢失。
    """
    if (
        length < 1
        or population_size < 2
        or generations < 0
        or not 0 <= mutation_rate <= 1
    ):
        raise ValueError("长度、种群大小、代数或变异率无效")
    rng = random.Random(seed)
    population = [
        tuple(rng.randrange(2) for _ in range(length)) for _ in range(population_size)
    ]
    best = max(population, key=fitness)
    for _ in range(generations):
        scores = [fitness(chromosome) for chromosome in population]
        generation_best = population[
            max(range(population_size), key=lambda index: scores[index])
        ]
        if fitness(generation_best) > fitness(best):
            best = generation_best
        next_population = [best]
        while len(next_population) < population_size:
            first, second = (
                _tournament(population, fitness, rng),
                _tournament(population, fitness, rng),
            )
            cut = rng.randrange(1, length) if length > 1 else 1
            child = first[:cut] + second[cut:]
            next_population.append(
                tuple(
                    1 - gene if rng.random() < mutation_rate else gene for gene in child
                )
            )
        population = next_population
    return GeneticResult(best, fitness(best))


def _tournament(
    population: list[tuple[int, ...]],
    fitness: Callable[[tuple[int, ...]], float],
    rng: random.Random,
) -> tuple[int, ...]:
    first, second = rng.choice(population), rng.choice(population)
    return first if fitness(first) >= fitness(second) else second


if __name__ == "__main__":
    result = genetic_algorithm(
        sum, length=12, population_size=40, generations=80, mutation_rate=0.04, seed=5
    )
    assert result.fitness == 12 and result.chromosome == (1,) * 12
    assert genetic_algorithm(
        sum, length=1, population_size=2, generations=0, seed=1
    ).fitness in {0, 1}
    print("005_genetic_algorithm: all examples passed")
