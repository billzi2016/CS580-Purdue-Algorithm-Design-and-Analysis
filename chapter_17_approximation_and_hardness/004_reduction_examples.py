"""
复杂性归约示例：把一个问题实例机械转换成另一个问题实例。

本文件的意图：
1. 用可运行的小函数展示“归约不是口头类比，而是实例转换”。
2. 实现 Independent Set 到 Vertex Cover 的互补关系转换。
3. 实现 3SAT 子句到 Set Cover 教学构造中的元素命名骨架。

这些函数不是求解 NP-hard 问题，而是展示证明 NP-hardness 时常用的结构映射。
"""


Edge = tuple[int, int]
Clause = tuple[str, str, str]


def independent_set_to_vertex_cover_target(vertex_count: int, independent_size: int) -> int:
    """Independent Set 大小 k 转为 Vertex Cover 大小 n-k。

    在同一张图中，S 是 independent set 当且仅当 V-S 是 vertex cover。
    """

    if not 0 <= independent_size <= vertex_count:
        raise ValueError("independent_size 必须位于 [0, vertex_count]")
    return vertex_count - independent_size


def complement_vertices(vertex_count: int, chosen: set[int]) -> set[int]:
    """返回顶点全集 {0..n-1} 中 chosen 的补集。"""

    universe = set(range(vertex_count))
    if not chosen <= universe:
        raise ValueError("chosen 中包含不存在的顶点")
    return universe - chosen


def is_independent_set(edges: list[Edge], chosen: set[int]) -> bool:
    """验证 chosen 是否为独立集。"""

    return all(not (u in chosen and v in chosen) for u, v in edges)


def is_vertex_cover(edges: list[Edge], chosen: set[int]) -> bool:
    """验证 chosen 是否为点覆盖。"""

    return all(u in chosen or v in chosen for u, v in edges)


def clauses_to_set_cover_elements(clauses: list[Clause]) -> set[str]:
    """把 3SAT 子句编号转换成 set cover 里的待覆盖元素名称。

    完整 3SAT -> Set Cover 归约还需要变量一致性集合和冲突约束。本函数只负责
    最基础且可复用的“每个子句必须被覆盖”元素层，避免写成无法验证的伪证明。
    """

    return {f"clause_{index}" for index, _ in enumerate(clauses)}


if __name__ == "__main__":
    edges = [(0, 1), (1, 2), (2, 3)]
    not_independent = {1, 2}
    assert independent_set_to_vertex_cover_target(4, 2) == 2
    assert not is_independent_set(edges, not_independent)

    independent = {0, 3}
    cover = complement_vertices(4, independent)
    assert is_independent_set(edges, independent)
    assert is_vertex_cover(edges, cover)

    clauses = [("x1", "~x2", "x3"), ("~x1", "x2", "x4")]
    assert clauses_to_set_cover_elements(clauses) == {"clause_0", "clause_1"}

    print("004_reduction_examples: all examples passed")
