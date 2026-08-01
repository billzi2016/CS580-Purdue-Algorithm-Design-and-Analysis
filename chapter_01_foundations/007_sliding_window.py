"""
文件意图：
    本文件手写实现滑动窗口模式，用于处理连续子数组或连续子串问题。

适用场景：
    窗口左右端点只向右移动，窗口状态可以增量维护。

核心思想：
    右端点扩展窗口，必要时移动左端点收缩窗口，使窗口始终满足目标约束。
"""


def min_subarray_len_at_least_target(nums: list[int], target: int) -> int:
    """
    返回和至少为 target 的最短连续子数组长度。

    前提：
        nums 中元素应为非负数；否则窗口和不具备单调收缩性质。
    """
    left = 0
    current_sum = 0
    best = len(nums) + 1

    for right, value in enumerate(nums):
        current_sum += value

        # 当前窗口已经满足条件时，尽量收缩左端点以获得更短答案。
        while current_sum >= target:
            best = min(best, right - left + 1)
            current_sum -= nums[left]
            left += 1

    return 0 if best == len(nums) + 1 else best


def longest_substring_without_repeating_chars(text: str) -> int:
    """
    返回不含重复字符的最长子串长度。
    """
    last_seen: dict[str, int] = {}
    left = 0
    best = 0

    for right, char in enumerate(text):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        best = max(best, right - left + 1)

    return best


if __name__ == "__main__":
    assert min_subarray_len_at_least_target([2, 3, 1, 2, 4, 3], 7) == 2
    assert min_subarray_len_at_least_target([1, 1, 1], 5) == 0
    assert longest_substring_without_repeating_chars("abcabcbb") == 3
    assert longest_substring_without_repeating_chars("bbbbb") == 1
    assert longest_substring_without_repeating_chars("") == 0

    print("007_sliding_window: all examples passed")
