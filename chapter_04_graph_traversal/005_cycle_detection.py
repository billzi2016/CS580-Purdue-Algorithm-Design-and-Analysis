"""
文件意图：
    本文件手写实现图中的环检测，包括有向图和无向图两种常见场景。

适用场景：
    依赖关系检查、死锁/循环依赖判断、判断无向图是否为森林。

核心思想：
    有向图使用 DFS 三色标记：访问中节点再次被访问表示存在回边。
    无向图使用 DFS 并记录父节点：遇到已访问且不是父节点的邻居表示存在环。

输入输出：
    输入邻接表，返回是否存在环。

时间复杂度：
    O(V + E)

空间复杂度：
    O(V)
"""

from collections.abc import Hashable

Node = Hashable
Graph = dict[Node, list[Node]]


def has_cycle_directed(graph: Graph) -> bool:
    """
    判断有向图中是否存在环。
    """
    visiting: set[Node] = set()
    visited: set[Node] = set()

    def dfs(node: Node) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False

        visiting.add(node)
        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True

        visiting.remove(node)
        visited.add(node)
        return False

    for node in _collect_all_nodes(graph):
        if node not in visited and dfs(node):
            return True

    return False


def has_cycle_undirected(graph: Graph) -> bool:
    """
    判断无向图中是否存在环。
    """
    visited: set[Node] = set()

    def dfs(node: Node, parent: Node | None) -> bool:
        visited.add(node)

        for neighbor in graph.get(node, []):
            if neighbor == parent:
                continue
            if neighbor in visited:
                return True
            if dfs(neighbor, node):
                return True

        return False

    for node in _collect_all_nodes(graph):
        if node not in visited and dfs(node, None):
            return True

    return False


def _collect_all_nodes(graph: Graph) -> list[Node]:
    """
    收集 key 和邻接表值中出现的所有节点。
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
    assert has_cycle_directed({"A": ["B"], "B": ["C"], "C": ["A"]})
    assert not has_cycle_directed({"A": ["B"], "B": ["C"], "C": []})
    assert not has_cycle_directed({})

    undirected_cycle = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    undirected_tree = {1: [2], 2: [1, 3], 3: [2]}
    assert has_cycle_undirected(undirected_cycle)
    assert not has_cycle_undirected(undirected_tree)
    assert not has_cycle_undirected({1: []})

    print("005_cycle_detection: all examples passed")
