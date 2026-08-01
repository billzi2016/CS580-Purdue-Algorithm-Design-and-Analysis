"""
文件意图：
    本文件手写实现 0-1 BFS，用于边权只可能为 0 或 1 的单源最短路径问题。

适用场景：
    图的边权只有 0 和 1。此时可以用双端队列替代 Dijkstra 的优先队列，
    得到 O(V + E) 的时间复杂度。

核心思想：
    松弛 0 权边时把节点放到队首，松弛 1 权边时放到队尾。这样队列始终
    近似保持按距离从小到大处理。

输入输出：
    输入 0/1 带权图和起点，返回距离表。

时间复杂度：
    O(V + E)

空间复杂度：
    O(V)
"""

from collections import deque
from collections.abc import Hashable

Node = Hashable
ZeroOneGraph = dict[Node, list[tuple[Node, int]]]


def zero_one_bfs(graph: ZeroOneGraph, source: Node) -> dict[Node, int]:
    """
    计算 source 到所有可达节点的最短 0/1 权重距离。
    """
    _validate_zero_one_edges(graph)

    distance: dict[Node, int] = {source: 0}
    queue: deque[Node] = deque([source])

    while queue:
        node = queue.popleft()

        for neighbor, weight in graph.get(node, []):
            candidate = distance[node] + weight
            if candidate < distance.get(neighbor, 10**18):
                distance[neighbor] = candidate

                if weight == 0:
                    queue.appendleft(neighbor)
                else:
                    queue.append(neighbor)

    return distance


def _validate_zero_one_edges(graph: ZeroOneGraph) -> None:
    """
    校验边权必须为 0 或 1。
    """
    for node, edges in graph.items():
        for neighbor, weight in edges:
            if weight not in (0, 1):
                raise ValueError(f"0-1 BFS 只支持 0/1 边权：{node} -> {neighbor} 权重 {weight}")


if __name__ == "__main__":
    graph = {
        "S": [("A", 0), ("B", 1)],
        "A": [("C", 1)],
        "B": [("C", 0)],
        "C": [],
    }
    assert zero_one_bfs(graph, "S") == {"S": 0, "A": 0, "B": 1, "C": 1}
    assert zero_one_bfs({}, "X") == {"X": 0}

    try:
        zero_one_bfs({"A": [("B", 2)]}, "A")
        raise AssertionError("非法边权必须抛出 ValueError")
    except ValueError:
        pass

    print("004_zero_one_bfs: all examples passed")
