"""
文件意图：
    本文件手写实现双指针常见模式，用于有序数组配对和原地去重。

适用场景：
    输入具有单调性，或可以用两个方向移动的指针避免 O(n^2) 枚举。

核心思想：
    根据当前状态移动左指针或右指针，每一步都排除一批不可能答案。
"""


def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int] | None:
    """
    在有序数组中寻找两个数，使它们的和等于 target。

    返回：
        如果存在，返回两个下标；否则返回 None。
    """
    left, right = 0, len(nums) - 1

    while left < right:
        current = nums[left] + nums[right]
        if current == target:
            return left, right
        if current < target:
            left += 1
        else:
            right -= 1

    return None


def remove_duplicates_sorted(nums: list[int]) -> int:
    """
    原地删除有序数组中的重复值。

    返回：
        去重后的有效长度。nums[:length] 是去重结果。
    """
    if not nums:
        return 0

    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1

    return write


if __name__ == "__main__":
    assert two_sum_sorted([1, 2, 4, 7, 11], 9) == (1, 3)
    assert two_sum_sorted([1, 2, 4, 7, 11], 20) is None

    nums = [1, 1, 2, 2, 3, 5, 5]
    length = remove_duplicates_sorted(nums)
    assert length == 4
    assert nums[:length] == [1, 2, 3, 5]

    print("006_two_pointers: all examples passed")
