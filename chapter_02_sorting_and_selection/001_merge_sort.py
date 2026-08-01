"""
文件意图：手写实现稳定的归并排序。
适用场景：需要稳定地排序可比较元素，或需要保证 O(n log n) 最坏时间复杂度时。
核心思想：递归排序两个半区间，再线性合并两个有序结果。
输入输出：输入可比较元素列表，返回一个新的非递减排序列表。
时间复杂度：O(n log n)。空间复杂度：O(n)。
关键边界：空列表和单元素列表直接返回；相等元素优先从左半区取出以保持稳定性。
"""

from typing import TypeVar

T = TypeVar("T")


def merge_sort(values: list[T]) -> list[T]:
    """返回 values 的稳定非递减排序副本。

    参数：values 为彼此可用 <= 比较的元素列表。
    返回：不修改原列表的新排序列表。
    边界情况：长度小于等于一时直接复制返回。
    关键算法点：合并阶段只在两个有序前缀中选择较小元素。
    """
    if len(values) <= 1:
        return values[:]

    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    merged: list[T] = []
    left_index = right_index = 0

    # 循环不变量：merged 始终是已消费元素的稳定有序合并结果。
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


if __name__ == "__main__":
    assert merge_sort([]) == []
    assert merge_sort([7]) == [7]
    assert merge_sort([5, 1, 4, 1, 3]) == [1, 1, 3, 4, 5]
    assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    print("001_merge_sort: all examples passed")
