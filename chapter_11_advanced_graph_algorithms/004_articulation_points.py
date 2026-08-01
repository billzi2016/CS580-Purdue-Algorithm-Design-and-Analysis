"""
文件意图：手写实现无向简单图中的割点检测。
适用场景：寻找移除后会使网络连通性下降的关键顶点。
核心思想：借助 DFS low-link 值判断某棵子树能否绕过当前顶点回到其祖先。
输入输出：输入无向邻接表，返回所有割点组成的集合。
时间复杂度：O(V + E)。空间复杂度：O(V)。
关键边界：支持非连通图；本基础版本只处理对称且无平行边的简单无向图。
"""


def _validate_simple_undirected_graph(graph: list[list[int]]) -> None:
    """验证邻接表为不含自环和平行边的对称无向图。"""
    vertex_count = len(graph)
    for vertex, neighbors in enumerate(graph):
        seen: set[int] = set()
        for neighbor in neighbors:
            if neighbor < 0 or neighbor >= vertex_count or neighbor == vertex:
                raise ValueError("graph 必须是不含自环的简单无向图")
            if neighbor in seen or vertex not in graph[neighbor]:
                raise ValueError("graph 必须使用对称且无平行边的邻接表")
            seen.add(neighbor)


def find_articulation_points(graph: list[list[int]]) -> set[int]:
    """返回无向简单图 graph 的全部割点。

    参数：graph 为对称、无自环、无平行边的无向邻接表。
    返回：删除后增加连通分量数量的顶点编号集合。
    边界情况：孤立顶点不是割点；DFS 根必须拥有至少两个子树才是割点。
    关键算法点：非根 vertex 在存在 child 满足 low[child] >= discovery[vertex] 时为割点。
    """
    _validate_simple_undirected_graph(graph)
    discovery = [-1] * len(graph)
    low_link = [0] * len(graph)
    points: set[int] = set()
    time = 0

    def visit(vertex: int, parent: int) -> None:
        nonlocal time
        discovery[vertex] = low_link[vertex] = time
        time += 1
        child_count = 0
        for neighbor in graph[vertex]:
            if neighbor == parent:
                continue
            if discovery[neighbor] == -1:
                child_count += 1
                visit(neighbor, vertex)
                low_link[vertex] = min(low_link[vertex], low_link[neighbor])
                if parent != -1 and low_link[neighbor] >= discovery[vertex]:
                    points.add(vertex)
            else:
                low_link[vertex] = min(low_link[vertex], discovery[neighbor])
        if parent == -1 and child_count >= 2:
            points.add(vertex)

    for vertex in range(len(graph)):
        if discovery[vertex] == -1:
            visit(vertex, -1)
    return points


if __name__ == "__main__":
    graph = [[1], [0, 2, 3], [1, 3], [1, 2, 4], [3], []]
    assert find_articulation_points(graph) == {1, 3}
    assert find_articulation_points([[1, 2], [0, 2], [0, 1]]) == set()
    assert find_articulation_points([[], []]) == set()
    assert find_articulation_points([[1, 2], [0], [0]]) == {0}
    print("004_articulation_points: all examples passed")
