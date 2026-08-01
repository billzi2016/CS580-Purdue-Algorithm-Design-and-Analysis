"""
文件意图：
    本文件手写实现 DAG 最短路径算法，用于在有向无环图中按拓扑序松弛边。

适用场景：
    图必须是 DAG。边权可以为负，因为 DAG 中不存在环，不会出现负权环问题。

核心思想：
    先拓扑排序，再按拓扑序从前到后松弛每条边。由于所有前驱都会先于后继处理，
    每个节点被处理时其最短距离已经由所有可能前驱更新完毕。

输入输出：
    输入 DAG 带权邻接表和起点，返回距离表与父节点表。

时间复杂度：
    O(V + E)

空间复杂度：
    O(V)
"""

from collections import deque
from collections.abc import Hashable

Node = Hashable
WeightedGraph = dict[Node, list[tuple[Node, float]]]


def dag_shortest_path(
    graph: WeightedGraph, source: Node
) -> tuple[dict[Node, float], dict[Node, Node | None]]:
    """
    计算 DAG 中 source 到所有节点的最短路径。
    """
    order = _topological_sort_weighted_graph(graph)
    if source not in order:
        order.append(source)

    distance = {node: float("inf") for node in order}
    parent: dict[Node, Node | None] = {node: None for node in order}
    distance[source] = 0.0

    for node in order:
        if distance[node] == float("inf"):
            continue

        for neighbor, weight in graph.get(node, []):
            candidate = distance[node] + weight
            if candidate < distance.get(neighbor, float("inf")):
                distance[neighbor] = candidate
                parent[neighbor] = node

    return distance, parent


def _topological_sort_weighted_graph(graph: WeightedGraph) -> list[Node]:
    """
    对带权 DAG 执行拓扑排序。
    """
    nodes = _collect_all_nodes(graph)
    indegree = {node: 0 for node in nodes}

    for node in nodes:
        for neighbor, _ in graph.get(node, []):
            indegree[neighbor] += 1

    queue: deque[Node] = deque([node for node in nodes if indegree[node] == 0])
    order: list[Node] = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor, _ in graph.get(node, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(nodes):
        raise ValueError("输入图不是 DAG，不能使用 DAG 最短路径算法")

    return order


def _collect_all_nodes(graph: WeightedGraph) -> list[Node]:
    """
    收集 key 和邻接表值中出现的所有节点。
    """
    nodes: list[Node] = []
    seen: set[Node] = set()

    for node, edges in graph.items():
        if node not in seen:
            nodes.append(node)
            seen.add(node)
        for neighbor, _ in edges:
            if neighbor not in seen:
                nodes.append(neighbor)
                seen.add(neighbor)

    return nodes


if __name__ == "__main__":
    graph = {
        "S": [("A", 2), ("B", 5)],
        "A": [("C", -3)],
        "B": [("C", 1)],
        "C": [("D", 4)],
        "D": [],
    }
    distance, parent = dag_shortest_path(graph, "S")
    assert distance["S"] == 0.0
    assert distance["A"] == 2.0
    assert distance["C"] == -1.0
    assert distance["D"] == 3.0
    assert parent["D"] == "C"

    isolated_distance, isolated_parent = dag_shortest_path({}, "X")
    assert isolated_distance == {"X": 0.0}
    assert isolated_parent == {"X": None}

    try:
        dag_shortest_path({"A": [("B", 1)], "B": [("A", 1)]}, "A")
        raise AssertionError("有环图必须抛出 ValueError")
    except ValueError:
        pass

    print("005_dag_shortest_path: all examples passed")
