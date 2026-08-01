"""
文件意图：
    本文件手写实现分治 DP 优化，以一维数组分 k 段最小平方和代价为例。

适用场景：
    DP 转移形如 dp[g][i] = min(dp[g-1][j] + cost(j, i))，且最优决策点单调。

核心思想：
    对当前层的区间中点 mid 求最优决策点，并利用决策单调性递归限制左右区间的搜索范围。

时间复杂度：
    O(k * n log n) 级别的教学实现，优于朴素 O(k * n^2)。

空间复杂度：
    O(k * n)
"""


def partition_min_square_sum(nums: list[int], groups: int) -> int:
    """把 nums 划分为 groups 个连续非空段，最小化每段元素和平方之和。"""
    n = len(nums)
    if groups <= 0:
        raise ValueError("groups 必须为正")
    if n == 0:
        return 0
    groups = min(groups, n)

    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] + value)

    def cost(left: int, right: int) -> int:
        segment_sum = prefix[right] - prefix[left]
        return segment_sum * segment_sum

    previous = [0] + [10**18] * n
    for group in range(1, groups + 1):
        current = [10**18] * (n + 1)
        _compute_layer(1, n, 0, n - 1, previous, current, cost)
        previous = current

    return previous[n]


def _compute_layer(
    left: int,
    right: int,
    opt_left: int,
    opt_right: int,
    previous: list[int],
    current: list[int],
    cost,
) -> None:
    """递归计算当前 DP 层的 [left, right]。"""
    if left > right:
        return

    mid = (left + right) // 2
    best_value = 10**18
    best_split = opt_left

    for split in range(opt_left, min(opt_right, mid - 1) + 1):
        candidate = previous[split] + cost(split, mid)
        if candidate < best_value:
            best_value = candidate
            best_split = split

    current[mid] = best_value
    _compute_layer(left, mid - 1, opt_left, best_split, previous, current, cost)
    _compute_layer(mid + 1, right, best_split, opt_right, previous, current, cost)


if __name__ == "__main__":
    assert partition_min_square_sum([1, 2, 3], 1) == 36
    assert partition_min_square_sum([1, 2, 3], 2) == 18
    assert partition_min_square_sum([1, 2, 3], 3) == 14
    assert partition_min_square_sum([], 3) == 0

    print("008_divide_and_conquer_dp: all examples passed")
