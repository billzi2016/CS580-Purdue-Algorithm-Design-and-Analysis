"""手写离线动态连通性：时间线段树配合可回滚并查集。"""


def offline_dynamic_connectivity(
    vertex_count: int, operations: list[tuple[str, int, int]]
) -> list[bool]:
    """离线处理 add/remove/query，复杂度 O((q log q) log n)。"""
    if vertex_count <= 0:
        raise ValueError("顶点数必须为正")
    q = len(operations)
    active = {}
    intervals = []
    queries = {}
    for time, (kind, u, v) in enumerate(operations):
        if not (0 <= u < vertex_count and 0 <= v < vertex_count):
            raise ValueError("顶点编号无效")
        edge = (min(u, v), max(u, v))
        if kind == "add":
            if edge in active:
                raise ValueError("重复添加边")
            active[edge] = time
        elif kind == "remove":
            if edge not in active:
                raise ValueError("删除了不存在的边")
            intervals.append((active.pop(edge), time, edge))
        elif kind == "query":
            queries[time] = (u, v)
        else:
            raise ValueError("操作必须为 add、remove 或 query")
    intervals.extend((start, q, edge) for edge, start in active.items())
    tree = [[] for _ in range(4 * max(1, q))]

    def add(node, left, right, a, b, edge):
        if a <= left and right <= b:
            tree[node].append(edge)
            return
        m = (left + right) // 2
        if a < m:
            add(node * 2, left, m, a, b, edge)
        if b > m:
            add(node * 2 + 1, m, right, a, b, edge)

    for a, b, e in intervals:
        if a < b:
            add(1, 0, q, a, b, e)
    parent = list(range(vertex_count))
    size = [1] * vertex_count
    history = []
    answer = []

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    def unite(a, b):
        a, b = find(a), find(b)
        if a == b:
            history.append(None)
            return
        if size[a] < size[b]:
            a, b = b, a
        history.append((b, a, size[a]))
        parent[b] = a
        size[a] += size[b]

    def rollback(mark):
        while len(history) > mark:
            item = history.pop()
            if item:
                b, a, old = item
                parent[b] = b
                size[a] = old

    def solve(node, left, right):
        mark = len(history)
        for a, b in tree[node]:
            unite(a, b)
        if right - left == 1:
            if left in queries:
                a, b = queries[left]
                answer.append(find(a) == find(b))
        else:
            m = (left + right) // 2
            solve(node * 2, left, m)
            solve(node * 2 + 1, m, right)
        rollback(mark)

    if q:
        solve(1, 0, q)
    return answer


if __name__ == "__main__":
    assert offline_dynamic_connectivity(
        3,
        [
            ("add", 0, 1),
            ("query", 0, 2),
            ("add", 1, 2),
            ("query", 0, 2),
            ("remove", 1, 2),
            ("query", 0, 2),
        ],
    ) == [False, True, False]
    print("005_offline_dynamic_connectivity: all examples passed")
