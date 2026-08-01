"""
文件意图：
    本文件手写实现逆序对计数，用于统计数组中满足 i < j 且 nums[i] > nums[j]
    的下标对数量。

适用场景：
    需要衡量数组距离有序状态有多远，或在排序过程中顺便统计跨区间逆序关系。

核心思想：
    使用归并排序的分治结构。左半部分和右半部分分别递归统计逆序对；
    合并两个有序子数组时，如果左侧当前元素大于右侧当前元素，则左侧剩余
    所有元素都会与右侧当前元素形成逆序对。

输入输出：
    输入整数数组，返回逆序对数量和排序后的新数组。

时间复杂度：
    O(n log n)

空间复杂度：
    O(n)
"""


def count_inversions(nums: list[int]) -> tuple[int, list[int]]:
    """
    统计 nums 中的逆序对数量，并返回排序后的数组。

    参数：
        nums: 待统计的整数数组。

    返回：
        (inversion_count, sorted_nums)。

    边界情况：
        空数组和单元素数组没有逆序对。
    """
    if len(nums) <= 1:
        return 0, nums[:]

    middle = len(nums) // 2
    left_count, left_sorted = count_inversions(nums[:middle])
    right_count, right_sorted = count_inversions(nums[middle:])
    split_count, merged = _merge_and_count_split_inversions(left_sorted, right_sorted)

    return left_count + right_count + split_count, merged


def _merge_and_count_split_inversions(
    left: list[int], right: list[int]
) -> tuple[int, list[int]]:
    """
    合并两个有序数组，并统计跨左右两侧的逆序对。

    关键点：
        当 left[i] > right[j] 时，因为 left[i:] 已经有序，所以 left[i:] 中
        的每个元素都大于 right[j]，一次性贡献 len(left) - i 个逆序对。
    """
    i = 0
    j = 0
    inversions = 0
    merged: list[int] = []

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inversions += len(left) - i
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return inversions, merged


if __name__ == "__main__":
    assert count_inversions([]) == (0, [])
    assert count_inversions([1]) == (0, [1])
    assert count_inversions([1, 2, 3]) == (0, [1, 2, 3])
    assert count_inversions([3, 2, 1]) == (3, [1, 2, 3])
    assert count_inversions([2, 4, 1, 3, 5]) == (3, [1, 2, 3, 4, 5])
    assert count_inversions([1, 3, 2, 3, 1]) == (4, [1, 1, 2, 3, 3])

    print("001_count_inversions: all examples passed")
