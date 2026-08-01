"""
文件意图：手写实现 Tarjan 算法，分解有向图的强连通分量。
适用场景：分析有向图中的互相可达顶点、压缩图或构造依赖关系的分量图。
核心思想：DFS 时间戳与 low-link 值共同识别一段仍在栈中的 DFS 路径是否构成 SCC 根。
输入输出：输入邻接表，返回每个强连通分量的顶点列表。
时间复杂度：O(V + E)。空间复杂度：O(V)。
关键边界：支持非连通图、孤立点和自环；顶点编号必须在邻接表范围内。
"""


def tarjan_scc(graph: list[list[int]]) -> list[list[int]]:
    """使用 Tarjan 算法返回有向图的全部强连通分量。

    参数：graph 的下标是顶点编号，每个元素为该顶点的有向邻居。
    返回：强连通分量列表；分量和顶点在分量内的顺序由 DFS 决定。
    边界情况：空图返回空列表，非法邻居编号抛出 ValueError。
    关键算法点：只有仍在栈中的回边才能用于降低 low-link 值。
    """
    vertex_count = len(graph)
    if any(neighbor < 0 or neighbor >= vertex_count for neighbors in graph for neighbor in neighbors):
        raise ValueError("graph 包含超出邻接表范围的顶点编号")

    discovery = [-1] * vertex_count
    low_link = [0] * vertex_count
    on_stack = [False] * vertex_count
    stack: list[int] = []
    components: list[list[int]] = []
    time = 0

    def visit(vertex: int) -> None:
        nonlocal time
        discovery[vertex] = low_link[vertex] = time
        time += 1
        stack.append(vertex)
        on_stack[vertex] = True

        for neighbor in graph[vertex]:
            if discovery[neighbor] == -1:
                visit(neighbor)
                low_link[vertex] = min(low_link[vertex], low_link[neighbor])
            elif on_stack[neighbor]:
                # 已完成分量中的边不能把当前路径连接回该分量，不能参与更新。
                low_link[vertex] = min(low_link[vertex], discovery[neighbor])

        if low_link[vertex] == discovery[vertex]:
            component: list[int] = []
            while True:
                member = stack.pop()
                on_stack[member] = False
                component.append(member)
                if member == vertex:
                    break
            components.append(component)

    for vertex in range(vertex_count):
        if discovery[vertex] == -1:
            visit(vertex)
    return components


if __name__ == "__main__":
    graph = [[1], [2, 3], [0], [4], [3], []]
    assert {frozenset(component) for component in tarjan_scc(graph)} == {
        frozenset({0, 1, 2}), frozenset({3, 4}), frozenset({5})
    }
    assert tarjan_scc([]) == []
    assert {frozenset(component) for component in tarjan_scc([[0], []])} == {frozenset({0}), frozenset({1})}
    print("001_tarjan_scc: all examples passed")
