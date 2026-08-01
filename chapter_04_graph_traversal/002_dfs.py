"""
文件意图：
    本文件手写实现图的深度优先搜索（DFS），包括递归版和显式栈迭代版。

适用场景：
    连通性探索、拓扑结构分析、路径搜索、图算法中的时间戳和 DFS 树构建。

核心思想：
    DFS 沿着一条路径尽可能深入，无法继续后再回溯。递归调用栈或显式栈
    都可以表达这种“深入再回退”的遍历顺序。

输入输出：
    输入邻接表和起点，返回访问顺序。

时间复杂度：
    O(V + E)

空间复杂度：
    O(V)
"""

from collections.abc import Hashable

Node = Hashable
Graph = dict[Node, list[Node]]


def depth_first_search_recursive(graph: Graph, start: Node) -> list[Node]:
    """
    使用递归实现 DFS。

    参数：
        graph: 邻接表。
        start: 起点。

    返回：
        DFS 首次访问节点的顺序。
    """
    visited: set[Node] = set()
    order: list[Node] = []

    def visit(node: Node) -> None:
        """
        递归访问 node 及其尚未访问的后继节点。
        """
        visited.add(node)
        order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visit(neighbor)

    visit(start)
    return order


def depth_first_search_iterative(graph: Graph, start: Node) -> list[Node]:
    """
    使用显式栈实现 DFS。

    关键点：
        为了让迭代版访问顺序与递归版一致，需要按邻接表逆序入栈。
    """
    visited: set[Node] = set()
    order: list[Node] = []
    stack: list[Node] = [start]

    while stack:
        node = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        order.append(node)

        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


if __name__ == "__main__":
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": [],
        "E": [],
        "F": [],
    }
    assert depth_first_search_recursive(graph, "A") == ["A", "B", "D", "E", "C", "F"]
    assert depth_first_search_iterative(graph, "A") == ["A", "B", "D", "E", "C", "F"]
    assert depth_first_search_recursive({}, "X") == ["X"]
    assert depth_first_search_iterative({}, "X") == ["X"]

    cyclic_graph = {"A": ["B"], "B": ["C"], "C": ["A"]}
    assert depth_first_search_recursive(cyclic_graph, "A") == ["A", "B", "C"]
    assert depth_first_search_iterative(cyclic_graph, "A") == ["A", "B", "C"]

    print("002_dfs: all examples passed")
