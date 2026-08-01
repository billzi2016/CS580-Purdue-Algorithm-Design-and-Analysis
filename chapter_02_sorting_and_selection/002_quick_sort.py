"""
文件意图：手写实现三向划分的快速排序。
适用场景：一般内存排序，尤其适合含有较多重复值的可比较元素列表。
核心思想：选取中间位置的枢轴，将元素划分为小于、等于和大于枢轴三部分后递归排序。
输入输出：输入可比较元素列表，返回新的非递减排序列表。
时间复杂度：平均 O(n log n)，最坏 O(n^2)。空间复杂度：平均 O(log n) 递归栈加 O(n) 输出。
关键边界：空列表、单元素和所有元素相同的列表均可直接处理。
"""

from typing import TypeVar

T = TypeVar("T")


def quick_sort(values: list[T]) -> list[T]:
    """返回 values 的非递减排序副本。

    参数：values 为彼此可比较的元素列表。
    返回：不修改原列表的新排序列表。
    边界情况：长度小于等于一时直接返回副本。
    关键算法点：三向划分避免重复枢轴元素造成的无效递归。
    """
    if len(values) <= 1:
        return values[:]

    pivot = values[len(values) // 2]
    smaller: list[T] = []
    equal: list[T] = []
    greater: list[T] = []
    for value in values:
        if value < pivot:
            smaller.append(value)
        elif value > pivot:
            greater.append(value)
        else:
            equal.append(value)
    return quick_sort(smaller) + equal + quick_sort(greater)


if __name__ == "__main__":
    assert quick_sort([]) == []
    assert quick_sort([9]) == [9]
    assert quick_sort([3, 1, 2, 3, 3, 0]) == [0, 1, 2, 3, 3, 3]
    assert quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    print("002_quick_sort: all examples passed")
