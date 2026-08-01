"""
Dinic 最大流：BFS 分层图 + DFS 阻塞流。

本文件的教学意图：
1. 展示从 Edmonds-Karp 到 Dinic 的关键优化：一次 BFS 后不只增广一条路，
   而是在同一张分层图里尽量推成阻塞流。
2. 手写 current arc（当前弧）优化，避免 DFS 反复扫描已经证明不可用的边。
3. 用清晰的残量边结构支持平行边、反向撤销和后续最小割复用。

复杂度提示：
- 一般图 Dinic 为 O(V^2 E)。
- 单位容量图、二分图匹配等特殊场景还有更强界，但这里保持通用实现。
"""

from collections import deque
from dataclasses import dataclass


@dataclass
class Edge:
    """Dinic 残量网络边。"""

    to: int
    rev: int
    capacity: int


class Dinic:
    """通用整数容量最大流求解器。"""

    def __init__(self, vertex_count: int) -> None:
        """初始化 vertex_count 个顶点的残量网络。"""

        if vertex_count <= 0:
            raise ValueError("vertex_count 必须为正数")
        self.graph: list[list[Edge]] = [[] for _ in range(vertex_count)]
        self.level = [-1] * vertex_count
        self.next_edge = [0] * vertex_count

    def add_edge(self, source: int, target: int, capacity: int) -> None:
        """加入一条有向容量边，并建立反向残量边。"""

        self._validate_vertex(source)
        self._validate_vertex(target)
        if capacity < 0:
            raise ValueError("capacity 不能为负数")

        forward = Edge(target, len(self.graph[target]), capacity)
        backward = Edge(source, len(self.graph[source]), 0)
        self.graph[source].append(forward)
        self.graph[target].append(backward)

    def max_flow(self, source: int, sink: int) -> int:
        """计算 source 到 sink 的最大流。"""

        self._validate_vertex(source)
        self._validate_vertex(sink)
        if source == sink:
            raise ValueError("source 和 sink 不能相同")

        total_flow = 0
        infinite = 10**18

        while self._build_level_graph(source, sink):
            self.next_edge = [0] * len(self.graph)
            while True:
                pushed = self._send_blocking_flow(source, sink, infinite)
                if pushed == 0:
                    break
                total_flow += pushed

        return total_flow

    def _build_level_graph(self, source: int, sink: int) -> bool:
        """BFS 构造分层图；返回 sink 是否可达。"""

        self.level = [-1] * len(self.graph)
        self.level[source] = 0
        queue: deque[int] = deque([source])

        while queue:
            vertex = queue.popleft()
            for edge in self.graph[vertex]:
                if edge.capacity == 0 or self.level[edge.to] != -1:
                    continue
                self.level[edge.to] = self.level[vertex] + 1
                queue.append(edge.to)

        return self.level[sink] != -1

    def _send_blocking_flow(self, vertex: int, sink: int, flow_limit: int) -> int:
        """在当前分层图中 DFS 推送阻塞流的一部分。

        next_edge[vertex] 是当前弧优化：一条边如果已经无法继续贡献流量，就不再
        被后续 DFS 重复扫描。这个小细节对 Dinic 的实际性能非常关键。
        """

        if vertex == sink:
            return flow_limit

        while self.next_edge[vertex] < len(self.graph[vertex]):
            edge_index = self.next_edge[vertex]
            edge = self.graph[vertex][edge_index]

            if edge.capacity > 0 and self.level[edge.to] == self.level[vertex] + 1:
                pushed = self._send_blocking_flow(
                    edge.to,
                    sink,
                    min(flow_limit, edge.capacity),
                )
                if pushed > 0:
                    edge.capacity -= pushed
                    self.graph[edge.to][edge.rev].capacity += pushed
                    return pushed

            # 当前边不能再带来有效增广，移动当前弧指针。
            self.next_edge[vertex] += 1

        return 0

    def _validate_vertex(self, vertex: int) -> None:
        """检查顶点编号是否有效。"""

        if not 0 <= vertex < len(self.graph):
            raise IndexError("vertex 超出图的顶点范围")


def dinic_max_flow(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    source: int,
    sink: int,
) -> int:
    """函数式封装：用 Dinic 计算最大流。"""

    solver = Dinic(vertex_count)
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
    assert dinic_max_flow(6, classic_edges, 0, 5) == 23

    layered_edges = [
        (0, 1, 5),
        (0, 2, 5),
        (1, 3, 4),
        (2, 3, 6),
        (3, 4, 7),
    ]
    assert dinic_max_flow(5, layered_edges, 0, 4) == 7

    no_path_edges = [(0, 1, 10), (2, 3, 10)]
    assert dinic_max_flow(4, no_path_edges, 0, 3) == 0

    print("003_dinic: all examples passed")
