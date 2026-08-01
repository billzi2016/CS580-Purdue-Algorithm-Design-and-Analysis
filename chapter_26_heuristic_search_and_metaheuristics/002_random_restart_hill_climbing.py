"""通过随机重启爬山法降低单个局部最优的影响。

适用场景：目标函数有多个峰值、单次爬山容易停在差局部最优的离散优化问题。
核心思想：从多个随机起点独立执行最陡上升爬山，再保留所有运行中得分最高的结果。
输入输出：输入起点采样器、目标函数和邻居函数，输出全局最佳运行结果及每次运行记录。
时间复杂度：R 次爬山的总和；空间 O(R)，R 为重启次数。
边界情况：固定 ``seed`` 使测试可复现；重启次数小于一会报错；这不是全局最优证明。
"""

from __future__ import annotations

import random
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TypeVar


State = TypeVar("State")


@dataclass(frozen=True)
class RestartResult:
    """包含最佳状态、得分与每次运行最终得分的随机重启结果。"""

    state: object
    score: float
    run_scores: tuple[float, ...]


def random_restart_hill_climb(
    sample_start: Callable[[random.Random], State],
    objective: Callable[[State], float],
    neighbors: Callable[[State], Iterable[State]],
    restarts: int,
    seed: int | None = None,
) -> RestartResult:
    """从独立随机起点执行爬山，并返回得分最好的那次。

    参数：起点采样器会收到私有 RNG，因而不会污染外部全局随机状态。
    边界：并列最高时保留先出现的运行；``restarts`` 必须至少为一。
    关键点：每次运行在没有严格改善邻居时停止，保证单次目标值单调提升。
    """
    if restarts < 1:
        raise ValueError("重启次数至少为 1")
    generator = random.Random(seed)
    best_state: State | None = None
    best_score = float("-inf")
    run_scores: list[float] = []
    for _ in range(restarts):
        current = sample_start(generator)
        current_score = objective(current)
        while True:
            candidate = current
            candidate_score = current_score
            for neighbor in neighbors(current):
                score = objective(neighbor)
                if score > candidate_score:
                    candidate, candidate_score = neighbor, score
            if candidate_score == current_score:
                break
            current, current_score = candidate, candidate_score
        run_scores.append(current_score)
        if current_score > best_score:
            best_state, best_score = current, current_score
    return RestartResult(best_state, best_score, tuple(run_scores))


if __name__ == "__main__":

    def starts(generator: random.Random) -> int:
        return generator.randrange(0, 9)

    def neighbors(value: int) -> list[int]:
        return [
            candidate for candidate in (value - 1, value + 1) if 0 <= candidate <= 8
        ]

    result = random_restart_hill_climb(
        starts, lambda value: -((value - 6) ** 2), neighbors, 8, seed=7
    )
    assert result.state == 6 and result.score == 0
    assert len(result.run_scores) == 8
    try:
        random_restart_hill_climb(starts, float, neighbors, 0)
        raise AssertionError("零次重启应被拒绝")
    except ValueError:
        pass
    print("002_random_restart_hill_climbing: all examples passed")
