"""
文件意图：
    本文件手写实现二分图检测，用于判断无向图能否用两种颜色染色且相邻节点颜色不同。

适用场景：
    二分图匹配前置检查、冲突关系建模、奇环检测。

核心思想：
    对每个连通分量执行 BFS 染色。若访问到已染色邻居且颜色与当前节点相同，
    则图不是二分图；否则所有分量都能成功染色。

输入输出：
    输入无向图邻接表，返回是否二分图以及颜色映射。

时间复杂度：
    O(V + E)

空间复杂度：
    O(V)
"""

from collections import deque
from collections.abc import Hashable

Node = Hashable
Graph = dict[Node, list[Node]]


def check_bipartite(graph: Graph) -> tuple[bool, dict[Node, int]]:
    """
    判断无向图是否为二分图。

    参数：
        graph: 无向图邻接表。

    返回：
        (is_bipartite, color)，color 使用 0/1 表示两个集合。
        如果不是二分图，返回冲突发生前已经构造出的部分染色。
    """
    color: dict[Node, int] = {}

    for start in _collect_all_nodes(graph):
        if start in color:
            continue

        color[start] = 0
        queue: deque[Node] = deque([start])

        while queue:
            current = queue.popleft()

            for neighbor in graph.get(current, []):
                expected_color = 1 - color[current]
                if neighbor not in color:
                    color[neighbor] = expected_color
                    queue.append(neighbor)
                elif color[neighbor] != expected_color:
                    return False, color

    return True, color


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
    square = {
        1: [2, 4],
        2: [1, 3],
        3: [2, 4],
        4: [1, 3],
    }
    is_bipartite, color = check_bipartite(square)
    assert is_bipartite
    assert color[1] != color[2]
    assert color[2] != color[3]

    triangle = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    assert not check_bipartite(triangle)[0]

    disconnected = {"A": ["B"], "B": ["A"], "C": []}
    assert check_bipartite(disconnected)[0]
    assert check_bipartite({}) == (True, {})

    print("006_bipartite_check: all examples passed")
