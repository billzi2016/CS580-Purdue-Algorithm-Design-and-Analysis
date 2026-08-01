"""
文件意图：
    本文件手写实现次小生成树计算，用于找出权重大于等于 MST 的最佳替代生成树。

适用场景：
    分析最小生成树的稳定性，或需要知道替换一条边后的最优生成树。

核心思想：
    先用 Kruskal 求一棵 MST。对于每条非 MST 边 (u, v, w)，把它加入 MST 会形成
    一个环。要恢复生成树，必须删除该环中一条边；为了总权重尽量小，应删除
    u 到 v 的 MST 路径上权重最大的边。

输入输出：
    输入节点集合和无向边列表，返回 MST 权重和次小生成树权重。

时间复杂度：
    教学版 O(EV)，因为每条非树边都在 MST 上 DFS 查找路径最大边。

空间复杂度：
    O(V + E)
"""

from collections.abc import Hashable, Iterable

Node = Hashable
Edge = tuple[Node, Node, float]


class UnionFind:
    """
    次小生成树内部使用的并查集。
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


def second_best_mst_weight(
    nodes: Iterable[Node], edges: list[Edge]
) -> tuple[float, float | None]:
    """
    计算 MST 权重和次小生成树权重。

    返回：
        (mst_weight, second_best_weight)。如果不存在次小生成树，second_best_weight 为 None。
    """
    node_list = list(dict.fromkeys(nodes))
    mst_edges, mst_weight, selected_indices = _kruskal_with_indices(node_list, edges)

    if len(mst_edges) != max(0, len(node_list) - 1):
        raise ValueError("输入图不连通，不存在覆盖所有节点的 MST")

    mst_graph = _build_tree_adjacency(node_list, mst_edges)
    best_candidate = float("inf")

    for index, (start, end, weight) in enumerate(edges):
        if index in selected_indices:
            continue

        max_edge_on_path = _max_edge_weight_on_tree_path(mst_graph, start, end)
        candidate = mst_weight + weight - max_edge_on_path

        # 允许相同权重的另一棵 MST 作为 second-best；如果要求 strictly larger，可改为 candidate > mst_weight。
        if candidate >= mst_weight and candidate < best_candidate:
            best_candidate = candidate

    return mst_weight, None if best_candidate == float("inf") else best_candidate


def _kruskal_with_indices(
    nodes: list[Node], edges: list[Edge]
) -> tuple[list[Edge], float, set[int]]:
    """
    Kruskal 求 MST，同时记录被选中的原始边下标。
    """
    union_find = UnionFind(nodes)
    selected_edges: list[Edge] = []
    selected_indices: set[int] = set()
    total_weight = 0.0

    indexed_edges = sorted(enumerate(edges), key=lambda item: item[1][2])
    for index, (start, end, weight) in indexed_edges:
        if start not in union_find.parent or end not in union_find.parent:
            raise ValueError("边中出现了 nodes 未包含的节点")
        if union_find.union(start, end):
            selected_edges.append((start, end, weight))
            selected_indices.add(index)
            total_weight += weight

    return selected_edges, total_weight, selected_indices


def _build_tree_adjacency(
    nodes: list[Node], edges: list[Edge]
) -> dict[Node, list[tuple[Node, float]]]:
    """
    根据 MST 边构建无向树邻接表。
    """
    graph: dict[Node, list[tuple[Node, float]]] = {node: [] for node in nodes}
    for start, end, weight in edges:
        graph[start].append((end, weight))
        graph[end].append((start, weight))
    return graph


def _max_edge_weight_on_tree_path(
    graph: dict[Node, list[tuple[Node, float]]], start: Node, end: Node
) -> float:
    """
    在树中查找 start 到 end 路径上的最大边权。
    """
    stack: list[tuple[Node, Node | None, float]] = [(start, None, float("-inf"))]

    while stack:
        node, parent, current_max = stack.pop()
        if node == end:
            return current_max

        for neighbor, weight in graph.get(node, []):
            if neighbor != parent:
                stack.append((neighbor, node, max(current_max, weight)))

    raise ValueError("MST 路径查找失败，输入图可能不连通")


if __name__ == "__main__":
    nodes = ["A", "B", "C", "D"]
    edges = [
        ("A", "B", 1),
        ("B", "C", 2),
        ("C", "D", 3),
        ("A", "C", 4),
        ("B", "D", 5),
    ]
    assert second_best_mst_weight(nodes, edges) == (6.0, 8.0)

    tied_edges = [
        ("A", "B", 1),
        ("B", "C", 1),
        ("A", "C", 1),
    ]
    assert second_best_mst_weight(["A", "B", "C"], tied_edges) == (2.0, 2.0)

    try:
        second_best_mst_weight(["A", "B", "C"], [("A", "B", 1)])
        raise AssertionError("不连通图必须抛出 ValueError")
    except ValueError:
        pass

    print("005_second_best_mst: all examples passed")
