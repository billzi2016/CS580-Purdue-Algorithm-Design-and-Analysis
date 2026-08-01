"""
文件意图：
    本文件手写实现一维前缀和，用于 O(1) 查询数组区间和。

适用场景：
    原数组静态不变，但需要多次查询连续区间的元素和。

核心思想：
    prefix[i] 存储 nums[0:i] 的总和，因此区间 [left, right] 的和为
    prefix[right + 1] - prefix[left]。

预处理复杂度：
    O(n)

单次查询复杂度：
    O(1)
"""


def build_prefix_sum(nums: list[int]) -> list[int]:
    """
    构建一维前缀和数组。

    返回：
        长度为 len(nums) + 1 的 prefix，其中 prefix[0] = 0。
    """
    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] + value)
    return prefix


def range_sum(prefix: list[int], left: int, right: int) -> int:
    """
    查询闭区间 [left, right] 的元素和。

    参数：
        prefix: build_prefix_sum 返回的前缀和数组。
        left: 查询左端点。
        right: 查询右端点。

    返回：
        nums[left] + ... + nums[right]。
    """
    if left < 0 or right + 1 >= len(prefix) or left > right:
        raise ValueError("查询区间必须是合法闭区间 [left, right]")
    return prefix[right + 1] - prefix[left]


if __name__ == "__main__":
    nums = [2, -1, 3, 5, -2]
    prefix = build_prefix_sum(nums)

    assert prefix == [0, 2, 1, 4, 9, 7]
    assert range_sum(prefix, 0, 0) == 2
    assert range_sum(prefix, 1, 3) == 7
    assert range_sum(prefix, 0, 4) == 7

    print("003_prefix_sum: all examples passed")
