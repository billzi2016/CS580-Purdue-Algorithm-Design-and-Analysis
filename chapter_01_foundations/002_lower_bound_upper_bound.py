"""
文件意图：
    本文件手写实现 lower_bound 和 upper_bound，用于在有序数组中定位插入边界。

适用场景：
    需要处理重复元素、统计目标值出现次数、或寻找第一个满足条件的位置。

核心思想：
    使用二分维护半开区间 [left, right)，让搜索结束时 left 成为最小可行下标。

时间复杂度：
    O(log n)

空间复杂度：
    O(1)
"""


def lower_bound(nums: list[int], target: int) -> int:
    """
    返回 nums 中第一个大于等于 target 的位置。

    参数：
        nums: 已按非递减顺序排列的数组。
        target: 查询目标。

    返回：
        第一个满足 nums[i] >= target 的下标；如果不存在，返回 len(nums)。
    """
    left, right = 0, len(nums)

    # 不变量：答案始终位于半开区间 [left, right] 中。
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left


def upper_bound(nums: list[int], target: int) -> int:
    """
    返回 nums 中第一个大于 target 的位置。

    参数：
        nums: 已按非递减顺序排列的数组。
        target: 查询目标。

    返回：
        第一个满足 nums[i] > target 的下标；如果不存在，返回 len(nums)。
    """
    left, right = 0, len(nums)

    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return left


def count_equal(nums: list[int], target: int) -> int:
    """
    统计 target 在有序数组中的出现次数。

    关键点：
        出现次数等于 upper_bound(target) - lower_bound(target)。
    """
    return upper_bound(nums, target) - lower_bound(nums, target)


if __name__ == "__main__":
    nums = [1, 2, 2, 2, 4, 7]
    assert lower_bound(nums, 2) == 1
    assert upper_bound(nums, 2) == 4
    assert count_equal(nums, 2) == 3
    assert lower_bound(nums, 3) == 4
    assert upper_bound(nums, 7) == 6
    assert lower_bound([], 5) == 0

    print("002_lower_bound_upper_bound: all examples passed")
