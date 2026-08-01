"""用爬山法在离散状态空间中寻找局部最大值。

适用场景：邻居关系容易枚举、只需快速获得局部可行解的组合优化问题。
核心思想：每轮检查当前状态所有邻居，仅在严格改进时移动，因此目标值单调上升。
输入输出：输入起点、目标函数和邻居生成函数，输出最终状态与目标值。
时间复杂度：O(I×N×C)，I 为迭代次数、N 为每轮邻居数、C 为一次目标计算成本；空间 O(N)。
边界情况：没有邻居、平台或已是局部最优时立即停止；目标函数应返回可比较的数值。
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TypeVar


State = TypeVar("State")


@dataclass(frozen=True)
class HillClimbResult:
    """爬山过程的局部最优状态、分数及实际移动次数。"""

    state: object
    score: float
    steps: int


def hill_climb(
    initial_state: State,
    objective: Callable[[State], float],
    neighbors: Callable[[State], Iterable[State]],
    max_steps: int = 1_000,
) -> HillClimbResult:
    """执行最陡上升爬山法。

    参数：起点、最大化目标、邻居生成器和移动上限。返回局部最优结果。
    边界：``max_steps`` 必须非负；同分邻居不会移动，避免在平台上循环。
    关键点：扫描完全部邻居再选择最佳者，避免邻居枚举顺序改变结果质量。
    """
    if max_steps < 0:
        raise ValueError("max_steps 不能为负")
    current = initial_state
    current_score = objective(current)
    for step in range(max_steps):
        best_state = current
        best_score = current_score
        for candidate in neighbors(current):
            candidate_score = objective(candidate)
            if candidate_score > best_score:
                best_state = candidate
                best_score = candidate_score
        if best_score == current_score:
            return HillClimbResult(current, current_score, step)
        current, current_score = best_state, best_score
    return HillClimbResult(current, current_score, max_steps)


if __name__ == "__main__":
    def integer_neighbors(value: int) -> list[int]:
        return [value - 1, value + 1]

    result = hill_climb(0, lambda value: -(value - 4) ** 2, integer_neighbors)
    assert result.state == 4
    assert result.score == 0
    assert result.steps == 4
    plateau = hill_climb(5, lambda _: 1, integer_neighbors)
    assert plateau.state == 5 and plateau.steps == 0
    print("001_hill_climbing: all examples passed")
