"""用禁忌搜索最大化离散目标函数。

适用场景：局部最优较多的组合优化。核心思想：即使候选变差也可移动，但最近访问状态在禁忌期限内不可选，除非满足优于历史最佳的特赦条件。
输入输出：输入状态、邻居和目标，输出历史最佳。时间 O(I×N×C)，空间 O(T)。
边界：邻居为空时停止；禁忌表按状态值记录过期迭代；需要状态可哈希。
"""

from __future__ import annotations
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Hashable, TypeVar


State = TypeVar("State", bound=Hashable)

@dataclass(frozen=True)
class TabuResult:
    state: object
    score: float


def tabu_search(initial: State, objective: Callable[[State], float], neighbors: Callable[[State], Iterable[State]], iterations: int = 100, tenure: int = 5) -> TabuResult:
    """执行带特赦准则的禁忌搜索，并返回历史最佳状态。

    关键点：禁忌仅限制重复访问，特赦允许候选若刷新全局最佳，避免错过真正改进。
    """
    if iterations < 0 or tenure < 1:
        raise ValueError("迭代次数和禁忌期限无效")
    current = best = initial
    current_score = best_score = objective(initial)
    forbidden: dict[State, int] = {}
    for step in range(iterations):
        choices = []
        for candidate in neighbors(current):
            score = objective(candidate)
            if forbidden.get(candidate, -1) <= step or score > best_score:
                choices.append((score, candidate))
        if not choices:
            break
        current_score, current = max(choices, key=lambda item: item[0])
        forbidden[current] = step + tenure
        if current_score > best_score:
            best, best_score = current, current_score
    return TabuResult(best, best_score)


if __name__ == "__main__":
    result = tabu_search(0, lambda value: -(value - 5) ** 2, lambda value: [value - 1, value + 1], iterations=20)
    assert result.state == 5 and result.score == 0
    assert tabu_search(3, float, lambda _: [], iterations=3).state == 3
    print("008_tabu_search: all examples passed")
