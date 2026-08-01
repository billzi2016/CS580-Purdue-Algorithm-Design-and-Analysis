"""用 A* 搜索带非负边权图的最短路径。

适用场景：有可采纳启发式的路径规划。核心思想：优先扩展 f=g+h 最小的节点，并在找到更短 g 值时松弛。
输入输出：输入图、起点、目标、启发式，输出路径与代价。时间取决于展开节点数，空间同样为 O(展开节点数)。
边界：边权必须非负；不可达返回 ``None``；最优性要求启发式不高估真实剩余代价。
"""

from __future__ import annotations
import heapq
from collections.abc import Callable
from dataclasses import dataclass
from typing import Hashable, TypeVar

Node = TypeVar("Node", bound=Hashable)


@dataclass(frozen=True)
class PathResult:
    path: tuple[object, ...]
    cost: float


def a_star(
    graph: dict[Node, list[tuple[Node, float]]],
    start: Node,
    goal: Node,
    heuristic: Callable[[Node], float],
) -> PathResult | None:
    """返回从 start 到 goal 的最短路径；没有路径时返回 ``None``。"""
    queue: list[tuple[float, int, Node]] = [(heuristic(start), 0, start)]
    costs, parents, counter = {start: 0.0}, {start: None}, 0
    while queue:
        _, _, node = heapq.heappop(queue)
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parents[node]
            return PathResult(tuple(reversed(path)), costs[goal])
        for neighbor, edge_cost in graph.get(node, []):
            if edge_cost < 0:
                raise ValueError("A* 不支持负边权")
            candidate = costs[node] + edge_cost
            if candidate < costs.get(neighbor, float("inf")):
                costs[neighbor], parents[neighbor] = candidate, node
                counter += 1
                heapq.heappush(
                    queue, (candidate + heuristic(neighbor), counter, neighbor)
                )
    return None


if __name__ == "__main__":
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 1), ("D", 5)],
        "C": [("D", 1)],
        "D": [],
    }
    result = a_star(graph, "A", "D", {"A": 3, "B": 2, "C": 1, "D": 0}.__getitem__)
    assert result == PathResult(("A", "B", "C", "D"), 3)
    assert a_star(graph, "D", "A", lambda _: 0) is None
    print("010_a_star: all examples passed")
