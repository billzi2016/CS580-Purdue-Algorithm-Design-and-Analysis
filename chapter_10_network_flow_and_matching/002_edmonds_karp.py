"""
Edmonds-Karp 最大流：Ford-Fulkerson 的 BFS 最短增广路版本。

本文件的教学意图：
1. 对比 DFS 任意增广路和 BFS 最短增广路的差异。
2. 展示为什么“固定选择规则”能给出多项式时间复杂度 O(VE^2)。
3. 保留 parent 边记录细节，让路径回溯、瓶颈计算、残量更新都可审查。

Edmonds-Karp 仍然使用残量网络，只是每轮用 BFS 找边数最少的增广路。这个选择
避免了 Ford-Fulkerson 在某些图上反复走很差路径的问题。
"""

from collections import deque
from dataclasses import dataclass


@dataclass
class Edge:
    """残量网络边。

    original_capacity 只用于解释和调试；真正决定能否增广的是 capacity。
    """

    to: int
    rev: int
    capacity: int
    original_capacity: int


class EdmondsKarp:
    """使用 BFS 增广路的最大流求解器。"""

    def __init__(self, vertex_count: int) -> None:
        """初始化空图。"""

        if vertex_count <= 0:
            raise ValueError("vertex_count 必须为正数")
        self.graph: list[list[Edge]] = [[] for _ in range(vertex_count)]

    def add_edge(self, source: int, target: int, capacity: int) -> None:
        """加入一条容量边，并自动维护反向残量边。"""

        self._validate_vertex(source)
        self._validate_vertex(target)
        if capacity < 0:
            raise ValueError("capacity 不能为负数")

        forward = Edge(target, len(self.graph[target]), capacity, capacity)
        backward = Edge(source, len(self.graph[source]), 0, 0)
        self.graph[source].append(forward)
        self.graph[target].append(backward)

    def max_flow(self, source: int, sink: int) -> int:
        """返回 source 到 sink 的最大流值。"""

        self._validate_vertex(source)
        self._validate_vertex(sink)
        if source == sink:
            raise ValueError("source 和 sink 不能相同")

        total_flow = 0
        while True:
            parent = self._bfs_parent_edges(source, sink)
            if parent[sink] is None:
                return total_flow

            bottleneck = self._path_bottleneck(source, sink, parent)
            self._augment_path(source, sink, parent, bottleneck)
            total_flow += bottleneck

    def _bfs_parent_edges(
        self,
        source: int,
        sink: int,
    ) -> list[tuple[int, int] | None]:
        """用 BFS 找一条边数最少的增广路。

        parent[v] = (u, edge_index)，表示 BFS 第一次到达 v 时使用的是
        graph[u][edge_index]。第一次到达保证了边数最短。
        """

        parent: list[tuple[int, int] | None] = [None] * len(self.graph)
        parent[source] = (source, -1)
        queue: deque[int] = deque([source])

        while queue:
            vertex = queue.popleft()
            for edge_index, edge in enumerate(self.graph[vertex]):
                if edge.capacity == 0 or parent[edge.to] is not None:
                    continue
                parent[edge.to] = (vertex, edge_index)
                if edge.to == sink:
                    return parent
                queue.append(edge.to)

        return parent

    def _path_bottleneck(
        self,
        source: int,
        sink: int,
        parent: list[tuple[int, int] | None],
    ) -> int:
        """沿 parent 链回溯，计算本轮增广路上的最小残余容量。"""

        bottleneck = 10**18
        vertex = sink
        while vertex != source:
            previous, edge_index = self._require_parent(parent[vertex])
            edge = self.graph[previous][edge_index]
            bottleneck = min(bottleneck, edge.capacity)
            vertex = previous
        return bottleneck

    def _augment_path(
        self,
        source: int,
        sink: int,
        parent: list[tuple[int, int] | None],
        amount: int,
    ) -> None:
        """沿增广路推送 amount 流量并更新正反两类残量边。"""

        vertex = sink
        while vertex != source:
            previous, edge_index = self._require_parent(parent[vertex])
            edge = self.graph[previous][edge_index]
            edge.capacity -= amount
            self.graph[edge.to][edge.rev].capacity += amount
            vertex = previous

    def _require_parent(self, item: tuple[int, int] | None) -> tuple[int, int]:
        """把 Optional parent 转成确定值；缺失代表调用顺序有 bug。"""

        if item is None:
            raise RuntimeError("增广路径 parent 信息不完整")
        return item

    def _validate_vertex(self, vertex: int) -> None:
        """检查顶点编号合法性。"""

        if not 0 <= vertex < len(self.graph):
            raise IndexError("vertex 超出图的顶点范围")


def edmonds_karp_max_flow(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    source: int,
    sink: int,
) -> int:
    """函数式封装：用 Edmonds-Karp 计算最大流。"""

    solver = EdmondsKarp(vertex_count)
    for u, v, capacity in edges:
        solver.add_edge(u, v, capacity)
    return solver.max_flow(source, sink)


if __name__ == "__main__":
    classic_edges = [
        (0, 1, 16),
        (0, 2, 13),
        (1, 2, 10),
        (2, 1, 4),
        (1, 3, 12),
        (3, 2, 9),
        (2, 4, 14),
        (4, 3, 7),
        (3, 5, 20),
        (4, 5, 4),
    ]
    assert edmonds_karp_max_flow(6, classic_edges, 0, 5) == 23

    bottleneck_edges = [(0, 1, 100), (0, 2, 1), (1, 2, 1), (1, 3, 100), (2, 3, 100)]
    assert edmonds_karp_max_flow(4, bottleneck_edges, 0, 3) == 101

    zero_capacity_edges = [(0, 1, 0), (0, 2, 5), (2, 1, 3)]
    assert edmonds_karp_max_flow(3, zero_capacity_edges, 0, 1) == 3

    print("002_edmonds_karp: all examples passed")
