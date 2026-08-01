"""
装箱问题启发式：First Fit、Best Fit、First Fit Decreasing。

本文件的意图：
1. 手写常见 bin packing heuristic，不把 NP-hard 问题伪装成精确求解。
2. 明确每个启发式的行为差异，便于对比近似算法和工程启发式。
3. 所有函数都返回具体箱子内容，方便检查容量约束。

注意：
装箱问题的最优解搜索通常需要指数级回溯或整数规划；本章只实现多项式启发式。
"""


def first_fit(items: list[int], capacity: int) -> list[list[int]]:
    """按输入顺序，把每个物品放入第一个能容纳它的箱子。"""

    _validate_items(items, capacity)
    bins: list[list[int]] = []

    for item in items:
        placed = False
        for bucket in bins:
            if sum(bucket) + item <= capacity:
                bucket.append(item)
                placed = True
                break
        if not placed:
            bins.append([item])

    return bins


def best_fit(items: list[int], capacity: int) -> list[list[int]]:
    """把物品放入剩余空间最小但仍能容纳它的箱子。"""

    _validate_items(items, capacity)
    bins: list[list[int]] = []

    for item in items:
        best_index = -1
        best_remaining = capacity + 1

        for index, bucket in enumerate(bins):
            remaining = capacity - sum(bucket) - item
            if 0 <= remaining < best_remaining:
                best_remaining = remaining
                best_index = index

        if best_index == -1:
            bins.append([item])
        else:
            bins[best_index].append(item)

    return bins


def first_fit_decreasing(items: list[int], capacity: int) -> list[list[int]]:
    """先按体积降序排列，再执行 First Fit。"""

    return first_fit(sorted(items, reverse=True), capacity)


def all_bins_valid(bins: list[list[int]], capacity: int) -> bool:
    """验证每个箱子的总容量不超过 capacity。"""

    return all(sum(bucket) <= capacity for bucket in bins)


def _validate_items(items: list[int], capacity: int) -> None:
    """检查容量和物品大小是否合法。"""

    if capacity <= 0:
        raise ValueError("capacity 必须为正数")
    for item in items:
        if item <= 0:
            raise ValueError("物品大小必须为正数")
        if item > capacity:
            raise ValueError("单个物品不能超过箱子容量")


if __name__ == "__main__":
    items = [4, 8, 1, 4, 2, 1]
    assert first_fit(items, 10) == [[4, 1, 4, 1], [8, 2]]
    best_fit_bins = best_fit(items, 10)
    assert all_bins_valid(best_fit_bins, 10)
    assert len(best_fit_bins) == 2
    assert sorted(item for bucket in best_fit_bins for item in bucket) == sorted(items)
    ffd_bins = first_fit_decreasing(items, 10)
    assert all_bins_valid(ffd_bins, 10)
    assert len(ffd_bins) == 2
    assert first_fit([], 10) == []

    print("003_bin_packing_heuristics: all examples passed")
