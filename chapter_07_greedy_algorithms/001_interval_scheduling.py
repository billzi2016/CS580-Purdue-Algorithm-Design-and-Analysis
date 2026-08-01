"""
文件意图：
    本文件手写实现区间调度贪心算法，用于选择数量最多的互不重叠区间。

适用场景：
    每个任务占用一个时间区间，目标是安排最多任务，任务权重相同。

核心思想：
    每次选择结束时间最早且与已选任务不冲突的区间。结束越早，留给后续任务的空间越大。

时间复杂度：
    O(n log n)

空间复杂度：
    O(n)
"""

Interval = tuple[int, int]


def select_max_non_overlapping_intervals(intervals: list[Interval]) -> list[Interval]:
    """
    选择最多数量的互不重叠区间。

    参数：
        intervals: 区间列表，每个区间为 (start, end)，要求 start <= end。

    返回：
        被选中的区间列表，按结束时间排序。
    """
    for start, end in intervals:
        if start > end:
            raise ValueError("区间必须满足 start <= end")

    selected: list[Interval] = []
    current_end: int | None = None

    for interval in sorted(intervals, key=lambda item: (item[1], item[0])):
        start, end = interval
        if current_end is None or start >= current_end:
            selected.append(interval)
            current_end = end

    return selected


if __name__ == "__main__":
    assert select_max_non_overlapping_intervals([(1, 3), (2, 4), (3, 5), (0, 7)]) == [(1, 3), (3, 5)]
    assert select_max_non_overlapping_intervals([]) == []
    assert select_max_non_overlapping_intervals([(1, 2), (2, 3), (3, 4)]) == [(1, 2), (2, 3), (3, 4)]

    try:
        select_max_non_overlapping_intervals([(5, 1)])
        raise AssertionError("非法区间必须抛出 ValueError")
    except ValueError:
        pass

    print("001_interval_scheduling: all examples passed")
