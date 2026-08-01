"""
文件意图：
    本文件手写实现图的广度优先搜索（BFS），用于按距离层次遍历无权图。

适用场景：
    无权图最短步数、层序遍历、连通性探索、从起点扩展可达节点。

核心思想：
    使用队列维护当前边界。先访问距离起点更近的节点，再访问下一层节点。
    对无权图而言，节点第一次被 BFS 访问时得到的距离就是最短边数距离。

输入输出：
    输入邻接表和起点，返回访问顺序、父节点表和距离表。

时间复杂度：
    O(V + E)

空间复杂度：
    O(V)
"""

from collections import deque
from collections.abc import Hashable

Node = Hashable
Graph = dict[Node, list[Node]]


def breadth_first_search(graph: Graph, start: Node) -> tuple[list[Node], dict[Node, Node | None], dict[Node, int]]:
    """
    从 start 开始执行 BFS。

    参数：
        graph: 邻接表，graph[u] 是 u 的所有出边邻居。
        start: 起点。

    返回：
        (order, parent, distance)：
            order: BFS 访问顺序；
            parent: BFS 树中的父节点，起点父节点为 None；
            distance: 从起点到各可达节点的最短边数。

    边界情况：
        如果 start 不在 graph 中，仍然把 start 视为孤立节点处理。
    """
    order: list[Node] = []
    parent: dict[Node, Node | None] = {start: None}
    distance: dict[Node, int] = {start: 0}
    queue: deque[Node] = deque([start])

    while queue:
        current = queue.popleft()
        order.append(current)

        for neighbor in graph.get(current, []):
            if neighbor in distance:
                continue

            # 第一次发现 neighbor 时，当前路径一定是无权图中的最短路径。
            parent[neighbor] = current
            distance[neighbor] = distance[current] + 1
            queue.append(neighbor)

    return order, parent, distance


def reconstruct_path(parent: dict[Node, Node | None], target: Node) -> list[Node]:
    """
    根据 BFS 父节点表还原从起点到 target 的路径。

    如果 target 不在 parent 中，说明 target 不可达，返回空列表。
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
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D", "E"],
        "D": ["F"],
        "E": [],
        "F": [],
    }
    order, parent, distance = breadth_first_search(graph, "A")
    assert order == ["A", "B", "C", "D", "E", "F"]
    assert distance == {"A": 0, "B": 1, "C": 1, "D": 2, "E": 2, "F": 3}
    assert reconstruct_path(parent, "F") == ["A", "B", "D", "F"]
    assert reconstruct_path(parent, "Z") == []

    isolated_order, isolated_parent, isolated_distance = breadth_first_search({}, "X")
    assert isolated_order == ["X"]
    assert isolated_parent == {"X": None}
    assert isolated_distance == {"X": 0}

    print("001_bfs: all examples passed")
