"""手写树上莫队：离线回答无权树路径上不同颜色数。

通过 DFS 的两次访问 Euler 序把路径转成区间；窗口端点切换顶点的奇偶出现状态，
区间中出现奇数次的顶点恰为当前路径。时间复杂度 O((n+q)sqrt(n))，空间 O(n)。
仅支持连通无向树；非法树或顶点编号抛出 ValueError。
"""


def mo_tree_distinct_colors(
    tree: list[list[int]], colors: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    """返回每个 (u,v) 路径上的不同颜色数。

    参数：tree 为对称无向树，colors[v] 为顶点颜色，queries 为路径端点。
    返回：按原顺序的不同颜色数。
    边界：单点路径可处理；颜色允许任意整数。
    关键点：非祖先端点的 Euler 区间需额外临时加入 LCA。
    """
    n = len(tree)
    if n == 0 or len(colors) != n:
        raise ValueError("tree 必须非空且 colors 长度匹配")
    if any(u < 0 or v < 0 or u >= n or v >= n for u, v in queries):
        raise ValueError("查询顶点编号无效")
    parent, depth, tin, tout, euler = [0] * n, [-1] * n, [0] * n, [0] * n, []
    depth[0] = 0
    stack = [(0, 0, 0)]
    while stack:
        v, p, i = stack[-1]
        if i == 0:
            tin[v] = len(euler)
            euler.append(v)
        if i == len(tree[v]):
            tout[v] = len(euler)
            euler.append(v)
            stack.pop()
            continue
        w = tree[v][i]
        stack[-1] = (v, p, i + 1)
        if w == p:
            continue
        if w < 0 or w >= n or depth[w] != -1:
            raise ValueError("tree 必须是连通无环图")
        parent[w] = v
        depth[w] = depth[v] + 1
        stack.append((w, v, 0))
    if any(d < 0 for d in depth):
        raise ValueError("tree 必须连通")

    def lca(a: int, b: int) -> int:
        while depth[a] > depth[b]:
            a = parent[a]
        while depth[b] > depth[a]:
            b = parent[b]
        while a != b:
            a, b = parent[a], parent[b]
        return a

    packed = []
    for i, (u, v) in enumerate(queries):
        if tin[u] > tin[v]:
            u, v = v, u
        w = lca(u, v)
        packed.append(
            (tin[u], tin[v], -1 if w == u else w, i)
            if w == u
            else (tout[u], tin[v], w, i)
        )
    block = max(1, int((2 * n) ** 0.5))
    packed.sort(key=lambda x: (x[0] // block, x[1]))
    active = [False] * n
    freq: dict[int, int] = {}
    answer = [0] * len(queries)
    distinct = 0
    left = 0
    right = -1

    def toggle(pos: int) -> None:
        nonlocal distinct
        v = euler[pos]
        c = colors[v]
        if active[v]:
            freq[c] -= 1
            if not freq[c]:
                del freq[c]
                distinct -= 1
        else:
            if freq.get(c, 0) == 0:
                distinct += 1
            freq[c] = freq.get(c, 0) + 1
        active[v] = not active[v]

    for a, b, extra, index in packed:
        while left > a:
            left -= 1
            toggle(left)
        while right < b:
            right += 1
            toggle(right)
        while left < a:
            toggle(left)
            left += 1
        while right > b:
            toggle(right)
            right -= 1
        if extra != -1:
            c = colors[extra]
            answer[index] = distinct + (freq.get(c, 0) == 0)
        else:
            answer[index] = distinct
    return answer


if __name__ == "__main__":
    tree = [[1, 2], [0, 3, 4], [0, 5], [1], [1], [2]]
    assert mo_tree_distinct_colors(
        tree, [1, 2, 1, 2, 3, 3], [(3, 4), (3, 5), (0, 0)]
    ) == [2, 3, 1]
    assert mo_tree_distinct_colors([[]], [7], [(0, 0)]) == [1]
    print("002_mos_algorithm_on_tree: all examples passed")
