"""
文件意图：
    本文件用可执行检查函数演示最小生成树的割性质与环性质。

适用场景：
    理解 Kruskal 和 Prim 为什么正确，以及如何判断某条边是否被某个性质支持或排除。

核心思想：
    割性质：跨越某个割的唯一最轻边一定属于某棵 MST。
    环性质：某个环中的唯一最重边不属于任何 MST。

输入输出：
    输入无向边集和割/环描述，返回性质判断结果。

时间复杂度：
    单次检查 O(E) 或 O(C)，其中 C 是环边数量。

空间复杂度：
    O(E)
"""

from collections.abc import Hashable

Node = Hashable
Edge = tuple[Node, Node, float]


def lightest_crossing_edges(edges: list[Edge], left_side: set[Node]) -> list[Edge]:
    """
    返回跨越割 (left_side, V-left_side) 的最轻边集合。

    说明：
        如果返回集合大小为 1，则这条边是该割的唯一最轻边，受割性质支持。
    """
    crossing: list[Edge] = []
    for start, end, weight in edges:
        if (start in left_side) != (end in left_side):
            crossing.append((start, end, weight))

    if not crossing:
        return []

    minimum_weight = min(weight for _, _, weight in crossing)
    return [edge for edge in crossing if edge[2] == minimum_weight]


def is_unique_lightest_crossing_edge(
    edges: list[Edge], left_side: set[Node], target: Edge
) -> bool:
    """
    判断 target 是否是某个割上的唯一最轻横切边。
    """
    lightest = lightest_crossing_edges(edges, left_side)
    return len(lightest) == 1 and _same_undirected_edge(lightest[0], target)


def heaviest_edges_on_cycle(cycle_edges: list[Edge]) -> list[Edge]:
    """
    返回环中的最重边集合。

    说明：
        如果返回集合大小为 1，则这条唯一最重边受环性质排除，不会出现在任何 MST 中。
    """
    if not cycle_edges:
        raise ValueError("环边列表不能为空")

    maximum_weight = max(weight for _, _, weight in cycle_edges)
    return [edge for edge in cycle_edges if edge[2] == maximum_weight]


def is_unique_heaviest_on_cycle(cycle_edges: list[Edge], target: Edge) -> bool:
    """
    判断 target 是否是某个环上的唯一最重边。
    """
    heaviest = heaviest_edges_on_cycle(cycle_edges)
    return len(heaviest) == 1 and _same_undirected_edge(heaviest[0], target)


def _same_undirected_edge(first: Edge, second: Edge) -> bool:
    """
    判断两条无向边是否连接同一对端点且权重相同。
    """
    first_u, first_v, first_w = first
    second_u, second_v, second_w = second
    return {first_u, first_v} == {second_u, second_v} and first_w == second_w


if __name__ == "__main__":
    edges = [
        ("A", "B", 1),
        ("A", "C", 4),
        ("B", "C", 2),
        ("C", "D", 3),
    ]
    assert lightest_crossing_edges(edges, {"A"}) == [("A", "B", 1)]
    assert is_unique_lightest_crossing_edge(edges, {"A"}, ("A", "B", 1))
    assert not is_unique_lightest_crossing_edge(edges, {"A"}, ("A", "C", 4))

    tied_edges = [("A", "B", 1), ("A", "C", 1)]
    assert len(lightest_crossing_edges(tied_edges, {"A"})) == 2

    cycle = [("A", "B", 1), ("B", "C", 2), ("A", "C", 4)]
    assert heaviest_edges_on_cycle(cycle) == [("A", "C", 4)]
    assert is_unique_heaviest_on_cycle(cycle, ("C", "A", 4))

    try:
        heaviest_edges_on_cycle([])
        raise AssertionError("空环必须抛出 ValueError")
    except ValueError:
        pass

    print("004_cut_and_cycle_properties: all examples passed")
