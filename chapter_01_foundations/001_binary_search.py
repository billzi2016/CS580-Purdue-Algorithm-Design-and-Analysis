"""
文件意图：
    本文件手写实现二分查找，用于在有序数组中查找目标值。

适用场景：
    输入数组已经按非递减顺序排列，需要在 O(log n) 时间内判断目标值是否存在。

核心思想：
    每次检查当前搜索区间的中点，根据中点值与目标值的大小关系排除一半区间。

时间复杂度：
    O(log n)

空间复杂度：
    O(1)
"""


def binary_search(nums: list[int], target: int) -> int:
    """
    在有序数组 nums 中查找 target。

    参数：
        nums: 已按非递减顺序排列的整数数组。
        target: 需要查找的目标值。

    返回：
        如果找到 target，返回其中一个匹配下标；否则返回 -1。

    边界情况：
        空数组会直接跳过循环并返回 -1。
    """
    left, right = 0, len(nums) - 1

    # 循环不变量：如果 target 存在，它一定在闭区间 [left, right] 内。
    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


if __name__ == "__main__":
    examples = [
        ([1, 3, 5, 7, 9], 5, 2),
        ([1, 3, 5, 7, 9], 4, -1),
        ([], 10, -1),
        ([2], 2, 0),
        ([2], 3, -1),
    ]

    for nums, target, expected in examples:
        assert binary_search(nums, target) == expected

    print("001_binary_search: all examples passed")
