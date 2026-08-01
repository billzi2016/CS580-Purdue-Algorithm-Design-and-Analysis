"""
文件意图：手写实现有向图欧拉路径的 Hierholzer 算法。
适用场景：需要一条恰好经过每条有向边一次的路径或回路时。
核心思想：沿未使用边持续前进形成回路，在回溯时将局部回路拼接进最终路径。
输入输出：输入顶点数和有向边列表，存在欧拉路径时返回顶点序列，否则返回 None。
时间复杂度：O(V + E)。空间复杂度：O(V + E)。
关键边界：空边集返回空路径；自动检查入出度条件和含边顶点的弱连通性。
"""


def find_euler_path(vertex_count: int, edges: list[tuple[int, int]]) -> list[int] | None:
    """返回有向图的一条欧拉路径，或在不存在时返回 None。

    参数：vertex_count 是顶点数，edges 是 (source, target) 有向边列表。
    返回：包含 E+1 个顶点的欧拉路径；无边图返回空列表。
    边界情况：非法顶点编号抛出 ValueError，度数或连通性不满足时返回 None。
    关键算法点：回溯入栈的顶点顺序反转后，恰好构成 Hierholzer 拼接结果。
    """
    if vertex_count < 0:
        raise ValueError("vertex_count 不能为负数")
    if not edges:
        return []
    adjacency = [[] for _ in range(vertex_count)]
    undirected = [[] for _ in range(vertex_count)]
    in_degree = [0] * vertex_count
    out_degree = [0] * vertex_count
    for source, target in edges:
        if source < 0 or source >= vertex_count or target < 0 or target >= vertex_count:
            raise ValueError("edges 包含无效顶点编号")
        adjacency[source].append(target)
        undirected[source].append(target)
        undirected[target].append(source)
        out_degree[source] += 1
        in_degree[target] += 1

    start = -1
    end_count = start_count = 0
    for vertex in range(vertex_count):
        difference = out_degree[vertex] - in_degree[vertex]
        if difference == 1:
            start_count += 1
            start = vertex
        elif difference == -1:
            end_count += 1
        elif difference != 0:
            return None
    if not ((start_count == 1 and end_count == 1) or (start_count == 0 and end_count == 0)):
        return None
    if start == -1:
        start = next(vertex for vertex in range(vertex_count) if out_degree[vertex] > 0)

    # 忽略孤立点检查弱连通性，否则不可能用一条路径经过不同连通块中的边。
    seen = [False] * vertex_count
    pending = [start]
    seen[start] = True
    while pending:
        vertex = pending.pop()
        for neighbor in undirected[vertex]:
            if not seen[neighbor]:
                seen[neighbor] = True
                pending.append(neighbor)
    if any((in_degree[vertex] or out_degree[vertex]) and not seen[vertex] for vertex in range(vertex_count)):
        return None

    cursor = [0] * vertex_count
    stack = [start]
    path: list[int] = []
    while stack:
        vertex = stack[-1]
        if cursor[vertex] < len(adjacency[vertex]):
            neighbor = adjacency[vertex][cursor[vertex]]
            cursor[vertex] += 1
            stack.append(neighbor)
        else:
            path.append(stack.pop())
    path.reverse()
    return path if len(path) == len(edges) + 1 else None


if __name__ == "__main__":
    path = find_euler_path(3, [(0, 1), (1, 2), (2, 0), (0, 2)])
    assert path is not None and len(path) == 5 and path[0] == 0 and path[-1] == 2
    assert find_euler_path(4, [(0, 1), (2, 3)]) is None
    assert find_euler_path(3, []) == []
    assert find_euler_path(3, [(0, 1), (1, 0)]) in ([0, 1, 0], [1, 0, 1])
    print("005_euler_path: all examples passed")
