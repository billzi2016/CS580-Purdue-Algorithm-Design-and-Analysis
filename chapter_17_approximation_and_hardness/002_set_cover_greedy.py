"""
集合覆盖贪心近似：每轮选择覆盖最多未覆盖元素的集合。

本文件的意图：
1. 手写 set cover 的经典贪心算法。
2. 支持带名称的集合，便于在课程作业和竞赛题里追踪选择结果。
3. 返回前验证是否真的覆盖 universe，避免“看起来选了集合但没覆盖完”的伪实现。

理论性质：
- 对一般 set cover，贪心算法有 H_n 近似因子。
- 这个算法不是最优解搜索；它追求可证明的近似质量和多项式时间。
"""

NamedSet = tuple[str, set[str]]


def greedy_set_cover(universe: set[str], subsets: list[NamedSet]) -> list[str]:
    """返回被选中集合的名称列表。"""

    uncovered = set(universe)
    chosen: list[str] = []

    while uncovered:
        best_name = ""
        best_cover: set[str] = set()

        for name, subset in subsets:
            newly_covered = uncovered & subset
            if len(newly_covered) > len(best_cover):
                best_name = name
                best_cover = newly_covered

        if not best_cover:
            missing = ", ".join(sorted(uncovered))
            raise ValueError(f"universe 中存在无法覆盖的元素: {missing}")

        chosen.append(best_name)
        uncovered -= best_cover

    return chosen


def covered_elements(chosen_names: list[str], subsets: list[NamedSet]) -> set[str]:
    """根据名称列表还原被覆盖的元素集合。"""

    lookup = {name: subset for name, subset in subsets}
    result: set[str] = set()
    for name in chosen_names:
        result |= lookup[name]
    return result


if __name__ == "__main__":
    universe = {"a", "b", "c", "d", "e"}
    subsets = [
        ("S1", {"a", "b"}),
        ("S2", {"b", "c", "d"}),
        ("S3", {"d", "e"}),
        ("S4", {"e"}),
    ]
    chosen = greedy_set_cover(universe, subsets)
    assert chosen == ["S2", "S1", "S3"]
    assert universe <= covered_elements(chosen, subsets)

    assert greedy_set_cover(set(), subsets) == []

    print("002_set_cover_greedy: all examples passed")
