"""
文件意图：
    本文件手写实现无向图连通分量计算，用于把图拆成若干个互不连通的节点集合。

适用场景：
    无向图连通性分析、社群/簇的基础划分、判断图是否整体连通。

核心思想：
    对每个尚未访问的节点启动一次 DFS/BFS。一次遍历能访问到的所有节点
    构成一个连通分量。

输入输出：
    输入无向图邻接表，返回连通分量列表。

时间复杂度：
    O(V + E)

空间复杂度：
    O(V)
"""

from collections.abc import Hashable

Node = Hashable
Graph = dict[Node, list[Node]]


def connected_components(graph: Graph) -> list[list[Node]]:
    """
    计算无向图的所有连通分量。

    参数：
        graph: 无向图邻接表。孤立点应以 key 存在并映射到空列表。

    返回：
        连通分量列表，每个分量内部按 DFS 发现顺序排列。
    """
    visited: set[Node] = set()
    components: list[list[Node]] = []

    all_nodes = _collect_all_nodes(graph)
    for node in all_nodes:
        if node in visited:
            continue

        component: list[Node] = []
        stack = [node]
        visited.add(node)

        while stack:
            current = stack.pop()
            component.append(current)

            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)

        components.append(component)

    return components


def is_connected(graph: Graph) -> bool:
    """
    判断无向图是否整体连通。

    空图在这里视为连通，因为不存在两个不可达节点。
    """
    return len(connected_components(graph)) <= 1


def _collect_all_nodes(graph: Graph) -> list[Node]:
    """
    收集所有节点，包括只出现在邻接表值中的节点。
    """
    nodes: list[Node] = []
    seen: set[Node] = set()

    for node, neighbors in graph.items():
        if node not in seen:
            nodes.append(node)
            seen.add(node)
        for neighbor in neighbors:
            if neighbor not in seen:
                nodes.append(neighbor)
                seen.add(neighbor)

    return nodes


if __name__ == "__main__":
    graph = {
        1: [2],
        2: [1, 3],
        3: [2],
        4: [5],
        5: [4],
        6: [],
    }
    components = connected_components(graph)
    component_sets = {frozenset(component) for component in components}
    assert component_sets == {frozenset({1, 2, 3}), frozenset({4, 5}), frozenset({6})}
    assert not is_connected(graph)
    assert is_connected({1: [2], 2: [1]})
    assert is_connected({})

    value_only_node_graph = {"A": ["B"]}
    assert {
        frozenset(component)
        for component in connected_components(value_only_node_graph)
    } == {frozenset({"A", "B"})}

    print("003_connected_components: all examples passed")
