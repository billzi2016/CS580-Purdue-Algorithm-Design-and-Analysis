"""
文件意图：手写构造区间 [1,n] 中规模最大的无相邻整数集合，并验证极值上界。
适用场景：鸽巢原理、路径图最大独立集及“按块给上界，再给达到上界的构造”类极值问题。
核心思想：将数列按相邻二元块 (1,2)、(3,4)… 分组，每组至多选择一个；选择所有奇数恰好达到该上界。
输入输出：输入非负 n，输出一个最大无相邻集合和它的最大可能大小。
时间复杂度：构造 O(n)，空间复杂度 O(n)（输出集合所需空间）。
关键边界情况：n=0 的答案为空；负 n 没有对应区间，必须拒绝。
"""


def construct_maximum_non_adjacent_set(n: int) -> list[int]:
    """构造 [1,n] 中不含相邻整数的一个最大规模子集。

    参数：n 是区间右端点，必须非负。
    返回：从小到大排列的最大无相邻整数集合。
    边界情况：n 为 0 时返回空列表；n 为负数时抛出 ValueError。
    关键算法点：选择所有奇数，每相邻两个整数最多一个被选，因此该构造达到逐块上界。
    """
    if n < 0:
        raise ValueError("n 必须是非负整数")
    return list(range(1, n + 1, 2))


def maximum_non_adjacent_size(n: int) -> int:
    """返回 [1,n] 中无相邻整数子集的最大可能规模。

    参数：n 是非负区间右端点。
    返回：最大规模 ceil(n/2)。
    边界情况：n=0 返回 0；负 n 抛出 ValueError。
    关键算法点：将区间分成大小至多为二的相邻块，每块最多取一个，故上界为 ceil(n/2)。
    """
    if n < 0:
        raise ValueError("n 必须是非负整数")
    return (n + 1) // 2


def is_valid_maximum_construction(n: int, chosen: list[int]) -> bool:
    """验证 chosen 是否为 [1,n] 的最大无相邻整数集合。

    参数：n 是区间右端点；chosen 是候选集合列表。
    返回：范围合法、互异、无相邻且规模达到上界时返回真。
    边界情况：n 为负或 chosen 包含越界/重复值时返回假。
    关键算法点：排序后只需检查相邻选中值之差，大小再与已证明上界比较。
    """
    if n < 0 or len(set(chosen)) != len(chosen) or any(value < 1 or value > n for value in chosen):
        return False
    ordered = sorted(chosen)
    if any(right - left == 1 for left, right in zip(ordered, ordered[1:])):
        return False
    return len(chosen) == maximum_non_adjacent_size(n)


def pair_block_upper_bound(n: int) -> list[tuple[int, int | None]]:
    """返回用于极值证明的相邻块划分，展示每块至多选一个的上界来源。

    参数：n 是非负区间右端点。
    返回：(奇数, 后继偶数或 None) 组成的块列表。
    边界情况：n=0 返回空列表；负 n 抛出 ValueError。
    关键算法点：块彼此不交并覆盖 [1,n]，块内两个值相邻，从而每块贡献不超过一个选中元素。
    """
    if n < 0:
        raise ValueError("n 必须是非负整数")
    return [(start, start + 1 if start + 1 <= n else None) for start in range(1, n + 1, 2)]


if __name__ == "__main__":
    assert construct_maximum_non_adjacent_set(0) == []
    assert construct_maximum_non_adjacent_set(6) == [1, 3, 5]
    assert construct_maximum_non_adjacent_set(7) == [1, 3, 5, 7]
    assert maximum_non_adjacent_size(7) == 4
    assert pair_block_upper_bound(5) == [(1, 2), (3, 4), (5, None)]
    assert is_valid_maximum_construction(6, [2, 4, 6])
    assert not is_valid_maximum_construction(6, [1, 2, 5])
    print("005_extremal_construction: all examples passed")
