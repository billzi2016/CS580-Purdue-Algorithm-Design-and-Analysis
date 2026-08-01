"""
文件意图：
    本文件手写实现一维差分数组，用于高效处理多次区间加法更新。

适用场景：
    需要对静态长度数组执行多次区间增量更新，最后一次性恢复最终数组。

核心思想：
    对闭区间 [left, right] 加 delta 时，只修改 diff[left] 和 diff[right + 1]。
    最终通过前缀累加 diff 得到每个位置的真实值。

区间更新复杂度：
    O(1)

恢复数组复杂度：
    O(n)
"""


def build_difference_array(nums: list[int]) -> list[int]:
    """
    根据原数组构建差分数组。
    """
    if not nums:
        return []

    diff = [0] * len(nums)
    diff[0] = nums[0]
    for index in range(1, len(nums)):
        diff[index] = nums[index] - nums[index - 1]
    return diff


def range_add(diff: list[int], left: int, right: int, delta: int) -> None:
    """
    对闭区间 [left, right] 加上 delta。

    注意：
        本函数原地修改 diff。
    """
    if left < 0 or right >= len(diff) or left > right:
        raise ValueError("更新区间必须是合法闭区间 [left, right]")

    diff[left] += delta
    if right + 1 < len(diff):
        diff[right + 1] -= delta


def restore_from_difference(diff: list[int]) -> list[int]:
    """
    从差分数组恢复最终数组。
    """
    nums: list[int] = []
    running = 0
    for value in diff:
        running += value
        nums.append(running)
    return nums


if __name__ == "__main__":
    nums = [1, 2, 3, 4, 5]
    diff = build_difference_array(nums)
    range_add(diff, 1, 3, 10)
    range_add(diff, 0, 0, -1)

    assert restore_from_difference(diff) == [0, 12, 13, 14, 5]
    assert build_difference_array([]) == []

    print("005_difference_array: all examples passed")
