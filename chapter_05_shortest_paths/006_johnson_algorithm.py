"""
文件意图：
    本文件手写实现 Johnson 算法，用于稀疏图中的所有点对最短路径。

适用场景：
    有向图可以包含负权边，但不能包含负权环。相较 Floyd-Warshall 的 O(V^3)，
    Johnson 在稀疏图上通常更适合。

核心思想：
    先添加超级源点并用 Bellman-Ford 计算势函数 h。随后将每条边重新赋权为
    w'(u, v) = w(u, v) + h(u) - h(v)，使所有新边权非负。再从每个节点运行
    Dijkstra，最后把距离还原回原始权重。

输入输出：
    输入节点列表和边列表，返回所有点对最短距离。

时间复杂度：
    O(VE + V(E log V))

空间复杂度：
    O(V^2 + E)
"""

from collections.abc import Hashable

Node = Hashable
Edge = tuple[Node, Node, float]
WeightedGraph = dict[Node, list[tuple[Node, float]]]


class _MinHeap:
    """Johnson 重赋权后 Dijkstra 使用的手写二叉最小堆。"""
    def __init__(self) -> None:
        self.data: list[tuple[float, Node]] = []

    def push(self, item: tuple[float, Node]) -> None:
        """插入条目，并通过向上交换恢复父节点不大于子节点的不变量。"""
        self.data.append(item)
        index = len(self.data) - 1
        while index and self.data[(index - 1) // 2][0] > item[0]:
            self.data[index] = self.data[(index - 1) // 2]
            index = (index - 1) // 2
        self.data[index] = item

    def pop(self) -> tuple[float, Node]:
        """返回最小距离条目；空堆调用无效。"""
        result = self.data[0]
        last = self.data.pop()
        if self.data:
            index = 0
            while index * 2 + 1 < len(self.data):
                child = index * 2 + 1
                if child + 1 < len(self.data) and self.data[child + 1][0] < self.data[child][0]:
                    child += 1
                if self.data[child][0] >= last[0]:
                    break
                self.data[index] = self.data[child]
                index = child
            self.data[index] = last
        return result

    def __bool__(self) -> bool:
        return bool(self.data)


def johnson_all_pairs_shortest_paths(nodes: list[Node], edges: list[Edge]) -> dict[Node, dict[Node, float]]:
    """
    使用 Johnson 算法计算所有点对最短路径。

    参数：
        nodes: 图中节点列表。
        edges: 有向边列表。

    返回：
        result[u][v] 是 u 到 v 的最短距离；不可达为 inf。
    """
    unique_nodes = list(dict.fromkeys(nodes))
    super_source = object()
    augmented_nodes: list[Node] = [*unique_nodes, super_source]
    augmented_edges: list[Edge] = [*edges, *[(super_source, node, 0.0) for node in unique_nodes]]

    potential = _bellman_ford_potential(augmented_nodes, augmented_edges, super_source)

    reweighted_graph: WeightedGraph = {node: [] for node in unique_nodes}
    for start, end, weight in edges:
        new_weight = weight + potential[start] - potential[end]
        if new_weight < -1e-9:
            raise AssertionError("Johnson 重新赋权后不应出现负权边")
        reweighted_graph.setdefault(start, []).append((end, max(0.0, new_weight)))
        reweighted_graph.setdefault(end, reweighted_graph.get(end, []))

    all_distances: dict[Node, dict[Node, float]] = {}
    for source in unique_nodes:
        reweighted_distance = _dijkstra_non_negative(reweighted_graph, source)
        original_distance: dict[Node, float] = {}

        for target in unique_nodes:
            if reweighted_distance.get(target, float("inf")) == float("inf"):
                original_distance[target] = float("inf")
            else:
                original_distance[target] = (
                    reweighted_distance[target] - potential[source] + potential[target]
                )

        all_distances[source] = original_distance

    return all_distances


def _bellman_ford_potential(nodes: list[Node], edges: list[Edge], source: Node) -> dict[Node, float]:
    """
    使用 Bellman-Ford 计算 Johnson 势函数。
    """
    distance = {node: float("inf") for node in nodes}
    distance[source] = 0.0

    for _ in range(len(nodes) - 1):
        changed = False
        for start, end, weight in edges:
            if distance[start] == float("inf"):
                continue
            candidate = distance[start] + weight
            if candidate < distance[end]:
                distance[end] = candidate
                changed = True
        if not changed:
            break

    for start, end, weight in edges:
        if distance[start] != float("inf") and distance[start] + weight < distance[end]:
            raise ValueError("图中存在负权环，Johnson 算法不能处理")

    return distance


def _dijkstra_non_negative(graph: WeightedGraph, source: Node) -> dict[Node, float]:
    """
    在非负重新赋权图上运行 Dijkstra。
    """
    distance = {node: float("inf") for node in graph}
    distance[source] = 0.0
    heap = _MinHeap()
    heap.push((0.0, source))

    while heap:
        current_distance, node = heap.pop()
        if current_distance != distance[node]:
            continue

        for neighbor, weight in graph.get(node, []):
            candidate = current_distance + weight
            if candidate < distance.get(neighbor, float("inf")):
                distance[neighbor] = candidate
                heap.push((candidate, neighbor))

    return distance


if __name__ == "__main__":
    nodes = ["A", "B", "C", "D"]
    edges = [
        ("A", "B", 1),
        ("B", "C", -2),
        ("A", "C", 4),
        ("C", "D", 2),
        ("D", "B", 3),
    ]
    distances = johnson_all_pairs_shortest_paths(nodes, edges)
    assert distances["A"]["A"] == 0.0
    assert distances["A"]["C"] == -1.0
    assert distances["A"]["D"] == 1.0
    assert distances["D"]["C"] == 1.0

    disconnected = johnson_all_pairs_shortest_paths(["A", "B"], [])
    assert disconnected["A"]["A"] == 0.0
    assert disconnected["A"]["B"] == float("inf")

    try:
        johnson_all_pairs_shortest_paths(["A", "B"], [("A", "B", -1), ("B", "A", -1)])
        raise AssertionError("负权环必须抛出 ValueError")
    except ValueError:
        pass

    print("006_johnson_algorithm: all examples passed")
