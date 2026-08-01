"""
Ford-Fulkerson 最大流：用残量网络和任意增广路反复提升 s-t 流量。

本文件的教学意图：
1. 展示最大流问题的核心建模：容量、流量守恒、残量边、反向边。
2. 保留最原始的 DFS 增广写法，便于理解 Edmonds-Karp 和 Dinic 的改进点。
3. 明确说明适用边界：当容量为整数时算法会终止；如果用浮点或病态路径选择，
   理论上可能出现非常慢甚至不收敛的情况。

实现约束：
- 不调用任何图论库，残量网络完全手写。
- 平行边通过残量边自然支持。
- 每次 add_edge 都同时加入一条容量为 0 的反向边，用于之后撤销部分流量。
"""

from dataclasses import dataclass


@dataclass
class Edge:
    """残量网络中的一条有向边。

    to:
        边指向的顶点。
    rev:
        这条边对应反向边在邻接表 graph[to] 中的下标。
    capacity:
        当前残余容量。注意这里存的是“还能继续推多少流”，不是原始容量。
    """

    to: int
    rev: int
    capacity: int


class FordFulkerson:
    """使用 DFS 寻找增广路的 Ford-Fulkerson 最大流求解器。"""

    def __init__(self, vertex_count: int) -> None:
        """创建一个含 vertex_count 个点的空残量网络。"""

        if vertex_count <= 0:
            raise ValueError("vertex_count 必须为正数")
        self.graph: list[list[Edge]] = [[] for _ in range(vertex_count)]

    def add_edge(self, source: int, target: int, capacity: int) -> None:
        """加入一条从 source 到 target、容量为 capacity 的有向边。

        Ford-Fulkerson 要求剩余容量可以被减少、反向容量可以被增加，所以每条
        原始边必须配一条反向边。反向边初始容量为 0，表示一开始没有可撤销流量。
        """

        self._validate_vertex(source)
        self._validate_vertex(target)
        if capacity < 0:
            raise ValueError("capacity 不能为负数")

        forward = Edge(target, len(self.graph[target]), capacity)
        backward = Edge(source, len(self.graph[source]), 0)
        self.graph[source].append(forward)
        self.graph[target].append(backward)

    def max_flow(self, source: int, sink: int) -> int:
        """返回 source 到 sink 的最大流值。"""

        self._validate_vertex(source)
        self._validate_vertex(sink)
        if source == sink:
            raise ValueError("source 和 sink 不能相同")

        total_flow = 0
        infinite = 10**18

        while True:
            visited = [False] * len(self.graph)
            pushed = self._dfs_augment(source, sink, infinite, visited)
            if pushed == 0:
                # 找不到任何可增广路径时，根据最大流最小割定理，当前流就是最大流。
                return total_flow
            total_flow += pushed

    def _dfs_augment(
        self,
        vertex: int,
        sink: int,
        available_flow: int,
        visited: list[bool],
    ) -> int:
        """从 vertex 出发找一条到 sink 的增广路，并返回本次实际推送的流量。"""

        if vertex == sink:
            return available_flow

        visited[vertex] = True
        for edge in self.graph[vertex]:
            if edge.capacity == 0 or visited[edge.to]:
                continue

            # 路径瓶颈由目前路径可用流量和这条边的残余容量共同决定。
            pushed = self._dfs_augment(
                edge.to,
                sink,
                min(available_flow, edge.capacity),
                visited,
            )
            if pushed == 0:
                continue

            # 正向边减少残余容量，反向边增加残余容量；这一步等价于修改流量。
            edge.capacity -= pushed
            self.graph[edge.to][edge.rev].capacity += pushed
            return pushed

        return 0

    def _validate_vertex(self, vertex: int) -> None:
        """检查顶点下标是否落在图的范围内。"""

        if not 0 <= vertex < len(self.graph):
            raise IndexError("vertex 超出图的顶点范围")


def ford_fulkerson_max_flow(
    vertex_count: int,
    edges: list[tuple[int, int, int]],
    source: int,
    sink: int,
) -> int:
    """函数式封装：根据边列表构图并返回最大流。

    edges 中每个三元组为 (u, v, capacity)，表示一条有向容量边。这个封装适合
    LeetCode / Codeforces 风格输入，也方便和后续 Edmonds-Karp、Dinic 对比。
    """

    solver = FordFulkerson(vertex_count)
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
    assert ford_fulkerson_max_flow(6, classic_edges, 0, 5) == 23

    parallel_edges = [(0, 1, 3), (0, 1, 2), (1, 2, 4), (0, 2, 1)]
    assert ford_fulkerson_max_flow(3, parallel_edges, 0, 2) == 5

    disconnected_edges = [(0, 1, 7), (2, 3, 5)]
    assert ford_fulkerson_max_flow(4, disconnected_edges, 0, 3) == 0

    print("001_ford_fulkerson: all examples passed")
