"""
文件意图：
    本文件手写实现 Bellman-Ford 算法，用于含负权边图中的单源最短路径计算。

适用场景：
    图中可以有负权边，但不能存在从起点可达的负权环。若存在可达负环，
    最短路径没有良定义，算法应明确报告。

核心思想：
    对所有边重复执行 V - 1 轮松弛。任意不含环的最短路径最多包含 V - 1 条边；
    如果第 V 轮仍能松弛，说明存在从起点可达的负权环。

输入输出：
    输入边列表和起点，返回距离表与父节点表。

时间复杂度：
    O(VE)

空间复杂度：
    O(V)
"""

from collections.abc import Hashable, Iterable

Node = Hashable
Edge = tuple[Node, Node, float]


def bellman_ford(
    nodes: Iterable[Node], edges: list[Edge], source: Node
) -> tuple[dict[Node, float], dict[Node, Node | None]]:
    """
    计算 source 到所有节点的最短距离。

    参数：
        nodes: 图中节点集合。
        edges: 边列表，每条边为 (u, v, weight)。
        source: 起点。

    返回：
        (distance, parent)。

    异常：
        如果存在从 source 可达的负权环，抛出 ValueError。
    """
    node_list = list(dict.fromkeys([*nodes, source]))
    distance = {node: float("inf") for node in node_list}
    parent: dict[Node, Node | None] = {node: None for node in node_list}
    distance[source] = 0.0

    for _ in range(len(node_list) - 1):
        changed = False

        for start, end, weight in edges:
            if distance.get(start, float("inf")) == float("inf"):
                continue

            candidate = distance[start] + weight
            if candidate < distance.get(end, float("inf")):
                distance[end] = candidate
                parent[end] = start
                changed = True

        # 如果一整轮没有任何更新，说明已经提前收敛。
        if not changed:
            break

    for start, end, weight in edges:
        if distance.get(start, float("inf")) == float("inf"):
            continue
        if distance[start] + weight < distance.get(end, float("inf")):
            raise ValueError("存在从起点可达的负权环")

    return distance, parent


def reconstruct_path(parent: dict[Node, Node | None], target: Node) -> list[Node]:
    """
    根据 Bellman-Ford 父节点表还原路径。
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


if __name__ == "__main__":
    nodes = ["S", "A", "B", "C"]
    edges = [
        ("S", "A", 4),
        ("S", "B", 5),
        ("A", "C", -2),
        ("B", "C", 3),
    ]
    distance, parent = bellman_ford(nodes, edges, "S")
    assert distance["S"] == 0.0
    assert distance["A"] == 4.0
    assert distance["B"] == 5.0
    assert distance["C"] == 2.0
    assert reconstruct_path(parent, "C") == ["S", "A", "C"]

    unreachable_distance, _ = bellman_ford(["S", "X"], [], "S")
    assert unreachable_distance["X"] == float("inf")

    try:
        bellman_ford(["A", "B"], [("A", "B", -1), ("B", "A", -1)], "A")
        raise AssertionError("可达负权环必须抛出 ValueError")
    except ValueError:
        pass

    print("002_bellman_ford: all examples passed")
