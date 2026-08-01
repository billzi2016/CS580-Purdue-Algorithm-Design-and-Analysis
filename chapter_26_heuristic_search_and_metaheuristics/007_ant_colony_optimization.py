"""用蚁群算法近似求解对称旅行商问题。

适用场景：节点数较小、距离矩阵给定的 TSP 教学示例。核心思想：蚂蚁按信息素与距离启发式随机构造回路，再蒸发并按回路质量沉积信息素。
输入输出：输入方阵距离，输出最短闭合回路和长度。时间 O(I×A×N²)，空间 O(N²)。
边界：仅支持非负、对称距离；这是基础 ACO，不含候选列表、局部搜索或并行蚂蚁。
"""

from __future__ import annotations
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class ACOResult:
    tour: tuple[int, ...]
    length: float


def ant_colony_tsp(
    distances: list[list[float]],
    ants: int = 20,
    iterations: int = 80,
    evaporation: float = 0.3,
    seed: int | None = None,
) -> ACOResult:
    """用信息素引导的随机回路构造近似最短 TSP 回路。

    距离矩阵必须为对称方阵。关键点：较短回路沉积更多 ``1/length`` 信息素，蒸发避免早期路径永久垄断。
    """
    size = len(distances)
    if (
        size < 2
        or ants < 1
        or iterations < 0
        or not 0 < evaporation < 1
        or any(len(row) != size for row in distances)
    ):
        raise ValueError("ACO 参数或距离矩阵无效")
    if any(
        distances[i][j] < 0 or distances[i][j] != distances[j][i]
        for i in range(size)
        for j in range(size)
    ):
        raise ValueError("距离必须非负且对称")
    rng = random.Random(seed)
    pheromone = [[1.0 for _ in range(size)] for _ in range(size)]
    best_tour: tuple[int, ...] = ()
    best_length = float("inf")
    for _ in range(iterations):
        tours: list[tuple[tuple[int, ...], float]] = []
        for _ in range(ants):
            start = rng.randrange(size)
            tour = [start]
            while len(tour) < size:
                candidates = [node for node in range(size) if node not in tour]
                weights = [
                    pheromone[tour[-1]][node] / max(distances[tour[-1]][node], 1e-12)
                    for node in candidates
                ]
                tour.append(rng.choices(candidates, weights=weights)[0])
            length = sum(distances[tour[i]][tour[(i + 1) % size]] for i in range(size))
            tours.append((tuple(tour), length))
            if length < best_length:
                best_tour, best_length = tuple(tour), length
        for i in range(size):
            for j in range(size):
                pheromone[i][j] *= 1 - evaporation
        for tour, length in tours:
            deposit = 1 / max(length, 1e-12)
            for i in range(size):
                first, second = tour[i], tour[(i + 1) % size]
                pheromone[first][second] += deposit
                pheromone[second][first] += deposit
    return ACOResult(best_tour, best_length)


if __name__ == "__main__":
    matrix = [[0, 1, 3, 2], [1, 0, 2, 3], [3, 2, 0, 1], [2, 3, 1, 0]]
    result = ant_colony_tsp(matrix, iterations=100, seed=7)
    assert set(result.tour) == {0, 1, 2, 3}
    assert result.length == 6
    print("007_ant_colony_optimization: all examples passed")
