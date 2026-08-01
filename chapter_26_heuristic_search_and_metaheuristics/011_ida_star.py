"""用迭代加深 A*（IDA*）在显著更少内存下寻找最短路径。

适用场景：状态空间大但深度优先内存更合适的启发式路径搜索。核心思想：以 f=g+h 阈值做 DFS，失败后升到最小超限 f 值。
输入输出：输入后继、代价、启发式和目标判定，输出路径及代价。时间可能重复展开节点，空间 O(搜索深度)。
边界：边代价必须正以避免环；无解返回 ``None``；最优性依赖可采纳启发式。
"""

from __future__ import annotations
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Hashable, TypeVar

State = TypeVar("State", bound=Hashable)

@dataclass(frozen=True)
class IDAResult:
    path: tuple[object, ...]
    cost: float

def ida_star(start: State, is_goal: Callable[[State], bool], successors: Callable[[State], Iterable[tuple[State, float]]], heuristic: Callable[[State], float]) -> IDAResult | None:
    """执行 IDA*；每轮 DFS 都只允许 f 值不超过当前阈值。"""
    bound = heuristic(start)
    path = [start]
    while True:
        outcome = _search(path, 0.0, bound, is_goal, successors, heuristic)
        if isinstance(outcome, IDAResult):
            return outcome
        if outcome == float("inf"):
            return None
        bound = outcome

def _search(path: list[State], cost: float, bound: float, is_goal: Callable[[State], bool], successors: Callable[[State], Iterable[tuple[State, float]]], heuristic: Callable[[State], float]) -> IDAResult | float:
    state = path[-1]
    estimate = cost + heuristic(state)
    if estimate > bound:
        return estimate
    if is_goal(state):
        return IDAResult(tuple(path), cost)
    minimum = float("inf")
    for neighbor, edge_cost in successors(state):
        if edge_cost <= 0:
            raise ValueError("IDA* 示例要求边代价为正")
        if neighbor in path:
            continue
        path.append(neighbor)
        outcome = _search(path, cost + edge_cost, bound, is_goal, successors, heuristic)
        if isinstance(outcome, IDAResult):
            return outcome
        minimum = min(minimum, outcome)
        path.pop()
    return minimum

if __name__ == "__main__":
    graph = {0: [(1, 1), (2, 3)], 1: [(2, 1), (3, 4)], 2: [(3, 1)], 3: []}
    result = ida_star(0, lambda state: state == 3, graph.__getitem__, {0: 3, 1: 2, 2: 1, 3: 0}.__getitem__)
    assert result == IDAResult((0, 1, 2, 3), 3)
    assert ida_star(3, lambda state: state == 0, graph.__getitem__, lambda _: 0) is None
    print("011_ida_star: all examples passed")
