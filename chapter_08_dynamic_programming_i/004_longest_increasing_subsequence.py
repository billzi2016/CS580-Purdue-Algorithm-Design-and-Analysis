"""
文件意图：
    本文件手写实现最长递增子序列（LIS），包括 O(n^2) DP 和 O(n log n) 贪心加二分。

适用场景：
    需要在序列中选择下标递增、值严格递增的最长子序列。

核心思想：
    O(n^2) DP 直接枚举前驱；O(n log n) 方法维护每个长度的最小可能结尾值。

时间复杂度：
    O(n^2) 或 O(n log n)

空间复杂度：
    O(n)
"""


def lis_length_dp(nums: list[int]) -> int:
    """使用 O(n^2) DP 计算 LIS 长度。"""
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def lis_length_binary_search(nums: list[int]) -> int:
    """手写 lower_bound，用 O(n log n) 计算 LIS 长度。"""
    tails: list[int] = []
    for value in nums:
        index = _lower_bound(tails, value)
        if index == len(tails):
            tails.append(value)
        else:
            tails[index] = value
    return len(tails)


def _lower_bound(nums: list[int], target: int) -> int:
    """返回第一个大于等于 target 的位置。"""
    left, right = 0, len(nums)
    while left < right:
        middle = left + (right - left) // 2
        if nums[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left


if __name__ == "__main__":
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    assert lis_length_dp(nums) == 4
    assert lis_length_binary_search(nums) == 4
    assert lis_length_dp([]) == 0
    assert lis_length_binary_search([]) == 0
    assert lis_length_binary_search([2, 2, 2]) == 1

    print("004_longest_increasing_subsequence: all examples passed")
