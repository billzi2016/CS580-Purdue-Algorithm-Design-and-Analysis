"""手写粒子群优化（PSO）以最大化有界连续目标。

适用场景：目标无梯度或梯度难求的低维连续优化。核心思想：粒子速度由惯性、个人最佳和群体最佳共同更新。
输入输出：输入目标、变量上下界与参数，输出最佳位置和分数。时间 O(I×P×D)，空间 O(P×D)。
边界：边界通过截断保证；这是基础全局最优 PSO，不含邻域拓扑、自适应参数或约束修复。
"""

from __future__ import annotations
import random
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class PSOResult:
    """粒子群迭代结束时发现的全局最佳位置与分数。"""

    position: tuple[float, ...]
    score: float


def particle_swarm_optimize(
    objective: Callable[[tuple[float, ...]], float],
    bounds: list[tuple[float, float]],
    particles: int = 20,
    iterations: int = 100,
    inertia: float = 0.7,
    cognitive: float = 1.4,
    social: float = 1.4,
    seed: int | None = None,
) -> PSOResult:
    """在盒约束内最大化连续目标。

    参数：每维 bounds 为 ``(low, high)``。返回历史全局最佳。关键点：位置更新后立即评分并更新个人/全局最佳。
    边界：维度为空、边界无效或粒子数非正都会报错。
    """
    if (
        not bounds
        or particles < 1
        or iterations < 0
        or any(low > high for low, high in bounds)
    ):
        raise ValueError("维度、边界、粒子数或迭代次数无效")
    rng = random.Random(seed)
    positions = [
        tuple(rng.uniform(low, high) for low, high in bounds) for _ in range(particles)
    ]
    velocities = [[0.0 for _ in bounds] for _ in range(particles)]
    personal_best = list(positions)
    personal_scores = [objective(point) for point in positions]
    best_index = max(range(particles), key=lambda index: personal_scores[index])
    global_best, global_score = personal_best[best_index], personal_scores[best_index]
    for _ in range(iterations):
        for index, position in enumerate(positions):
            updated_velocity: list[float] = []
            updated_position: list[float] = []
            for dimension, (low, high) in enumerate(bounds):
                velocity = (
                    inertia * velocities[index][dimension]
                    + cognitive
                    * rng.random()
                    * (personal_best[index][dimension] - position[dimension])
                    + social
                    * rng.random()
                    * (global_best[dimension] - position[dimension])
                )
                updated_velocity.append(velocity)
                updated_position.append(
                    min(high, max(low, position[dimension] + velocity))
                )
            velocities[index] = updated_velocity
            positions[index] = tuple(updated_position)
            score = objective(positions[index])
            if score > personal_scores[index]:
                personal_best[index], personal_scores[index] = positions[index], score
                if score > global_score:
                    global_best, global_score = positions[index], score
    return PSOResult(global_best, global_score)


if __name__ == "__main__":
    result = particle_swarm_optimize(
        lambda point: -((point[0] - 2) ** 2 + (point[1] + 1) ** 2),
        [(-5, 5), (-5, 5)],
        particles=30,
        iterations=150,
        seed=4,
    )
    assert result.score > -0.01
    assert -5 <= result.position[0] <= 5 and -5 <= result.position[1] <= 5
    print("004_particle_swarm_optimization: all examples passed")
