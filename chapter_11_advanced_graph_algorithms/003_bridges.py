"""
文件意图：手写实现无向简单图中的桥检测。
适用场景：寻找删除后会增加连通分量数目的关键连接边。
核心思想：DFS 的 low-link 值表示子树能借助至多一条回边到达的最早祖先时间。
输入输出：输入无向邻接表，返回桥的规范化端点对。
时间复杂度：O(V + E)。空间复杂度：O(V)。
关键边界：支持非连通图和孤立点；本基础版本仅接受对称且无平行边的简单无向图。
"""


def _validate_simple_undirected_graph(graph: list[list[int]]) -> None:
    """验证邻接表表示简单无向图，避免平行边破坏 parent 边判断。"""
    vertex_count = len(graph)
    for vertex, neighbors in enumerate(graph):
        seen: set[int] = set()
        for neighbor in neighbors:
            if neighbor < 0 or neighbor >= vertex_count or neighbor == vertex:
                raise ValueError("graph 必须是不含自环的简单无向图")
            if neighbor in seen or vertex not in graph[neighbor]:
                raise ValueError("graph 必须使用对称且无平行边的邻接表")
            seen.add(neighbor)


def find_bridges(graph: list[list[int]]) -> list[tuple[int, int]]:
    """返回无向简单图 graph 中的全部桥。

    参数：graph 为对称、无自环、无平行边的无向邻接表。
    返回：端点按升序排列的桥列表，整体顺序由 DFS 决定。
    边界情况：空图、孤立点和非连通图均可处理。
    关键算法点：树边 (u, v) 是桥当且仅当 low[v] 大于 discovery[u]。
    """
    _validate_simple_undirected_graph(graph)
    discovery = [-1] * len(graph)
    low_link = [0] * len(graph)
    bridges: list[tuple[int, int]] = []
    time = 0

    def visit(vertex: int, parent: int) -> None:
        nonlocal time
        discovery[vertex] = low_link[vertex] = time
        time += 1
        for neighbor in graph[vertex]:
            if neighbor == parent:
                continue
            if discovery[neighbor] == -1:
                visit(neighbor, vertex)
                low_link[vertex] = min(low_link[vertex], low_link[neighbor])
                if low_link[neighbor] > discovery[vertex]:
                    bridges.append((min(vertex, neighbor), max(vertex, neighbor)))
            else:
                low_link[vertex] = min(low_link[vertex], discovery[neighbor])

    for vertex in range(len(graph)):
        if discovery[vertex] == -1:
            visit(vertex, -1)
    return bridges


if __name__ == "__main__":
    graph = [[1], [0, 2, 3], [1, 3], [1, 2, 4], [3], []]
    assert set(find_bridges(graph)) == {(0, 1), (3, 4)}
    assert find_bridges([[], []]) == []
    assert find_bridges([[1, 2], [0, 2], [0, 1]]) == []
    print("003_bridges: all examples passed")
