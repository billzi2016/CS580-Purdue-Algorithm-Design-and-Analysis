"""
文件意图：手写实现 Kosaraju 算法，分解有向图的强连通分量。
适用场景：需要以两次 DFS 清晰理解强连通分量的教学或工程场景。
核心思想：先按原图完成时间排序，再在反向图中按逆完成顺序收集分量。
输入输出：输入邻接表，返回每个强连通分量的顶点列表。
时间复杂度：O(V + E)。空间复杂度：O(V + E)。
关键边界：支持非连通图、孤立点和自环；非法顶点编号会被拒绝。
"""


def kosaraju_scc(graph: list[list[int]]) -> list[list[int]]:
    """使用 Kosaraju 算法返回有向图的全部强连通分量。

    参数：graph 的下标是顶点编号，每个元素为该顶点的有向邻居。
    返回：强连通分量列表，顺序由 DFS 完成时间决定。
    边界情况：空图返回空列表，非法邻居编号抛出 ValueError。
    关键算法点：反向图中的一次 DFS 不会跨越原图 SCC 缩点图的边界。
    """
    vertex_count = len(graph)
    if any(neighbor < 0 or neighbor >= vertex_count for neighbors in graph for neighbor in neighbors):
        raise ValueError("graph 包含超出邻接表范围的顶点编号")
    reverse_graph = [[] for _ in range(vertex_count)]
    for vertex, neighbors in enumerate(graph):
        for neighbor in neighbors:
            reverse_graph[neighbor].append(vertex)

    visited = [False] * vertex_count
    finish_order: list[int] = []

    def first_dfs(vertex: int) -> None:
        visited[vertex] = True
        for neighbor in graph[vertex]:
            if not visited[neighbor]:
                first_dfs(neighbor)
        # 后序加入保证越晚完成的顶点越靠近列表末尾。
        finish_order.append(vertex)

    for vertex in range(vertex_count):
        if not visited[vertex]:
            first_dfs(vertex)

    visited = [False] * vertex_count
    components: list[list[int]] = []

    def second_dfs(vertex: int, component: list[int]) -> None:
        visited[vertex] = True
        component.append(vertex)
        for neighbor in reverse_graph[vertex]:
            if not visited[neighbor]:
                second_dfs(neighbor, component)

    for vertex in reversed(finish_order):
        if not visited[vertex]:
            component: list[int] = []
            second_dfs(vertex, component)
            components.append(component)
    return components


if __name__ == "__main__":
    graph = [[1], [2, 3], [0], [4], [3], []]
    assert {frozenset(component) for component in kosaraju_scc(graph)} == {
        frozenset({0, 1, 2}), frozenset({3, 4}), frozenset({5})
    }
    assert kosaraju_scc([]) == []
    assert {frozenset(component) for component in kosaraju_scc([[0], []])} == {frozenset({0}), frozenset({1})}
    print("002_kosaraju_scc: all examples passed")
