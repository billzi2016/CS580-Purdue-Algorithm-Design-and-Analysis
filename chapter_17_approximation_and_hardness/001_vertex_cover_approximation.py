"""
点覆盖 2-近似：反复选一条未覆盖边，并把两个端点都加入覆盖集。

本文件的意图：
1. 手写经典 maximal matching 思路的 vertex cover 近似算法。
2. 给出可验证的覆盖检查函数，避免只返回一个看似合理的集合。
3. 说明近似保证来自匹配下界：任意点覆盖至少要覆盖匹配中的每条边。

算法性质：
- 返回集合一定是合法 vertex cover。
- 大小不超过最优解的 2 倍。
"""

Edge = tuple[int, int]


def approximate_vertex_cover(edges: list[Edge]) -> set[int]:
    """返回一个 2-近似点覆盖集合。"""

    uncovered = {tuple(sorted(edge)) for edge in edges if edge[0] != edge[1]}
    cover: set[int] = set()

    while uncovered:
        u, v = next(iter(uncovered))
        cover.add(u)
        cover.add(v)

        # 选中 u 和 v 后，所有与它们相邻的边都已经被覆盖，可以从未覆盖集合移除。
        uncovered = {
            (a, b) for a, b in uncovered if a not in (u, v) and b not in (u, v)
        }

    return cover


def is_vertex_cover(edges: list[Edge], cover: set[int]) -> bool:
    """验证 cover 是否覆盖每条边。"""

    return all(u in cover or v in cover for u, v in edges)


def greedy_maximal_matching(edges: list[Edge]) -> set[Edge]:
    """构造一个极大匹配，用于解释 2-近似证明中的下界。"""

    matching: set[Edge] = set()
    used_vertices: set[int] = set()

    for u, v in edges:
        if u == v:
            continue
        if u in used_vertices or v in used_vertices:
            continue
        matching.add(tuple(sorted((u, v))))
        used_vertices.add(u)
        used_vertices.add(v)

    return matching


if __name__ == "__main__":
    triangle = [(0, 1), (1, 2), (0, 2)]
    cover = approximate_vertex_cover(triangle)
    assert is_vertex_cover(triangle, cover)
    assert len(cover) <= 4

    path = [(0, 1), (1, 2), (2, 3)]
    path_cover = approximate_vertex_cover(path)
    assert is_vertex_cover(path, path_cover)
    assert len(path_cover) <= 4

    assert greedy_maximal_matching(path) == {(0, 1), (2, 3)}

    print("001_vertex_cover_approximation: all examples passed")
