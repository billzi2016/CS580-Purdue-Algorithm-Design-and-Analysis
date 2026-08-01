"""
文件意图：
    本文件手写实现 Kruskal 最小生成树算法，用于在无向带权图中选择总权重最小的生成树。

适用场景：
    无向连通图的最小生成树；如果图不连通，则返回最小生成森林。

核心思想：
    按边权从小到大考虑每条边。若当前边连接两个不同连通分量，则加入结果；
    否则加入该边会形成环，必须跳过。并查集用于高效维护连通分量。

输入输出：
    输入节点集合和无向边列表，返回生成树/森林边集及总权重。

时间复杂度：
    O(E log E)

空间复杂度：
    O(V)
"""

from collections.abc import Hashable, Iterable

Node = Hashable
Edge = tuple[Node, Node, float]


class UnionFind:
    """
    Kruskal 内部使用的轻量并查集。
    """

    def __init__(self, nodes: Iterable[Node]) -> None:
        unique_nodes = list(dict.fromkeys(nodes))
        self.parent = {node: node for node in unique_nodes}
        self.size = {node: 1 for node in unique_nodes}

    def find(self, node: Node) -> Node:
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, first: Node, second: Node) -> bool:
        root_first = self.find(first)
        root_second = self.find(second)
        if root_first == root_second:
            return False
        if self.size[root_first] < self.size[root_second]:
            root_first, root_second = root_second, root_first
        self.parent[root_second] = root_first
        self.size[root_first] += self.size[root_second]
        return True


def kruskal_minimum_spanning_forest(
    nodes: Iterable[Node], edges: list[Edge]
) -> tuple[list[Edge], float]:
    """
    使用 Kruskal 算法计算最小生成树或最小生成森林。

    参数：
        nodes: 图中节点集合。
        edges: 无向边列表，每条边为 (u, v, weight)。

    返回：
        (selected_edges, total_weight)。
    """
    node_list = list(dict.fromkeys(nodes))
    union_find = UnionFind(node_list)
    selected: list[Edge] = []
    total_weight = 0.0

    for start, end, weight in sorted(edges, key=lambda edge: edge[2]):
        if start not in union_find.parent or end not in union_find.parent:
            raise ValueError("边中出现了 nodes 未包含的节点")

        if union_find.union(start, end):
            selected.append((start, end, weight))
            total_weight += weight

    return selected, total_weight


if __name__ == "__main__":
    nodes = ["A", "B", "C", "D"]
    edges = [
        ("A", "B", 1),
        ("A", "C", 4),
        ("B", "C", 2),
        ("B", "D", 5),
        ("C", "D", 3),
    ]
    mst_edges, total = kruskal_minimum_spanning_forest(nodes, edges)
    assert total == 6.0
    assert len(mst_edges) == 3
    assert {frozenset((u, v)) for u, v, _ in mst_edges} == {
        frozenset(("A", "B")),
        frozenset(("B", "C")),
        frozenset(("C", "D")),
    }

    forest_edges, forest_total = kruskal_minimum_spanning_forest(
        ["A", "B", "C"], [("A", "B", 7)]
    )
    assert forest_edges == [("A", "B", 7)]
    assert forest_total == 7.0

    try:
        kruskal_minimum_spanning_forest(["A"], [("A", "B", 1)])
        raise AssertionError("未知节点必须抛出 ValueError")
    except ValueError:
        pass

    print("002_kruskal: all examples passed")
