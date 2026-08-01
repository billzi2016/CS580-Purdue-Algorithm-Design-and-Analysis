"""
文件意图：
    本文件手写实现 Prim 最小生成树算法，用于从一个起点逐步扩展最小生成树。

适用场景：
    无向连通带权图的最小生成树。若输入图不连通，本实现会返回起点所在连通分量
    的最小生成树，并明确只覆盖该分量。

核心思想：
    维护已加入树的节点集合，每次选择一条连接“树内节点”和“树外节点”的最小权边。
    使用最小堆高效取得当前最小横切边。

输入输出：
    输入无向带权邻接表和起点，返回选中边及总权重。

时间复杂度：
    O(E log E)

空间复杂度：
    O(V + E)
"""

import heapq
from collections.abc import Hashable

Node = Hashable
Graph = dict[Node, list[tuple[Node, float]]]
TreeEdge = tuple[Node, Node, float]


def prim_minimum_spanning_tree(graph: Graph, start: Node) -> tuple[list[TreeEdge], float]:
    """
    从 start 所在连通分量中计算最小生成树。

    参数：
        graph: 无向带权邻接表。每条无向边应在两个方向都出现。
        start: 起点。

    返回：
        (selected_edges, total_weight)。
    """
    visited: set[Node] = {start}
    selected: list[TreeEdge] = []
    total_weight = 0.0
    heap: list[tuple[float, Node, Node]] = []

    for neighbor, weight in graph.get(start, []):
        heapq.heappush(heap, (weight, start, neighbor))

    while heap:
        weight, parent, node = heapq.heappop(heap)
        if node in visited:
            continue

        visited.add(node)
        selected.append((parent, node, weight))
        total_weight += weight

        for neighbor, next_weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(heap, (next_weight, node, neighbor))

    return selected, total_weight


if __name__ == "__main__":
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("A", 1), ("C", 2), ("D", 5)],
        "C": [("A", 4), ("B", 2), ("D", 3)],
        "D": [("B", 5), ("C", 3)],
    }
    mst_edges, total = prim_minimum_spanning_tree(graph, "A")
    assert total == 6.0
    assert len(mst_edges) == 3
    assert {frozenset((u, v)) for u, v, _ in mst_edges} == {
        frozenset(("A", "B")),
        frozenset(("B", "C")),
        frozenset(("C", "D")),
    }

    isolated_edges, isolated_total = prim_minimum_spanning_tree({}, "X")
    assert isolated_edges == []
    assert isolated_total == 0.0

    disconnected_graph = {"A": [("B", 1)], "B": [("A", 1)], "C": []}
    component_edges, component_total = prim_minimum_spanning_tree(disconnected_graph, "C")
    assert component_edges == []
    assert component_total == 0.0

    print("003_prim: all examples passed")
