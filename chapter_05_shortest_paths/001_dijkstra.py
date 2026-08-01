"""
文件意图：
    本文件手写实现 Dijkstra 最短路径算法，用于计算非负边权图中的单源最短路径。

适用场景：
    图中所有边权都必须非负。若存在负权边，应使用 Bellman-Ford 或 Johnson 等算法。

核心思想：
    使用优先队列维护当前已知的最短候选距离。每次取出距离最小的节点时，
    在非负边权前提下，该节点的最短距离已经确定；随后用它松弛所有出边。

输入输出：
    输入带权有向图邻接表和起点，返回距离表与父节点表。

时间复杂度：
    O((V + E) log V)

空间复杂度：
    O(V)
"""

import heapq
from collections.abc import Hashable

Node = Hashable
WeightedGraph = dict[Node, list[tuple[Node, float]]]


def dijkstra(
    graph: WeightedGraph, source: Node
) -> tuple[dict[Node, float], dict[Node, Node | None]]:
    """
    计算 source 到所有可达节点的最短距离。

    参数：
        graph: 带权邻接表，graph[u] = [(v, weight), ...]。
        source: 起点。

    返回：
        (distance, parent)：
            distance[v] 是 source 到 v 的最短距离；
            parent[v] 是最短路径树中 v 的前驱节点。

    边界情况：
        source 不在 graph 中时，将其视为孤立节点。
    """
    _validate_non_negative_edges(graph)

    distance: dict[Node, float] = {source: 0.0}
    parent: dict[Node, Node | None] = {source: None}
    heap: list[tuple[float, Node]] = [(0.0, source)]

    while heap:
        current_distance, node = heapq.heappop(heap)

        # 如果堆中弹出的是旧距离，说明该候选已经被更短路径替代，直接跳过。
        if current_distance != distance[node]:
            continue

        for neighbor, weight in graph.get(node, []):
            candidate = current_distance + weight
            if candidate < distance.get(neighbor, float("inf")):
                distance[neighbor] = candidate
                parent[neighbor] = node
                heapq.heappush(heap, (candidate, neighbor))

    return distance, parent


def reconstruct_path(parent: dict[Node, Node | None], target: Node) -> list[Node]:
    """
    根据 Dijkstra 父节点表还原从 source 到 target 的最短路径。
    """
    if target not in parent:
        return []

    path: list[Node] = []
    current: Node | None = target
    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def _validate_non_negative_edges(graph: WeightedGraph) -> None:
    """
    校验所有边权非负，避免错误使用 Dijkstra。
    """
    for node, edges in graph.items():
        for neighbor, weight in edges:
            if weight < 0:
                raise ValueError(
                    f"Dijkstra 不支持负权边：{node} -> {neighbor} 权重 {weight}"
                )


if __name__ == "__main__":
    graph = {
        "A": [("B", 4), ("C", 1)],
        "B": [("D", 1)],
        "C": [("B", 2), ("D", 5)],
        "D": [],
    }
    distance, parent = dijkstra(graph, "A")
    assert distance == {"A": 0.0, "C": 1.0, "B": 3.0, "D": 4.0}
    assert reconstruct_path(parent, "D") == ["A", "C", "B", "D"]
    assert reconstruct_path(parent, "Z") == []

    isolated_distance, isolated_parent = dijkstra({}, "S")
    assert isolated_distance == {"S": 0.0}
    assert isolated_parent == {"S": None}

    try:
        dijkstra({"A": [("B", -1)]}, "A")
        raise AssertionError("负权边必须抛出 ValueError")
    except ValueError:
        pass

    print("001_dijkstra: all examples passed")
